# coding=utf-8

import re
import string

from datetime import timedelta, timezone

# 各种字符组合集
CHARACTERS_LIST_DICT = dict()

# 小写字母集
MODE1 = "mode1"
CHARACTERS_LIST_DICT[MODE1] = CHARACTERS1_LIST = list(string.ascii_letters)

# 大写字母集
MODE2 = "mode2"
CHARACTERS_LIST_DICT[MODE2] = CHARACTERS2_LIST = list(string.ascii_uppercase)

# 数字集
MODE3 = "mode3"
CHARACTERS_LIST_DICT[MODE3] = CHARACTERS3_LIST = list(string.digits)

# 小写字母与数字集
MODE4 = "mode4"
CHARACTERS_LIST_DICT[MODE4] = CHARACTERS4_LIST = list(string.ascii_letters + string.digits)

# 大写字母与数字集
MODE5 = "mode5"
CHARACTERS_LIST_DICT[MODE5] = CHARACTERS5_LIST = list(string.ascii_uppercase + string.digits)

# 大小写字母集
MODE6 = "mode6"
CHARACTERS_LIST_DICT[MODE6] = CHARACTERS6_LIST = list(string.ascii_letters + string.ascii_uppercase)

# 大小写字母与数字集
MODE7 = "mode7"
CHARACTERS_LIST_DICT[MODE7] = CHARACTERS7_LIST = list(string.ascii_letters + string.ascii_uppercase + string.digits)

# 大小写字母与数字以及特殊符号集
MODE8 = "mode8"
CHARACTERS_LIST_DICT[MODE8] = CHARACTERS8_LIST = list(string.ascii_letters + string.ascii_uppercase + string.digits +
                                                      "@#$%^&*-_")

# 邮箱验证正则
EMAIL_RE = re.compile(r"^([a-zA-Z0-9_\.-])+@([a-zA-Z0-9_-])+\.([a-zA-Z0-9\.])+$")

# 分页中单页最大数的默认值
DEFAULT_ONE_PAGE_MAX = 10

# 分页中单页最大数的最大值
MAX_ONE_PAGE_MAX = 31

# 统计 COOKIES 存储时长

COOKIES_SID_DAYS = 365
COOKIES_BID_DAYS = 365
COOKIES_OID_DAYS = 30


# UTC+8时区(北京)
TZ_UTC_8 = timezone(timedelta(hours=8))