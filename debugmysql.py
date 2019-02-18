#! /usr/bin/env python

## 修正 数据库不能存储 emoji 表情符问题的脚本
### 1.数据库字符集格式必须为utf8mb4
### 2.django配置中的DATABASES下的 指定库配置OPTIONS 中增加 {'charset': 'utf8mb4'}
### 3.执行该脚本，因为不执行该脚本 之前的表格字符集不为utf8mb4 不能存储下传入的值

#!!! 该脚本执行于docker内

import os
import MySQLdb

DJANGO_LOCAL_SETTING = os.environ.get('DJANGO_LOCAL_SETTING', 'local')

host = None
passwd = None
user = 'root'
dbname = 'yuehu'
port = 3306

if DJANGO_LOCAL_SETTING == 'local':
    host = "mysql"
    passwd = "root"

elif DJANGO_LOCAL_SETTING == 'docker':
    host = "mysql"
    passwd = "nhdxs1bc"

elif DJANGO_LOCAL_SETTING == 'dev':
    host = os.environ.get("YUEHU_MYSQL_HOST", "mysql")
    port = int(os.environ.get("YUEHU_MYSQL_PORT", 3306))
    user = os.environ.get("YUEHU_MYSQL_USER", "root")
    passwd = os.environ.get("YUEHU_MYSQL_PWD", "")
else:
    print("error: please seeing annotation or code")

if host:
    db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=dbname, port=port)
    cursor = db.cursor()

    cursor.execute("ALTER DATABASE `%s` CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_unicode_ci'" % dbname)

    sql = "SELECT DISTINCT(table_name) FROM information_schema.columns WHERE table_schema = '%s'" % dbname
    cursor.execute(sql)

    results = cursor.fetchall()
    for row in results:
      sql = "ALTER TABLE `%s` convert to character set DEFAULT COLLATE DEFAULT" % (row[0])
      cursor.execute(sql)
    db.close()
    print("run: finish")
else:
    print("run: error")
