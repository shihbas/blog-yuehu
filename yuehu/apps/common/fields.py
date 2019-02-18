# coding=utf-8

from datetime import datetime

from common.constant import TZ_UTC_8

def datetime_str_fmt(datetime_str):
    """
        datetime的字符串转换为Datetime类型
    :param datetime_str: %Y-%m-%d %H:%M:%S 样式字段
    :return:
    """
    return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')


def datetime_str_fmt_utc8(datetime_str):
    """
        datetime的字符串转换为带 UTC+8 时区的 Datetime 类型
    :param datetime_str: %Y-%m-%d %H:%M:%S 样式字段
    :return:
    """
    return datetime_str_fmt(datetime_str).replace(tzinfo=TZ_UTC_8)


def date_str_fmt(datetime_str):
    """
        datetime的字符串转换为Date类型
    :param datetime_str: %Y-%m-%d %H:%M:%S 样式字段
    :return:
    """
    return datetime.strptime(datetime_str, '%Y-%m-%d').date()
