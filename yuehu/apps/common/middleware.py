# coding=utf-8

import uuid

from datetime import datetime, timedelta

from django.utils.deprecation import MiddlewareMixin

from common import constant as common_constant

from account.models import User


class UserVisitMiddleware(MiddlewareMixin):


    def process_response(self, request, response):
        """
            用作用户统计
        :param request:
        :param response:
        :return:
        """

        # session id 每次访问的唯一凭证
        s_id = request.session.get("YH_SID", None)

        if s_id is None:
            s_id = request.session["YH_SID"] = uuid.uuid4().hex
            response.set_cookie(
                key="YH_SID",
                value=s_id,
                expires=datetime.now() + timedelta(days=common_constant.COOKIES_SID_DAYS)
            )
        # browser id 每个浏览器访问的唯一凭证
        b_id = request.COOKIES.get("YH_BID", None)

        if b_id is None:
            b_id = uuid.uuid4().hex
            response.set_cookie(
                key="YH_BID",
                value=b_id,
                expires=datetime.now() + timedelta(days=common_constant.COOKIES_BID_DAYS)
            )

        # open id 每个登录用户的唯一码
        o_id = request.COOKIES.get("YH_OID", None)

        if isinstance(request.user, User):
            if o_id is None:
                o_id = request.user.open_id
                response.set_cookie(
                    key="YH_OID",
                    value=o_id,
                    expires=datetime.now() + timedelta(days=common_constant.COOKIES_OID_DAYS)
                )
        else:
            if o_id:
                response.delete_cookie(key="YH_OID")

        return response


    def process_exception(self, request, exception):
        # 通知接口挂了
        pass
