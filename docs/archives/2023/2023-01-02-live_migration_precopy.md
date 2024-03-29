---
title: Live Migration Precopy Analyze
layout: default
parent: 2023
grand_parent: Archives
---

**live_migration**
{: .label .label-blue }

**qemu**
{: .label .label-green }

**libvirt**
{: .label .label-purple }

**kvm**
{: .label .label-yellow }

**precopy**
{: .label .label-red }


# 热迁移原理

## 热迁移核心步骤

### 虚拟化层面实现流程和通信方式

1. 通过 python libvirt 接口启动 libvirt 迁移流程
2. client（agent compute）连接源端 libvirtd 进程
3. client 连接目的端 libvirt 进程
4. 调用源端 domainMigrateBegin3
5. 调用目的端 domainMigratePrapare3
6. 调用源端 domainMigratePerform3
	domainMigratePerform3函数主要是执行迁移操作，将源端的数据迁移到目的端。然后等待迁移完成的信号
	大致的调用流程：
		1. qemuDomainMigratePerform3 → 
			qemuMigrationPerform → 
			qemuMigrationPerformPhase → 
			doNativeMigrate → 
			qemuMigrationRun → 
			qemuMonitorSetMigrationSpeed →
			qemuMigrationConnect →  
			qemuMonitorMigrateToHost → 
			qemuMonitorJSONMigrate 
		2. 终会调用到 QEMU中的qmp_migrate
		3. setup iterature complete
7. 源端 libvirtd 进程调用 源端 qemu qmp_migrate 
	tcp_start_outgoing_migration
	migrate_fd_connect
	migrate_compress_thread_create
	migration_thread
	qemu_savevm_state_begin
	qemu_savevm_state_pending
	qemu_savevm_state_iterate
	migration_completion
	vm_stop
8. 目的端
	qemu_start_incoming_migration
	tcp_start_incoming_migration
	process_incoming_migration_co
	migrate_decompress_threads_create
	qemu_loadvm_state
	cpu_synchronize_all_post_init
	process_incoming_migration_bin
	vm_start

### 源端调用流程分析
* TODO

### 目的端调用流程分析
* TODO

### qmp_migrate
* tcp_start_outgoing_migration
	* 创建和目的端 libvirt 的 tcp 连接
* migrate_fd_connect
	* qemu接收来自 libvirt 传入的fd (tcp socket)，准备写入数据
* 迁移主函数 migration_thread
	* 发送header
	* 建立迁移的准备
	* 迭代传输
	* 完成迁移


### qemu 内存迁移 - 标脏所有的内存页

#### kvm 内存管理简介

* GVA - Guest虚拟地址

* GPA - Guest物理地址

* HVA - Host虚拟地址

* HPA -Host物理地址

```c
typedef struct KVMSlot
{
     hwaddr start_addr;               //Guest物理地址块的起始地址
     ram_addr_t memory_size;          //大小
     void *ram;                       //QUMU用户空间地址 
     int slot;                        //slot id
     int flags;
} KVMSlot;


struct kvm_memslots {
	int nmemslots;                      //slot number
	struct kvm_memory_slot memslots[KVM_MEMORY_SLOTS + KVM_PRIVATE_MEM_SLOTS];
};


struct kvm_memory_slot {
	gfn_t base_gfn;                     //该块物理内存块所在guest 物理页帧号
	unsigned long npages;               //该块物理内存块占用的page数
	unsigned long flags;
	unsigned long *rmap;                //分配该块物理内存对应的host内核虚拟地址（vmalloc分配）
	unsigned long *dirty_bitmap;
	struct {
		unsigned long rmap_pde;
		int write_count;
	} *lpage_info[KVM_NR_PAGE_SIZES - 1];
	unsigned long userspace_addr;       //用户空间地址（QEMU)
	int user_alloc;
};
```

0. KVM的虚拟机实际上运行在Qemu的进程上下文中
1. 虚拟机的物理内存实际上是Qemu进程的虚拟地址
2. KVMSlot 定义了GPA到HVA的映射关系，也就是虚拟机物理地址和宿主机OS虚拟地址之间的关系
3. Guest运行过程中，内存访问的过程，根据其所在memslot区域获得其对应的HVA 宿主机os虚拟地址，交给宿主机OS将HVA转化为HPA，得到宿主页帧号，对于缺页有缺页处理函数负责完成GPA->HPA转化


* memory model (info mtree from QEMU monitor console of guest vm)
* MemoryRegion 用于描述一个范围内的映射规则
* AddressSpace 用于描述整个地址空间的映射关系
* guest 通过映射关系访问到这些地址
	* 从顶层 MemoryRegion 逐个找其 child MemoryRegion，其中还需要处理 alias 和 priority 的问题
	* QEMU 在 MemoryRegion 的属性发生修改
	* MemoryRegion 生成 FlatRange，避免逐级查询 MemoryRegion
	* FlatRange 树形结构查询，查询时间复杂度 O(n) 优化到 O(log(N))
* 例如：kvm 处理 io 端口的操作键盘输入，只要给出 AddressSpace 以及地址，最后就可以找到最后的 handler 为 kbd_read_data

```c
// 调用栈
/*
#2  kbd_read_data (opaque=0x555556844d98, addr=<optimized out>, size=<optimized out>) at ../hw/input/pckbd.c:387
#3  0x0000555555cd2092 in memory_region_read_accessor (mr=mr@entry=0x555556844df0, addr=0, value=value@entry=0x7fffd9ff9130, size=size@entry=1, shift=0, mask=mask@entry=255, attrs=...) at ../softmmu/memory.c:440
#4  0x0000555555cceb1e in access_with_adjusted_size (addr=addr@entry=0, value=value@entry=0x7fffd9ff9130, size=size@entry=1, access_size_min=<optimized out>, access_size_max=<optimized out>, access_fn=0x555555cd2050 <memory_region_read_accessor>, mr=0x555556844df0, attrs=...) at ../softmmu/memory.c:554
#5  0x0000555555cd1ac1 in memory_region_dispatch_read1 (attrs=..., size=<optimized out>, pval=0x7fffd9ff9130, addr=0, mr=0x555556844df0) at ../softmmu/memory.c:1424
#6  memory_region_dispatch_read (mr=mr@entry=0x555556844df0, addr=0, pval=pval@entry=0x7fffd9ff9130, op=MO_8, attrs=attrs@entry=...) at ../softmmu/memory.c:1452
#7  0x0000555555c9eb89 in flatview_read_continue (fv=fv@entry=0x7ffe4402d230, addr=addr@entry=96, attrs=..., ptr=ptr@entry=0x7fffeb17d000, len=len@entry=1, addr1=<optimized out>, l=<optimized out>, mr=0x555556844df0) at /home/maritns3/core/kvmqemu/include/qemu/host-utils.h:165
#8  0x0000555555c9ed43 in flatview_read (fv=0x7ffe4402d230, addr=addr@entry=96, attrs=attrs@entry=..., buf=buf@entry=0x7fffeb17d000, len=len@entry=1) at ../softmmu/physmem.c:2881
#9  0x0000555555c9ee96 in address_space_read_full (as=0x555556606880 <address_space_io>, addr=96, attrs=..., buf=0x7fffeb17d000, len=1) at ../softmmu/physmem.c:2894
#10 0x0000555555c9f015 in address_space_rw (as=<optimized out>, addr=addr@entry=96, attrs=..., attrs@entry=..., buf=<optimized out>, len=len@entry=1, is_write=is_write@entry=false) at ../softmmu/physmem.c:2922
#11 0x0000555555c8ece9 in kvm_handle_io (count=1, size=1, direction=<optimized out>, data=<optimized out>, attrs=..., port=96) at ../accel/kvm/kvm-all.c:2635
#12 kvm_cpu_exec (cpu=cpu@entry=0x555556af4410) at ../accel/kvm/kvm-all.c:2886
#13 0x0000555555cf1825 in kvm_vcpu_thread_fn (arg=arg@entry=0x555556af4410) at ../accel/kvm/kvm-accel-ops.c:49
#14 0x0000555555e55983 in qemu_thread_start (args=<optimized out>) at ../util/qemu-thread-posix.c:541
#15 0x00007ffff628d609 in start_thread (arg=<optimized out>) at pthread_create.c:477
#16 0x00007ffff61b4293 in clone () at ../sysdeps/unix/sysv/linux/x86_64/clone.S:95
*/
```

```c
//┌──────────► 这是一个 AddressSpace，AddressSpace 用于描述整个地址空间的映射关系。
// │                                        ┌───────────────────────► MemoryRegion 的优先级，如果一个范围两个 MemoryRegion 出现重叠，优先级高的压制优先级低的
// │                                        │
// │                                        │   ┌───────────────────► 表示这个空间的类型，一般划分为 io 和 RAM
// │                                        │   │    ┌──────────────► 这是一个 MemoryRegion，这是 Address Space 中最核心的概念，MemoryRegion 用于描述一个范围内的映射规则
//address-space: memory                     │   │    │
  0000000000000000-ffffffffffffffff (prio 0, i/o): system
  0000000000000000-ffffffffffffffff (prio 0, i/o): system
    0000000000000000-00000000bfffffff (prio 0, ram): alias ram-below-4g @pc.ram 0000000000000000-00000000bfffffff ──────────────┐
    0000000000000000-ffffffffffffffff (prio -1, i/o): pci                                                                       │
      00000000000a0000-00000000000bffff (prio 1, i/o): vga-lowmem                                                               │
      00000000000c0000-00000000000dffff (prio 1, rom): pc.rom                                                                   │
      00000000000e0000-00000000000fffff (prio 1, rom): alias isa-bios @pc.bios 0000000000020000-000000000003ffff                │
      00000000fd000000-00000000fdffffff (prio 1, ram): vga.vram                                                                 │
      00000000fe000000-00000000fe003fff (prio 1, i/o): virtio-pci                                                               │
        00000000fe000000-00000000fe000fff (prio 0, i/o): virtio-pci-common-virtio-9p                                            │
        00000000fe001000-00000000fe001fff (prio 0, i/o): virtio-pci-isr-virtio-9p                                               │
        00000000fe002000-00000000fe002fff (prio 0, i/o): virtio-pci-device-virtio-9p                                            │
        00000000fe003000-00000000fe003fff (prio 0, i/o): virtio-pci-notify-virtio-9p                                            │
      00000000febc0000-00000000febdffff (prio 1, i/o): e1000-mmio                                                               │
      00000000febf0000-00000000febf3fff (prio 1, i/o): nvme-bar0                                                                │
        00000000febf0000-00000000febf1fff (prio 0, i/o): nvme                                                                   │
        00000000febf2000-00000000febf240f (prio 0, i/o): msix-table                                                             │
        00000000febf3000-00000000febf300f (prio 0, i/o): msix-pba                                                               │
      00000000febf4000-00000000febf7fff (prio 1, i/o): nvme-bar0                                                                │
        00000000febf4000-00000000febf5fff (prio 0, i/o): nvme                                                                   │
        00000000febf6000-00000000febf640f (prio 0, i/o): msix-table                                                             │
        00000000febf7000-00000000febf700f (prio 0, i/o): msix-pba                                                               │
      00000000febf8000-00000000febf8fff (prio 1, i/o): vga.mmio                                                                 │
        00000000febf8000-00000000febf817f (prio 0, i/o): edid                                                                   └── ram-below-4g 是 pc.ram 的一个 alias
        00000000febf8400-00000000febf841f (prio 0, i/o): vga ioports remapped
        00000000febf8500-00000000febf8515 (prio 0, i/o): bochs dispi interface                                                  ┌── ram-above-4g 也是 pc.ram 的一个 alias, 两者都被放到 system 这个 MemoryRegion 上
        00000000febf8600-00000000febf8607 (prio 0, i/o): qemu extended regs                                                     │
      00000000febf9000-00000000febf9fff (prio 1, i/o): virtio-9p-pci-msix                                                       │
        00000000febf9000-00000000febf901f (prio 0, i/o): msix-table                                                             │
        00000000febf9800-00000000febf9807 (prio 0, i/o): msix-pba                                                               │
      00000000fffc0000-00000000ffffffff (prio 0, rom): pc.bios                                                                  │
    00000000000a0000-00000000000bffff (prio 1, i/o): alias smram-region @pci 00000000000a0000-00000000000bffff                  │
    00000000000c0000-00000000000c3fff (prio 1, ram): alias pam-rom @pc.ram 00000000000c0000-00000000000c3fff                    │
    00000000000c4000-00000000000c7fff (prio 1, ram): alias pam-rom @pc.ram 00000000000c4000-00000000000c7fff                    │
    00000000000c8000-00000000000cbfff (prio 1, ram): alias pam-rom @pc.ram 00000000000c8000-00000000000cbfff                    │
    00000000000cb000-00000000000cdfff (prio 1000, ram): alias kvmvapic-rom @pc.ram 00000000000cb000-00000000000cdfff            │
    00000000000cc000-00000000000cffff (prio 1, ram): alias pam-rom @pc.ram 00000000000cc000-00000000000cffff                    │
    00000000000d0000-00000000000d3fff (prio 1, ram): alias pam-rom @pc.ram 00000000000d0000-00000000000d3fff                    │
    00000000000d4000-00000000000d7fff (prio 1, ram): alias pam-rom @pc.ram 00000000000d4000-00000000000d7fff                    │
    00000000000d8000-00000000000dbfff (prio 1, ram): alias pam-rom @pc.ram 00000000000d8000-00000000000dbfff                    │
    00000000000dc000-00000000000dffff (prio 1, ram): alias pam-rom @pc.ram 00000000000dc000-00000000000dffff                    │
    00000000000e0000-00000000000e3fff (prio 1, ram): alias pam-rom @pc.ram 00000000000e0000-00000000000e3fff                    │
    00000000000e4000-00000000000e7fff (prio 1, ram): alias pam-ram @pc.ram 00000000000e4000-00000000000e7fff                    │
    00000000000e8000-00000000000ebfff (prio 1, ram): alias pam-ram @pc.ram 00000000000e8000-00000000000ebfff                    │
    00000000000ec000-00000000000effff (prio 1, ram): alias pam-ram @pc.ram 00000000000ec000-00000000000effff                    │
    00000000000f0000-00000000000fffff (prio 1, ram): alias pam-rom @pc.ram 00000000000f0000-00000000000fffff                    │
    00000000fec00000-00000000fec00fff (prio 0, i/o): ioapic                                                                     │
    00000000fed00000-00000000fed003ff (prio 0, i/o): hpet                                                                       │
    00000000fee00000-00000000feefffff (prio 4096, i/o): apic-msi                                                                │
    0000000100000000-00000001bfffffff (prio 0, ram): alias ram-above-4g @pc.ram 00000000c0000000-000000017fffffff ──────────────┘
```

#### dirty page tracking 脏页标记
##### dirty bitmap
* bitmap是将原本需要占用1个字节或者多个字节的整数，转化成对一个字节单位中的一个确定位置的比特的占用
* Bitmaps are bit vectors where each ‘1’ bit in the vector indicates a modified (“dirty”) segment of the corresponding block device. The size of the segment that is tracked is the granularity of the bitmap. If the granularity of a bitmap is 64K, each ‘1’ bit means that a 64K region as a whole may have changed in some way, possibly by as little as one byte.、
* 将向量上的每个“1”表示为对应块的脏页，bitmap的增量每增加“1”，就是每个内存脏页大小（4kByte）变更了
* 核心：使用 bitmap 上每一个 solt 槽位来表示一个固定大小的脏页是否变更

* https://qemu-project.gitlab.io/qemu/interop/bitmaps.html


##### dirty ring
	* https://blog.csdn.net/huang987246510/article/details/112293303


```
+-------------+          +----------+       +--------------+          +---------------------+
|             |          | ram_list +-----> | dirty_memory +--------> | migration_bitmap_rcu|
|             |          +----------+       +------+-------+          +---------------------+
| Guest       |                                    ^
|             |                                    |
|             |                                    |
|             |                                    |用户态
|             +--------------------------------+   |-----
|             |                                |   |内核态
|             |                                |   |
|             |                                |   |
|             |                                v   |
|             |                                    |
|             |          +---------+       +-------+--------+
|             |          | memslot +-----> | dirty_bitmap   |
+-------------+          +---------+       +----------------+
```


##### 用户态
* 用户态与脏页统计有关的数据结构：RAMList和RAMBlock
* RAMList用在从内核获取脏页的时候，它表示脏页的粒度是kvm中的一个slot
	* 如前所述：KVMSlot 定义了GPA到HVA的映射关系，也就是虚拟机物理地址和宿主机OS虚拟地址之间的关系
* RAMBlock中的位图用来描述一个RAMBlock的脏页使用情况，它表示的脏页粒度是Qemu中的一个RAMBlock
* 在内存迁移统计脏页过程中，会依次使用这两个数据结构统计剩余内存的脏页数量

##### 内核态
* kvm_userspace_memory_region
* kvm_dirty_log
* kvm_memory_slot
* 为了让用于态统计虚机的脏页，内核提供了两个接口，分别是KVM_SET_USER_MEMORY_REGION、KVM_GET_DIRTY_LOG，这两个接口
* 内核提供了两个命令供用户态统计虚机的脏页，KVM_SET_USER_MEMORY_REGION、KVM_GET_DIRTY_LOG，KVM_SET_USER_MEMORY_REGION命令字作用在vm的fd，用来通知kvm开启对某段内存区域的脏页跟踪，结构体kvm_userspace_memory_region 是用户态传入的参数，用来描述kvm应该跟踪的内存区域
* KVM_GET_DIRTY_LOG命令字作用在vm的fd，用来获取内核跟踪的脏页信息，结构体kvm_dirty_log作为参数用来指定要查询的内存slot，同时保存内核的脏页查询结果

##### 交互过程简介
* 根据PML的硬件特性，每当CPU在Guest态根据EPT转换地址后，写数据到物理页，这时如果PML特性开启，在设置EPT页表项的Dirty位之后，还会将GPA地址写入PML Buffer。

##### 清零Dirty位

* KVM的实现中，在创建slot时，如果不想记录某个slot包含的所有物理页的是否为脏，需要默认将这些物理页对应的页表项的Dirty页置位，因为如果Dirty位是0，Guest态CPU写物理页时会将其置1并且填充GPA到PML Buffer，如果PML Buffer满了，就会触发VMExit，增加不必要的开销。反之，要记录脏页，首先需要将指向slot包含的所有物理页的spte的Dirty位清零，这里需要根据gfn找到指向该gfn对应页的spte，反向映射数组rmap就派上了用场。
物理页开启写保护：除了清零页表项的Dirty位，记录脏页还需要开启页的写保护，在脏页记录的过程中，所有slot包含的物理页变成只读，当CPU写访问这个页时，发生缺页异常，kvm会重新分配一个新的页给CPU。在脏页记录关闭后，才能将写保护去掉，slot包含的所有页变成可读写。

##### 步骤
1. qemu 初始化一个 bitmap 结构体 `migration_bitmap_rcu` 并set所有的solt 为1
2. qemu 将对内存页的标脏提交给 kvm 并调用 address_space_update_topology_pass
3. address_space_update_topology_pass 调用 log_start 将已经定义的 memory slot 增加 KVM_MEM_LOG_DIRTY_PAGES 的 flag，这一步就是内核标脏
3. kvm_create_dirty_bitmap kvm 初始化内存脏页 bitmap kvm_create_dirty_bitmap
4. qemu kvm 通过 migration_bitmap_sync 将内核脏页的 usersSpace 同步到 ram_list 结构体中
5. migration_bitmap_sync 将当前 ram_list 中的脏页 bitmap 拷贝到 migration_bitmap_rcu，这一步主要就是将kernal中的脏页同步回 qemu bitmap 结构体中
6. 通过对 migration_bitmap_rcu->bmap 的迭代，qemu将通过调用 ram_find_and_save_block 找到脏页并将脏页写入初始化的 fd

##### 简化步骤
1. qemu 初始化一个处于用户态的 bitmap 用于记录脏页，并set所有的solt 为1
2. qemu 初始化 RAMList 和 RAMBlock，分别用于存储虚拟机整个地址空间 kvmslot 和 用于表示单个脏页的 RAMBlock
3. qemu 将对内存页的标脏提交给 kvm
4. kvm 将已经定义的 memory slot 增加标脏的 flag，这一步就是内核标脏
5. qemu kvm中通过 kvm_vm_ioctl 获取内存脏页并同步到 RAMList和RAMBlock
6. 将当前 ram_list 中的脏页 bitmap 拷贝到 migration_bitmap_rcu，这一步主要就是将kernal中的脏页同步回 qemu bitmap 结构体中
7. 通过对 migration_bitmap_rcu->bmap 的迭代，qemu将通过调用 ram_find_and_save_block 找到脏页并将脏页写入初始化的 fd
8. 对已经完成拷贝的 block 进行清脏 KVM_CLEAR_DIRTY_LOG（一次拷贝完成，对端返回脏页数量）
9. 计算内存脏页率
10. 进行第二次拷贝


* 执行栈帧
```
(gdb) bt
#0  kvm_set_user_memory_region (kml=0x55ab8fc502c0, slot=0x55ab8fc50500) at /home/liqiang02/qemu0711/qemu-2.8/kvm-all.c:236
#1  0x000055ab8df10a92 in kvm_slot_update_flags (kml=0x55ab8fc502c0, mem=0x55ab8fc50500, mr=0x55ab8fd36f70)
    at /home/liqiang02/qemu0711/qemu-2.8/kvm-all.c:376
#2  0x000055ab8df10b1f in kvm_section_update_flags (kml=0x55ab8fc502c0, section=0x7f0ab37fb4c0)
    at /home/liqiang02/qemu0711/qemu-2.8/kvm-all.c:389
#3  0x000055ab8df10b65 in kvm_log_start (listener=0x55ab8fc502c0, section=0x7f0ab37fb4c0, old=0, new=4)
    at /home/liqiang02/qemu0711/qemu-2.8/kvm-all.c:404
#4  0x000055ab8df18b33 in address_space_update_topology_pass (as=0x55ab8ea21880 <address_space_memory>, old_view=0x7f0cc4118ca0, 
    new_view=0x7f0aa804d380, adding=true) at /home/liqiang02/qemu0711/qemu-2.8/memory.c:854
#5  0x000055ab8df18d9b in address_space_update_topology (as=0x55ab8ea21880 <address_space_memory>)
    at /home/liqiang02/qemu0711/qemu-2.8/memory.c:886
#6  0x000055ab8df18ed6 in memory_region_transaction_commit () at /home/liqiang02/qemu0711/qemu-2.8/memory.c:926
#7  0x000055ab8df1c9ef in memory_global_dirty_log_start () at /home/liqiang02/qemu0711/qemu-2.8/memory.c:2276
#8  0x000055ab8df30ce6 in ram_save_init_globals () at /home/liqiang02/qemu0711/qemu-2.8/migration/ram.c:1939
#9  0x000055ab8df30d36 in ram_save_setup (f=0x55ab90d874c0, opaque=0x0) at /home/liqiang02/qemu0711/qemu-2.8/migration/ram.c:1960
#10 0x000055ab8df3609a in qemu_savevm_state_begin (f=0x55ab90d874c0, params=0x55ab8ea0178c <current_migration+204>)
    at /home/liqiang02/qemu0711/qemu-2.8/migration/savevm.c:956
#11 0x000055ab8e25d9b8 in migration_thread (opaque=0x55ab8ea016c0 <current_migration>) at migration/migration.c:1829
#12 0x00007f0cda1fd494 in start_thread () from /lib/x86_64-linux-gnu/libpthread.so.0
#13 0x00007f0cd9f3facf in clone () from /lib/x86_64-linux-gnu/libc.so.6
```



### 4 - qemu 向 tcp sockets 中写入内存数据（迁移的控制层和实现层完全分开）
* 开始迁移内存，将内存数据拷贝到目的端（defaultpage size 4k）
* 发送内存数据到目的端，返回发送的内存页个数
* qemu每拷贝一次内存之前，会统计一次剩余的脏页数量，对比域值后决定是否一次性迁移
	* 脏页统计方法：dirtyrate = increased_memory / meaurement_time
	* 脏页速率越大，虚机内存变化越快，迁移时花费的时间就越多
	* 脏页统计率的统计过程和 dirty page tracking 类似，也是通过对内核中的脏页和qemu bitmap 之间的同步来计算增量
	* https://blog.csdn.net/huang987246510/article/details/118424717


* 内存发送和接收

```
   source                                destination

            +------------------------+             +-------------------------+
            |                        |             |                         |
  SETUP     | ram_save_setup         |             |  ram_load_setup         |
            |                        |             |                         |
            +------------------------+             +-------------------------+

            sync dirty bit to                      Setup RAMBlock->receivedmap
        RAMBlock->bmap


            +------------------------+             +-------------------------+
            |                        |             |                         |
  ITER      | ram_save_pending       |             |  ram_load               |
            | ram_save_iterate       |             |                         |
            |                        |             |                         |
            +------------------------+             +-------------------------+

            sync dirty bit                         Receive page
        and send page


            +------------------------+             +-------------------------+
            |                        |             |                         |
  COMP      | ram_save_pending       |             |  ram_load               |
            | ram_save_complete      |             |                         |
            |                        |             |                         |
            +------------------------+             +-------------------------+

            sync dirty bit                         Receive page
              and send page
```

### 5 - 迭代所有脏页，脏页达到一定的水平线
* TODO

### 6 - 暂停虚拟机（默认值30ms），一次性迁移剩余脏页
### 7 - 启动目的端vm



# 热迁移 downtime

## 什么是 downtime
* 脏页率达到指定阈值之后，暂停虚拟机，一次性迁移剩余脏页，并启动目的虚拟机的过程耗时
* 热迁移的停机时间（downtime）不是简单设置一个数字
* 迁移过程中的停机时间是变化的
* 不断增加，在一段时间后停机时间达到最终的最大值（用户态给定的最大值），这个值就是 live_migration_downtime


## 影响参数
* CONF.libvirt.live_migration_downtime
	* 最大值，手动配置、配置读取
	* downtime_steps 每个 Step 的 max downtime 都在递增直到真正用户设定的最大可容忍 downtime，
      这是因为 Nova 在不断的试探实际最小的 max downtime，尽可能早的进入退出状态。
* CONF.libvirt.live_migration_downtime_steps
	* 最大值，手动配置、配置读取
	* 一个元组表示一个 Step，分 Steps 次给 libvirtd 传输
* CONF.libvirt.live_migration_downtime_delay
	* 最大值，手动配置、配置读取
	* 下一次传递时间间隔

* downtime 通过上面一个算法得出：每次迭代都会重新计算虚拟机新的脏内存以及每次迭代所花掉的时间来估算带宽，再根据带宽和当前迭代的脏页数计算出传输剩余数据的时间
* 如果最后一次 libvirtd 迭代计算出来的 downtime 在传递的 downtime 范围内，则满足退出条件
* 自动收敛模式：如果虚拟机持续处于高业务状态，那么 libvirtd 会自动调整 vCPU 参数以减轻负载，达到降低脏内存的增长速度，从而保证 downtime 进入退出范围
* compute 中通过 migrateSetMaxDowntime 实现