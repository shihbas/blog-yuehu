# coding=utf-8

from common import common_api, common_validate

# 前台api装饰器
api_common = common_api(t="api", v="1.0")

# 后台api装饰器
cms_common = common_api(t="cms", v="1.0")
