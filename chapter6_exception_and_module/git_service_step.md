# 搭Gogs私服 
项目不同时期使用了不同python版本开发，假如要回到之前的某一个版本怎么办。又或者很多人同时开发一个项目，避免代码冲突、覆盖。所以需要版本管理，版本管理-即快照，以下记录搭gogs版本管理服务器。  

## 所需资源：
需要Mysql。一般用rpm安装，或者用二进制发行版。  
比较流行的Mysql版本：Percona-Server***.tar。安装方式：至少安装shared、client、Server，且按shared -> client -> Server顺序安装：  
Percona-Server***.tar安装博客参考：https://blog.csdn.net/m0_37461645/article/details/83116326

### 1、安装完：
`ss-tanl` 查看端口监听，mysql端口3306  
`ls /etc/init.d/my*` 查看装上没有(名字：mysql）  
启动、停止：`service mysql start/stop`  

### 2、启动并设置环境
启动之前cmd命令行执行`/usr/bin/mysql_secure_installation`，测试mysql服务起来没有，并设置基本环境。执行时，报ERROR***/mysql.sock时，表示mysql服务没起来。  

`/usr/bin/mysql_secure_installation`：设置root密码、要不要匿名用户anonymous、允不允许root密码远程登录(一般允许，方便windows登录)等等。  

### 3、进入mysql服务后：
执行 show databases；
# Todo
