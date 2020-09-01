---
title: Python服务容器化部署
author: Teddy
date: 2020-05-14 15:03:28 +0800
categories: [实践, 需求实现]
tags: [Python, Docker]
---


# 监控容器微服务部署

###### 新增节点初始化操作

* 0. 下载Docker环境部署文件，上传到物理机
* 将以上文件上传至同一目录下，执行如下：
* 1. 准备日志
* 2. 准备应用文件
* Step0：获取监控物理机信息
* Step1：初始化配置监控主机
* Step2：部署+验证

###### nmsagent镜像部署

* 0. 下载Docker环境部署文件，上传到物理机
* 1. 安装docker
* 2. 导入镜像, 必须在两台物理机上都执行
* 3. 准备日志
* 4. 准备应用文件
* 5. 部署nspmonitor-xxx.tar.gz,准备docker服务所需文件及虚环境安装lvxmonitor-engine到nginx物理机,以EFA为例子
* 6. 部署服务 - 部署nspmonitor和lvxmonitor-porxy的Docker服务
* 更新yunzhi环境信息
* Debug
* 采用docker三节点HA部署

###### 新增节点初始化操作
```sh
#允许root ssh登录修改：
vi /etc/ssh/sshd_config 
PermitRootLogin no修改为：PermitRootLogin yes
#重启sshd服务
service sshd restart
```

1. nspmonitor验证配置文件所有IP:PORT是否能够访问,alphaops验证hillstone防火墙snmpwalk和22端口

```sh
 snmp安装：
yum install -y net-snmp net-snmp-utils
 alphaops验证
```
 
2. 执行以下步骤：Step1
3. 上传镜像文件，初始化docker环境

0. 下载Docker环境部署文件，上传到物理机

[init_docker_node.sh](http://code.test.com.cn/#/repo/test-monitor/docker-images/master/blob/docker_ce_18%2Fdocker-centos7.2-install_scripts%2Finit_docker_node.sh)
[镜像包net_monitor_add_ssh.tar.tar](http://code.test.com.cn/#/repo/test-monitor/docker-images/master/blob/netmonitor_image%2Fnet_monitor_add_ssh.tar)
[下载最新版本的nspmonitor-xxx.tar.gz](http://127.0.0.1/network_group/nspmonitor/origin/release/)
[docker-package.tar.gz](http://code.test.com.cn/#/repo/test-monitor/docker-images/master/blob/docker_ce_18%2Fdocker-package.tar.gz)

将以上文件上传至同一目录下，执行如下：

```sh
bash init_docker_node.sh

注意：如果执行以上脚本出错，把内容复制出来，命令逐行执行
#检查镜像是否导入
docker images
```

1. 准备日志

```sh
mkdir -p /var/log/nspmonitor
vim /etc/logrotate.d/nspmonitor
# 将下面的文本粘贴到 /etc/logrotate.d/nspmonitor 该文件中
/var/log/nspmonitor/*.log {
    rotate 10
    size 50M
    missingok
    compress
    copytruncate
}
mkdir -p /var/log/lvxmonitor
vim /etc/logrotate.d/lvxmonitor
# 将下面的文本粘贴到 /etc/logrotate.d/lvxmonitor 该文件中
/var/log/lvxmonitor/*.log {
    rotate 10
    size 50M
    missingok
    compress
    copytruncate
}
```

2. 准备应用文件
* 创建目录

```sh
mkdir -p /opt/netmon/agent
```

* 解压agent_updater文件并移动到agent下

```sh
tar -zxvf nspmonitor-xxx.tar.gz -C /opt/netmon/agent
cp /opt/netmon/agentnspmonitor-xxx/nspmonitor /opt/netmon/agent -r
```
  
    
###### Step0：获取监控物理机信息

* 监控主机为双机高可用模式

###### Step1：初始化配置监控主机

* 修改ulimit linux系统对用户态程序限制

```sh
# 查看 open files 的限制数量
ulimit -a
# 永久修改：
vim /etc/security/limits.conf
* - nproc 102400
* - nofile 102400
# 修改max-file
vim /etc/sysctl.conf
fs.file-max = 6815744
# 最好对系统进行reboot
reboot
```

* 配置NTP服务器，并启动NTP时间同步服务，检查时间是否为UTC+8（不同地域可用区不同）

```sh
systemctl status ntpd
ntptime
# 参考AZ NSP的 /etc/ntp.conf ntp配置，拷贝到监控物理机
systemctl restart ntpd
ntptime #检查时间是否同步UTC+8（不同地域可用区不同）
# 如果服务没有启动或者时间不对，需要修改/etc/ntp.conf 配置文件，将server修改为该区域可用的ntp server，并启动服务
```

* 配置域名解析服务

```sh
cat /etc/resolv.conf
search cloud.pub
nameserver 127.0.0.1
nameserver 127.0.0.1
 
# 检查域名是否解析，网络是否可达
ping gateway-OpenFalcon.cloud.pub
telnet gateway-OpenFalcon.cloud.pub 12057
```

* 检查Open-Falcon的agent是否安装，端口是否监听

```sh
# 检查端口是否监听
netstat -antl | grep 12050
# 检查应用是否部署并启动
ps -aux | grep falcon
ps -aux | grep ops_updater
# falcon-agent进程不存在，或目录/opt/pamon/不存在
# 进入 http://fcloud.test.com.cn/d/9a0876f347/ 联系文件提供人，下载并安装
# 若OpenFalcon-agent未安装，请根据主机类型（传统环境/内部云/公有云）按照以下流程安装：
# http://yunzhi.test.com.cn/pages/viewpage.action?pageId=24564124
```

* YUM配置
* yum clean all && yum makecache  \# 如果不发生报错，则YUM配置可用，报错请继续
* 配置路径：/etc/yum.repos.d/ 对应.repo文件可以到AZ NSP物理机相同路径复制到本机目录
* 完成/etc/yum.repos.d/\*.repo 文件配置后 yum clean all && yum makecache 进行验证
* 修改主机密码
* passwd root 改为网络组新密码

###### Step2：部署+验证

nmsagent镜像部署
说明：
下面的安装步骤中 0,1,2,3 必须在两台物理机都进行操作
下面的安装步骤中 4,5,6 只需要在一台物理机都进行操作
0. 下载Docker环境部署文件，上传到物理机

```sh
add_manager.sh
install.sh
docker-package.tar.gz
net_monitor_add_ssh.tar
```

下载最新版本的nspmonitor-xxx.tar.gz
下载最新版本的agent_updater-xxx.tar.gz


1. 安装docker
* 将下面三个文件放置在同一级目录下

```sh
add_manager.sh
install.sh
docker-package.tar.gz
```

* 安装主节点

```sh
bash install.sh <ip> #此ip为两台物理机中任意一台, 安装完成后会显示 --token xxxx ip:port, 复制--token后面的内容
```

* 添加管理节点

```sh
bash add_manager.sh xxxx ip:port #将复制的--token之后的内容加在add_manager.sh后
```

* 检查集群状态

```sh
docker node ls
```

2. 导入镜像, 必须在两台物理机上都执行
* 将上传的net_monitor_add_ssh.tar文件导入为docker image, 命名为netmonitor，版本为1.0

```sh
docker import net_monitor_add_ssh.tar netmonitor:v1.0
```

3. 准备日志

```sh
mkdir -p /var/log/nspmonitor
vim /etc/logrotate.d/nspmonitor
# 将下面的文本粘贴到 /etc/logrotate.d/nspmonitor 该文件中
/var/log/nspmonitor/*.log {
    rotate 10
    size 50M
    missingok
    compress
    copytruncate
}
mkdir -p /var/log/lvxmonitor
vim /etc/logrotate.d/lvxmonitor
# 将下面的文本粘贴到 /etc/logrotate.d/lvxmonitor 该文件中
/var/log/lvxmonitor/*.log {
    rotate 10
    size 50M
    missingok
    compress
    copytruncate
}
```

4. 准备应用文件

* 创建目录

```sh
mkdir -p /opt/netmon/agent
```

* 解压agent_updater文件并移动到agent下

```sh
tar -zxvf agent_updater-xxx.tar.gz -C /opt/netmon/agent
```

* 到agent_updater内创建新的{可用区名称}配置文件夹, 以EFA为例子

```sh
mkdir /opt/netmon/agent/agent_updater/updater/config/EFA/
cp /opt/netmon/agent/agent_updater/updater/config/SCA/config.json /opt/netmon/agent/agent_updater/updater/config/EFA/  #拷贝SCA的配置文件为模版
vim /opt/netmon/agent/agent_updater/updater/config/EFA/config.json # 修改监控物理机ip，nginx物理机ip，密码也需要统一
```

5. 部署nspmonitor-xxx.tar.gz,准备docker服务所需文件及虚环境安装lvxmonitor-engine到nginx物理机,以EFA为例子

```sh
cp <上传路径>/nspmonitor-xxx.tar.gz /opt/netmon/agent/agent_updater/package
cd /opt/netmon/agent/agent_updater/updater

# ansible command not found 的情况下，需要安装ansible
cd /opt/netmon/agent/agent_updater/ansible/playbooks/init
python init.py

python updater.py EFA ansible # 以EFA为例子,检查部署结果
```

6. 部署服务 - 部署nspmonitor和lvxmonitor-porxy的Docker服务
* 修改服务compose文件, 修改文件中的可用区名称，例如：把所有的"SCA"替换为"EFA"

```sh
cd /opt/netmon/agent/agent_updater/package/nspmonitor-{1.2.5.dev57}/docker-compose/
# File use vim 修改可用区 line：20
-rwxr-xr-x 1 root root 691 Jul 31 00:59 lvxmonitor-proxy-compose.yml
-rwxr-xr-x 1 root root 687 Jul 31 01:07 nspmonitor-compose.yml
-rwxr-xr-x 1 root root 689 Jul 31 01:08 pagwmonitor-compose.yml
```

* config 文件配置，如果不存在下面两个配置文件或路径，请联系监控开发在代码仓库中添加，并提供最新的nspmonitor的包

```sh
/opt/netmon/agent/nspmonitor/etc/<可用区>/nspmonitor.ini
# 参考TEMPLATE中做修改
/opt/netmon/agent/nspmonitor/etc/<可用区>/lvxmonitor_proxy.conf
# 找到scan_ips， 将scan_ips后的ip改为Nginx物理机ip，以逗号分隔；
```

* 配置修改完成，重新同步代码

```sh
cd /opt/netmon/agent/
scp -r nspmonitor <agent_ip>:/opt/netmon/agent  # 以EFA为例子,检查部署结果,这里的agentip为另一台没有进行操作的主机ip
```

* Deploy

```sh
cd /opt/netmon/agent/agent_updater/package/nspmonitor-{1.2.5.dev57}/docker-compose/
docker stack deploy -c <compose_file>.yml <service_name>
#　对应名称
# compose_file: lvxmonitor-proxy-compose.yml service_name: lvxmonitor_proxy_EFA
# compose_file: nspmonitor-compose.yml service_name: nspmonitor_EFA
# compose_file: pagwmonitor-compose.yml service_name: pagwmonitor_EFA  # 对于没有PAGW（vpp）产品的可用区请不要部署该微服务
```

* 检查服务情况，查看当前服务是否成功启动，是否处于running状态

```sh
ansible lvx_monitor_engine -m shell -a "systemctl status lvxmonitor-engine.service" --inventory-file=/opt/netmon/agent/agent_updater/ansible/hosts
docker service ls
docker service ps <service_name>
```

* 检查日志

```sh
/var/log/nspmonitor # 在此目录下tail -f和tail -f | grep ERROR 检查日志是否有打印，检查是否有大量报错
更新yunzhi环境信息
NFV环境信息
Debug
# run a test container as TESTPOD
docker run -i -t -d --network=host -v /opt/netmon/:/app -v /var/log/:/var/log/ -v /etc/localtime:/etc/localtime --name TESTPOD netmonitor:v1.0 /bin/bash

# start debug process
# removing --log-file config app will output log directly to console
# add the '&' to the end of execute command will run this process as linux deamon
/usr/bin/python /app/agent/nspmonitor/agent/nginx/proxy.py --config-file=/app/agent/nspmonitor/etc/SCA/lvxmonitor_proxy.conf --log-file=/var/log/nspmonitor/proxy.log
/usr/bin/python /app/agent/nspmonitor/agent/nsp/entry.py --config-file=/app/agent/nspmonitor/etc/SCA/nspmonitor.ini --log-file=/var/log/nspmonitor/nspmonitor.log
/usr/bin/python /app/agent/nspmonitor/agent/pagw/entry.py --config-file=/app/agent/nspmonitor/etc/EFA/nspmonitor.ini --log-file=/var/log/nspmonitor/pagwmonitor.log
```


##### nspmonitor版本更新操作
1. 将nspmonitor_xxxx.tar.gz 拷贝至 /opt/netmon/agent/下
2. 解压：tar -xvf nspmonitor_xxxx.tar.gz ,cp nspmonitor_xxxx/nspmonitor /opt/netmon/agent/ -r
3. 重启服务 docker service update nspmonitor_agent –force
4. 验证进程是否拉起 docker service ps nspmonitor_agent –no-trunc
以及查看日志：tail /var/log/nspmonitor/nspmonitor.log
采用docker三节点HA部署
1. 新节点环境配置

```sh
#根据以上step 0，1，2步骤将新节点配置好
# step0 全部执行
# step1 全部执行
# step2 执行1，2，3步骤
```
 
 
```sh
# 准备应用文件
 
## 创建目录
 
mkdir -p /opt/netmon/agent
 
## 解压nspmonitor-xxx.tar.gz 文件并移动到agent下
 
tar -zxvf nspmonitor-xxx.tar.gz -C /opt/netmon/agent
cp /opt/netmon/agent/nspmonitor-xxx/nspmonitor /opt/netmon/agent
2.删除原二节点集群

# 删除服务，其中一个节点执行即可
dockers service ls
docker service rm （服务名称） --force
 
 
# 删除集群，两个节点
docker node ls
docker node rm --force （节点名称）
3.创建三节点新集群

#找其中一个节点先作为manager
docker swarm init --advertise-addr (ip)
 
 
#另外两个节点加入集群
docker swarm join --token (token) ip:port
#manager节点上执行，将两个worker节点升级为manager
docker node ls
docker promode (节点名称)
变更文档
#原节点执行，复制token
docker swarm join-token manager
#新加节点执行复制token内容
docker swarm join --token （token str）ip:port
 
 
 
 
其它方案
 
 
# 1.1 删除服务，其中一个节点执行即可
dockers service ls
docker service rm （服务名称） --force
 
 
# 1.2 删除集群，两个节点
docker node ls
docker node demote （节点名称）
docker node rm --force （节点名称）
 
 
# 2.1 找其中一个节点先作为manager
docker swarm init --advertise-addr (ip)
 
 
# 2.2另外两个节点加入集群
docker swarm join --token (token) ip:port
# 2.3manager节点上执行，将两个worker节点升级为manager
docker node ls
docker promode (节点名称)
 
 
# 回滚
docker node ls
docker node rm --force （节点名称）
docker swarm init --advertise-addr (ip)
docker swarm join --token (token) ip:port
docker stack deploy -c nspmonitor-compose.yml  nspmonitor
```
