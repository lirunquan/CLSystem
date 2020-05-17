# 《C语言程序设计》课程学习系统

## 搭建环境
- 操作系统\
	Ubuntu 16.04\
	安装以下包：
	```
	build-essential
	gcc
	libseccomp2
	libseccomp-dev
	cmake
	nginx
	```
- 开发语言\
	Python 3.7.1\
	安装模块:
	```
	pip install -r requirements.txt
	```
- 数据库
	MySQL 5.7

## 运行调试(root用户下进行)
- 克隆代码
	```
	git clone https://github.com/lirunquan/CLSystem.git
	```
- 导入数据库
	```
	# mysql -u root -p
	mysql> create database CLSystem default character set utf8;
	mysql> use CLSystem;
	mysql> source /path/to/CLSystem/CLSystem.sql
	```
	验证是否导入成功
	```
	# mysql -u root -p
	msyql> use CLSystem;
	mysql> show tables;
	```
	数据库内有`auth_user` `django_migrations` `django_session`等表则说明导入成功。
- 运行测试
	```
	# cd CLSystem/server
	# chmod a+x run.sh
	# ./run.sh
	```
	
