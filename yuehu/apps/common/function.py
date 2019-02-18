# coding=utf-8

import re
import random
import math

from django.core.mail import BadHeaderError, EmailMultiAlternatives
from django.conf import settings
from django.db.models import QuerySet

from rest_framework.request import Request

from common import constant as common_constant

from helper.logs import get_logger

logger = get_logger(__name__)


def create_random_code(length=4, mode=common_constant.MODE1):
    """
        生成随机码（默认4位）
    :param length: 随机码长度
    :param mode: 随机码模式（1-7）
    :return:
    """
    if mode not in common_constant.CHARACTERS_LIST_DICT:
        raise IndexError(f"CHARACTERS_LIST_DICT not has [{mode}] key")

    code_slice = random.sample(common_constant.CHARACTERS_LIST_DICT.get(mode), length)

    random_code = "".join(code_slice)

    return random_code


def email_rightful(email):
    """
        验证电子邮箱的正确性
    :param email: 电子邮箱
    :return:
    """

    try:
        email = str(email)
        query = re.search(common_constant.EMAIL_RE, email)
        if not query:
            return False, None
        email = query.group(0)
    except (IndexError, AttributeError) as e:
        logger.error(e)
        return False, email
    except Exception as e:
        logger.error(e)
        logger.error(email)
        return False, email

    return True, email


def send_email_format_html(subject, message, address_email_list: list):
    """
        发送html页面的电子邮件
    :param subject: 主题
    :param message: 内容
    :param address_email_list: 邮件列表
    :return: 是否成功
    """
    try:
        ema = EmailMultiAlternatives(subject, message, settings.DEFAULT_FROM_EMAIL, address_email_list)
        ema.attach_alternative(message, "text/html")
        ema.send()
    except BadHeaderError:
        return False
    except Exception as e:
        logger.error(e)
        return False
    else:
        return True


def send_email_admin_format_html(subject, message):
    """
        发送html页面的电子邮件给管理员
    :param subject: 主题
    :param message: 内容
    :return: 是否成功
    """
    try:
        ema = EmailMultiAlternatives(subject, message, settings.DEFAULT_FROM_EMAIL, settings.PYTHON_DOG_ADMIN_EMAIL_LIST)
        ema.attach_alternative(message, "text/html")
        ema.send()
    except BadHeaderError:
        return False
    except Exception as e:
        logger.error(e)
        return False
    else:
        return True



def request_objects_pagination(request: Request, query_set: QuerySet, serializer_cls):
    """
        查询对象集根据request分页
    :param request: Request 请求对象(GET请求)
    :param query_set: Django 查询对象集
    :param serializer_cls: 继承ModelSerializer的序列化类
    :return: (page_query_set: QuerySet, page_info: dict)
    """

    # 默认认为请求为GET
    page = request.GET.get("page", 1)
    one_page_max = request.GET.get("limit", common_constant.DEFAULT_ONE_PAGE_MAX)

    # 页数为不合法的值时要将其置为默认值 (default:1)
    try:
        page = int(page)
    except (ValueError, TypeError):
        page = 1

    # 这里分开写两个try 是防止one_page_max 异常而导致page一直为默认值 是值得写两个的
    try:
        one_page_max = int(one_page_max)
    except (ValueError, TypeError):
        one_page_max = common_constant.DEFAULT_ONE_PAGE_MAX

    #  解序列
    page_query_set, item_sum, (page_sum, page, one_page_max) = page_objects_pagination(page, query_set, one_page_max)

    page_info = {
        "page_sum": page_sum,
        "page": page,
        "limit": one_page_max,
        "item_sum": item_sum,
        "query_set": serializer_cls(page_query_set, many=True).data
    }

    return page_info


def page_objects_pagination(page: int, query_set: QuerySet, one_page_max: int=common_constant.DEFAULT_ONE_PAGE_MAX):
    """
        查询对象集根据当前页page分页
    :param page: 当前页
    :param query_set: Django 查询对象集
    :param one_page_max: 单页的最大数量
    :return: (page_query_set, item_sum, *args)  [*args=page_sum, page, one_page_max]
    """

    item_sum = query_set.count()
    item_start, item_end, *args = pagination(item_sum, page, one_page_max)
    page_query_set = query_set[item_start: item_end]
    return page_query_set, item_sum, args


def pagination(item_sum: int, page: int, one_page_max: int=common_constant.DEFAULT_ONE_PAGE_MAX):
    """
        计算分页
    :param item_sum: 项目总数
    :param page: 当前页
    :param one_page_max: 单页的最大数量
    :return: (item_start, item_end, page_sum, page, one_page_max)
    """

    # 为什么不在这里纠正参数类型错误？
    # 我认为pagination函数为最基础的分页函数，不应该关心纠正传入类型，而要做的是在参数类型错误时报错就好了，纠正类型应该在传入前就做好！
    if [o for o in [item_sum, page, one_page_max] if not isinstance(o, int)]:
        raise TypeError("Fun(Pagination): param value isn't [Int]")

    # 纠正参数数值范围
    if 1 > one_page_max or one_page_max > common_constant.MAX_ONE_PAGE_MAX:
        one_page_max = common_constant.DEFAULT_ONE_PAGE_MAX

    page_sum = math.ceil(item_sum/one_page_max)
    page_sum = page_sum if page_sum > 0 else 1

    if 1 > page:
        page = 1
    elif page > page_sum:
        page = page_sum

    _end = page * one_page_max
    _start = _end - one_page_max

    return _start, _end, page_sum, page, one_page_max


def fuzzy_real_email(email):
    """
        模糊真实邮箱
    :param email:
    :return:
    """
    index = email.index("@")

    head_show_number = 3 if index > 8 else 2
    end_show_number = head_show_number - 1

    return email[:head_show_number] + '*' * (index - end_show_number - head_show_number) + email[index - end_show_number:]
