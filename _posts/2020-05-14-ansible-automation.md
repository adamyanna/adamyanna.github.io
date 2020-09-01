---
title: Ansible自动化
author: Teddy
date: 2020-05-14 15:24:57 +0800
categories: [体系结构-应用, 自动化]
tags: [Ansible, Yaml, Python]
---

# Ansible自动化

## 学习路径

* 理解Ansible架构
* 安装配置Ansible, Inventory
* 理解playbook的原理
* Ansible Ad-Hoc Commands
* Ansible 强大的模块
* Ansible playbook编写
* 掌握编写自己的 Roles
* 使用Ansible管理集群

## Ansible Architecture

![]({{ "/assets/img/posts/ansible-architecture.png" | relative_url }})

* 核心：ansible
* 核心模块（Core Modules）：这些都是ansible自带的模块 
* 扩展模块（Custom Modules）：如果核心模块不足以完成某种功能，可以添加扩展模块
* 插件（Plugins）：完成模块功能的补充
* 剧本（Playbooks）：ansible的任务配置文件，将多个任务定义在剧本中，由ansible自动执行
* 连接插件（Connection Plugins）：ansible基于连接插件连接到各个主机上，虽然ansible是使用ssh连接到各个主机的，但是它还支持其他的连接方法，所以需要有连接插件（centos下必须要安装sshpass）
* 主机群（Host Inventory）：定义ansible管理的主机

## Installation

### Ansible安装

```sh
yum -y install ansible

pip install ansible
```

### Ansible配置

```sh
inventory      = /etc/ansible/hosts
roles_path    = /etc/ansible/roles
log_path  = /var/log/ansible.log
remote_tmp     = ~/.ansible/tmp
local_tmp      = ~/.ansible/tmp

forks          = 5
sudo_user      = root
remote_port    = 22
timeout = 10
remote_user = root
```

## Ansible Usage

### Ansible命令

ansible一共为我们提供了七个指令：ansible、ansible-doc、ansible-galaxy、ansible-lint、ansible-playbook、ansible-pull、ansible-vault

1. ansible 
ansible是指令核心部分，其主要用于执行ad-hoc命令，即单条命令。默认后面需要跟主机和选项部分，默认不指定模块时，使用的是command模块。

2. ansible-doc
该指令用于查看模块文档信息，常用参数有两个-l 和 -s 

3. ansible-galaxy
ansible-galaxy 指令用于方便的从https://galaxy.ansible.com/ 站点下载第三方扩展模块

4. ansible-lint
ansible-lint是对playbook的语法进行检查的一个工具。用法是ansible-lintplaybook.yml 

5. ansible-playbook
调用playbook，通过读取playbook 文件后，执行相应的动作，最常用最核心的命令

6. ansible-pull
通过ansible-pull结合Git和crontab一并实现对大批量机器配置，其原理是通过crontab定期拉取指定的Git版本到本地，并以指定模式自动运行预先制订好的指令。

7. ansible-vault
ansible-vault主要应用于配置文件中含有敏感信息，又不希望他能被人看到，vault可以帮你加密/解密这个配置文件。主要对于playbooks里比如涉及到配置密码或其他变量时，可以通过该指令加密，这样我们通过cat看到的会是一个密码串类的文件，编辑的时候需要输入事先设定的密码才能打开。这种playbook文件在执行时，需要加上 –ask-vault-pass参数，同样需要输入密码后才能正常执行。


## Usage & Ad-Hoc

![]({{ "/assets/img/posts/ansible-usage.png" | relative_url }})


### Ad-Hoc命令集, 由 /usr/bin/ansible实现，其命令用法如下：

```sh
ansible <host-parttern> [options]

# 查看可用选项： ansible -h
```

### 常用选项：
```sh
-f forks：启动的并发线程数（默认值为5）
-m module_name: 指定要使用的模块
-a –args module_args: 模块特有的参数
-v verbose: 详情模式，显示所有debug信息
```

### Ad-Hoc Commands

```sh
ansible host -m service -a “name=pacemaker.service state=restarted

ansible host -m shell -a “systemctl status  pacemaker.service”
```

## Working with module

### ansible内置模块

```sh 
ansible-doc --list  #列出所有可用模块

ansible-doc shell   #查看模块说明
```

#### 常用模块
* command
* shell
* ping
* yum
* pip
* service
* template
* copy
* fetch
* file
* cron
* synchronize
* unarchive

![]({{ "/assets/img/posts/ansible-doc-shell.png" | relative_url }})

![]({{ "/assets/img/posts/ansible-doc.png" | relative_url }})

## Module

### Module调用方式

```sh
[root@controller]# ansible [group_name] -m service -a "name=httpd state=started“
[root@controller]# ansible [group_name] -m ping

- name: reboot the servers
  command: /sbin/reboot -t now
```
* 模块是在 Ansible 中实际在执行的.它们就是在每个 playbook 任务中被调用执行的.你也可以仅仅通过 ‘ansible’ 命令来运行它们.

* 每个模块都能接收参数. 几乎所有的模块都接受键值对(key=value)参数,空格分隔.一些模块不接收参数,只需在命令行输入相关的命令就能调用.

* 用ansible-doc [module]命令来查看你要使用的模块的文档       

## Woking with Inventory

```sh
[group names]
ip_1 ansible_ssh_user=‘’ ansible_ssh_pass=‘’
ip_2 ansible_ssh_user=‘’ ansible_ssh_pass=‘’

Hostname_1 ansible_ssh_host=${ip} ansible_ssh_user=‘’ ansible_ssh_pass=‘’
Hostname_2 ansible_ssh_host=${ip} ansible_ssh_user=‘’ ansible_ssh_pass=‘’

Example: 
[nsp]
szd-l0100875 ansible_ssh_host=127.0.0.1 ansible_ssh_user=root ansible_ssh_pass=‘root'
```

* Ansible 可同时操作属于一个组的多台主机,组和主机之间的关系通过 inventory 文件配置, 默认的文件路径为 /etc/ansible/hosts.

* 除默认文件外,你还可以同时使用多个 inventory 文件(-i 选项), 也可以从动态源, 或云上拉取 inventory 配置信息.


## playbooks

![]({{ "/assets/img/posts/ansible-playbooks.png" | relative_url }})

### 调用命令

```sh
ansible-playbook playbook.yml -f 10   （-f参数表示ansible主机并非进程数）
```

* 简单来说,playbooks 是一种简单的配置管理系统与多机器部署系统的基础.与现有的其他系统有不同之处,且非常适合于复杂应用的部署.

* Playbooks 可用于声明配置,更强大的地方在于,在 playbooks 中可以编排有序的执行过程,甚至于做到在多组机器间,来回有序的执行特别指定的步骤.并且可以同步或异步的发起任务.

* Playbooks 的格式是YAML, 语法做到最小化, 避免 playbooks 成为一种编程语言或是脚本,但它也并不是一个配置模型或过程的模型.


## YAML & Jinja2

### YAML 像 XML 或 JSON 是一种利于读写的数据格式，Ansible使用YAML 语法来描述一个 playbooks

* 所有的 YAML 文件(无论和 Ansible 有没有关系)开始行都应该是 ---. 这是 YAML 格式的一部分, 表明一个文件的开始.
* 对于 Ansible, 每一个 YAML 文件都是从一个列表开始. 列表中的每一项都是一个键值对, 通常它们被称为一个 “哈希” 或 “字典”. 
* 列表中的所有成员都开始于相同的缩进级别, 并且使用一个 "- " 作为开头(一个横杠和一个空格)
* 个字典是由一个简单的 键: 值 的形式组成(这个冒号后面必须是一个空格)

```yaml
---
- hosts: webservers
  vars:
    http_port: 80
    max_clients: 200
  remote_user: root
  tasks:
  - name: ensure apache is at the latest version
    yum: pkg=httpd state=latest
  - name: write the apache config file
    template: src=/srv/httpd.j2 dest=/etc/httpd.conf
    notify:
    - restart apache
  - name: ensure apache is running
    service: name=httpd state=started
  handlers:
    - name: restart apache
      service: name=httpd state=restarted
```

### jinja2是Flask作者开发的一个模板系统，起初是仿django模板的一个模板引擎，为Flask提供模板支持，由于其灵活，快速和安全等优点被广泛使用。

#### 作为一个模板系统，它还提供了特殊的语法，在jinja2中，存在三种语法：

* 控制结构

```yaml
\{\% \%\} #\用于markdown表示的转义
```

* 变量取值 

```yaml
\{\{ \}\} #\用于markdown表示的转义 
```

* 注释 

```yaml
\{\# \#\} #\用于markdown表示的转义
```

```
[keystone_authtoken]
auth_uri = http://keystone.mgt.domain:\{\{ keystone_mgt_port1 \}\}
auth_url = http://keystone.mgt.domain:\{\{ keystone_mgt_port2 \}\}
auth_plugin = password
project_domain_id = default
user_domain_id = default
project_name = service
username = neutron
password = neutron
identity_uri = http://127.0.0.1:5000
```


## Roles&Include

![]({{ "/assets/img/posts/ansible-roles.png" | relative_url }})


* 使用 include 语句引用 task 文件的方法，可允许你将一个配置策略分解到更小的文件中，方便文件复用.

* Role：通过 include 包含文件并将它们组合在一起，组织成一个简洁、可重用的抽象的对象.

* 在playbook中通过 roles: 来包含多个角色，然后顺序执行.


```sh
foo.yml
roles/
   role_foo/
     files/
     templates/
     tasks/
     handlers/
     vars/
     defaults/
     meta/
```

* 如果 roles/x/tasks/main.yml 存在, 其中列出的 tasks 将被添加到 play 中
* 如果 roles/x/handlers/main.yml 存在, 其中列出的 handlers 将被添加到 play 中
* 如果 roles/x/vars/main.yml 存在, 其中列出的 variables 将被添加到 play 中
* 如果 roles/x/meta/main.yml 存在, 其中列出的 “角色依赖” 将被添加到 roles 列表中 
* 所有 copy tasks 可以引用 roles/x/files/ 中的文件，不需要指明文件的路径。
* 所有 script tasks 可以引用 roles/x/files/ 中的脚本，不需要指明文件的路径。
* 所有 template tasks 可以引用 roles/x/templates/ 中的文件，不需要指明文件的路径。
* 所有 include tasks 可以引用 roles/x/tasks/ 中的文件，不需要指明文件的路径。


## Tags

```sh
[root@controller]# ansible-playbook example.yml --tags "step_1,step_2"

[root@controller]# ansible-playbook example.yml --skip-tags "step_11,step_12"
```

* Ansible 允许给playbook里面的资源通过自定义的关键字打上标签，然后只运行与标签部分的代码。
* Tags允许用户在一个playbook中，只运行部分task或跳过部分task。
* always, never, 是两个特殊的tag，always表示task总会执行，除非--skip-tags always；never表示总会跳过never下的task执行，如果此task还有其他tag，并且在—tags中包含，才会执行never的task。
* tags: tagged, untagged, all, 这三个tag在执行命令中可以使用，默认情况下ansible是默认运行 --tags all

## Var&Condition&Loop

```yaml
---
tasks:
  - name: "shutdown Debian systems"
    command: /sbin/shutdown -t now
    when: ansible_os_family == "Debian"

---
tasks:
  - name: run script
    shell: python script.py
    when: "'\{\{ node1_ip \}\}' in ansible_all_ipv4_addresses or '\{\{ node2_ip \}\}' in ansible_all_ipv4_addresses"        
    register: output
  - name: print output
    debug: msg="\{\{ output.stdout \}\}"
```

* Ansible使用 When 语句来控制执行流. 
* When 语句也可以应用于role 或 task 中的incloud语句
* 变量文件在playbook中指定，变量用“\{\{ \}\}”的形式导入，并且括号外要加引号
* 使用resigter将执行动作的输出，赋值给定义的变量

```yaml
- name: add several users
  user: name=\{\{ item \}\} state=present groups=wheel
  with_items:
     - testuser1
     - testuser2

- name: enable services
  service: name=\{\{ item.name \}\} state=\{\{ item.state \}\} enabled=\{\{ item.enabled \}\}
  with_items:
  - \{name: ntpd, state: restarted, enabled: yes\}
  - \{name: httpd, state: restarted, enabled: yes\}

Loop：
with_list
with_items
with_indexed_items
with_flattened
with_together
with_dict
with_sequence
with_subelements
with_nested/with_cartesian
with_random_choice
```

---

# END