# Date

- done

> plan to do


---
# 2019-11-23

- create the github repository

- change into `dev` branch

- start project server

- update django settings

---
# 2019-12-06

- fix settings

- test djcelery

---
# 2019-12-09

- drop djcelery: cannot run celery worker with python3.7

- use django-apscheduler

- admin a12345678

---
# 2019-12-10

- start app user, add model User, Teacher, Student

> urls `/user/login`, `/user/logout`

> render redirect, for set password and email while first logging in

> send email

> import teachers and students from file, set in another module `utils`

> verification codes, send number to email, put photo on website

---
# 2019-12-11
```
session = {
    "verify": "",
    "account": "",
    "identity": ""
    }
生成验证码照片在服务器，发送到网页

```