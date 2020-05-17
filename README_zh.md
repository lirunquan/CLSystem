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
	安装系统所需模块:
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
	验证是否导入成功：
	```
	# mysql -u root -p
	msyql> use CLSystem;
	mysql> show tables;
	```
	数据库内有`auth_user` `django_migrations` `django_session`等表则说明导入成功。
- 安装Judger模块
	```
	# cd CLSystem/Judger/bindings/Python
	# sudo python setup.py install
	```
	测试是否安装成功：
	```
	# python
	>>> import _judger
	>>> _judger.VERSION
	```
	没有报错，能看到输出即安装成功。
- 系统设置
	在`CLSystem/server/server/settings.py`中根据实际情况进行设置。
	```
	# Database
	# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
	# Database using MySQL
	pymysql.install_as_MySQLdb()
	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.mysql',
	        'NAME': 'CLSystem',
	        'USER': 'root',
	        'PASSWORD': '1234567890', # 系统以root用户启动MySQL的密码
	        'HOST': 'localhost',
	        'PORT': '3306'
	    }
	}
	```
	```
	# Email Settings
	EMAIL_USE_SSL = True
	EMAIL_HOST = 'smtp.163.com'
	EMAIL_PORT = 465
	EMAIL_HOST_USER = '15813388007@163.com' # 可根据实际情况改为公共邮箱
	EMAIL_HOST_PASSWORD = 'liruner9576' # 邮箱登录密码
	DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
	EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
	```
	```
	# Host 
	SERVER_HOST = "http://192.168.2.112:10086" # 改为服务器的IP地址以及启动的端口
	```
- 运行测试
	运行`run.sh`脚本即可启动调试，默认端口为10086。
	```
	# cd CLSystem/server
	# chmod a+x run.sh
	# ./run.sh
	```
	打开浏览器输入地址`服务器ip:10086`，显示系统页面即运行成功。
- nginx+uwsgi部署
	复制`nginx.conf`到系统目录下，重启nginx服务，然后通过uwsgi启动系统
	```
	# cd CLSystem/server
	# cp nginx.conf /etc/nginx/conf.d/
	# service nginx restart
	# uwsgi --ini uwsgi.ini
	```
	打开浏览器输入地址`服务器ip:10086`，显示系统页面即运行成功。