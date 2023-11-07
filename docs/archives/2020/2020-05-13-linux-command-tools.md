---
title: Linux常用工具&内置命令
layout: default
parent: 2020
grand_parent: Archives
---

**Linux**
{: .label .label-blue }

**2020-05-13 17:17:18 +0800**
{: .label .label-yellow }


# Linux常用工具&内置命令

# Linux 工具箱

## I. 常用工具命令

###### 按路径检查磁盘利用率

```
NAME
du - estimate file space usage

USAGE
du -h --max-depth 1 | sort -hr
```



###### 快速杀掉某程序所有进程

```
ps -ef | grep {NAME} | awk -F ' ' '{ print $2}' | xargs kill -9
```



###### 清除DNS缓存

```
nscd -g  #查看统计信息

nscd -i passwd
nscd -i group
nscd -i hosts

rm -f /var/db/nscd/hosts
service nscd restart

#修改 /etc/nscd.conf
enable-cache hosts yes
```



###### sublime 反相匹配    

```
^(?!.*InstanceId).+
```



###### python 正则表达式反向

| 匹配符（...代表匹配内容） | 描述                                                      |
| ------------------------- | :-------------------------------------------------------- |
| (?!.*...)                 | 字符内容不匹配才能匹配成功                                |
| [...]                     | 匹配字符集，例如只匹配空格和制表符，不能使用\s，而是[\t ] |

![python re]()



###### find 高级查询

```
find ../ -type f -name "*.py[co]" -delete
find /（查找范围） -name '查找关键字' -type d
```
