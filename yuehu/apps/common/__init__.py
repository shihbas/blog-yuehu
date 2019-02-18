# coding=utf-8

import functools

from inspect import isfunction

from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request

from common.exceptions import LogicException, ValidateException

from helper.logs import get_logger

logger = get_logger(__name__)


def common_api(**ca_kw):
    """
        api接口统一装饰器，为规范代码
    :param ca_kw: 预留参数
    :return:
    """

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            api_type = ca_kw.get("t")
            api_version = ca_kw.get("v")

            try:
                response = func(*args, **kwargs)

                data = {
                    "data": response.data,
                    "code": "ok",
                    "message": "",
                    "version": api_version,
                    "type": api_type
                }
                response.data = data
                return response
            except (LogicException, ValidateException) as e:
                data = {
                    "data": "",
                    "code": e.code,
                    "message": e.msg,
                    "version": api_version,
                    "type": api_type
                }
                return Response(data=data, status=status.HTTP_200_OK)

        return wrapper

    return decorator


def common_validate(**cv_kw):

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            request = args[0] if isinstance(args[0], Request) else args[1]

            if request.method in ('GET', 'DELETE'):
                params = request.GET.copy()
            elif request.method in ('POST', 'PUT'):
                params = request.data
            else:
                raise LogicException('request请求类型错误')

            # 普通校验必填项 required_fields = ['a', 'b']
            required_fields_list = cv_kw.get("required_fields", None)
            if required_fields_list:
                null_field_list = []
                for item in required_fields_list:
                    if item not in params:
                        null_field_list.append(item)
                        continue
                    if isinstance(params[item], int):
                        continue
                    if not bool(params[item]):
                        null_field_list.append(item)

                if len(null_field_list) > 0:
                    ve = ValidateException()
                    ve.add_fields_null(null_field_list)
                    raise ve

            # 转换为指定类型 type_fields = {'a': int, 'b': (str, 'default')}
            type_field_dict = cv_kw.get("type_fields", None)
            if type_field_dict:
                for k, v in type_field_dict.items():
                    has_default = False
                    default = None

                    if isinstance(v, tuple):
                        default = v[1]
                        v_type = v[0]
                        has_default = True
                    else:
                        v_type = v

                    try:
                        if v_type is bool and not isinstance(params.get(k), int):
                            raise LogicException(f'{k}字段为bool类型，应输入0或1来设置该值')

                        # TODO: 这里不知道应该怎么才是最好的 函数与类型都可以直接 f(o) 将 o 改变为指定类型
                        # if isfunction(v_type):
                        #     params[k] = v_type(params.get(k))
                        params[k] = v_type(params.get(k))
                    except (TypeError, ValueError):
                        if has_default:
                            params[k] = default
                        else:
                            raise LogicException(f'{k}字段的类型错误，请校验')

            # TODO: 可增加多种校验类型 之后再慢慢添加
            # 校验逻辑 type_fields = {'a': func, 'b': (func, 'error_text')}
            logic_filed_dict = cv_kw.get("logic_fields", None)
            if logic_filed_dict:
                for k, v in logic_filed_dict.items():
                    if k not in params:
                        raise LogicException(f'{k}字段不存在于请求中')
                    if isinstance(v, tuple):
                        error_text = v[1]
                        _func = v[0]
                    else:
                        _func = v
                        error_text = '逻辑错误'
                    try:
                        logic_result = _func(params[k])
                    except Exception as e:
                        logger.error(e)
                        raise LogicException(f'{k}字段不合法，无法通过逻辑校验')
                    else:
                        if not logic_result:
                            raise LogicException(f'{k}字段校验错误:{error_text}')

            if request.method in ('GET', 'DELETE'):
                request.GET = params

            return func(*args, **kwargs)

        return wrapper

    return decorator
