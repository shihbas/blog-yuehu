# coding=utf-8

import requests

from django.conf import settings
from django.contrib.auth import login
from django.db.models import Q

from requests_oauthlib import OAuth2Session

from rest_framework.response import Response
from rest_framework.views import APIView

from common.exceptions import LogicException
from common.decorators import api_common
from common.function import email_rightful

from account.models import WeiBoUser, GitHubUser, User
from account.utils import create_account, random_password, send_email_html_oauth_once_pwd, send_email_html_oauth_old_account
from account import constant as account_constant

from helper.logs import get_logger

logger = get_logger(__name__)


class WeiBoLogin(APIView):

    client_id = settings.WEIBO_CLINT_ID
    client_secret = settings.WEIBO_CLINT_SECRET
    redirect_uri = settings.WEIBO_REDIRECT_URI
    scope = settings.WEIBO_SCOPE
    state = "python_dog"
    token_url = "https://api.weibo.com/oauth2/access_token"
    info_url = "https://api.weibo.com/2/users/show.json"
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
     }

    @api_common
    def get(self, request):
        code = request.GET.get("code")

        try:
            response = requests.post(
                url=self.token_url,
                data={
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                    'grant_type': 'authorization_code',
                    'code': code,
                    'redirect_uri': self.redirect_uri,
                },
                headers=self.headers
            )

            rs_json = response.json()

            access_token = rs_json.get('access_token', None)
            uid_str = rs_json.get('uid', None)
            if access_token is None or uid_str is None:
                raise KeyError
            uid = int(uid_str)
        except KeyError as e:
            raise LogicException("找不到有效的微博认证Token,可以重新登录或联系我")
        except (TypeError, ValueError) as e:
            raise LogicException("微博认证UID错误,可以重新登录或联系我")
        except Exception as e:
            logger.error(e)
            raise LogicException("获取微博认证Token错误,可以重新登录或联系我")

        weibo_user = WeiBoUser.objects.select_related('user').filter(uid=uid_str).first()

        # 如果找不到该用户就新建一个
        if weibo_user is None:

            try:
                response_user_info = requests.get(
                    url=self.info_url,
                    params={
                        'access_token': access_token,
                        'uid': uid
                    },
                    headers=self.headers
                )
                rs_user_info_json = response_user_info.json()
                name = rs_user_info_json.get("screen_name", None)
                avatar = rs_user_info_json.get("profile_image_url", None)
                gender = rs_user_info_json.get("gender", None)
                if gender:
                    gender = 1 if gender == 'm' else 0
            except Exception as e:
                logger.error(e)
                raise LogicException("获取微博用户信息时出错了，可以重新登录或联系我")

            weibo_user = WeiBoUser()
            weibo_user.uid = uid_str
            weibo_user.avatar = avatar
            weibo_user.name = name
            weibo_user.gender = gender

            username = f'weibo_{uid_str}'
            password = random_password(length=12)
            created, user = create_account(
                username=username,
                password=password,
                register_type=account_constant.ACCOUNT_REGISTER_TYPE_WEIBO,
                avatar=weibo_user.avatar,
                nickname=weibo_user.name,
                gender=weibo_user.gender
            )
            if not created:
                raise LogicException("创建用户失败, 请重新登录授权")

            weibo_user.user = user
            weibo_user.save()

        login(request, weibo_user.user)
        return Response({"login": "success"})


class GitHubLogin(APIView):

    client_id = settings.GITHUB_CLINT_ID
    client_secret = settings.GITHUB_CLINT_SECRET
    redirect_uri = settings.GITHUB_REDIRECT_URI
    scope = settings.GITHUB_SCOPE
    state = "python_dog"
    token_url = "https://github.com/login/oauth/access_token"
    info_url = "https://api.github.com/user"


    @api_common
    def get(self, request):

        code = request.GET.get("code")

        git_oauth = OAuth2Session(
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            state=self.state,
            scope=self.scope
        )
        try:
            git_oauth.fetch_token(
                self.token_url,
                method="POST",
                code=code,
                client_secret=self.client_secret
            )
            response = git_oauth.get(self.info_url)
            result = response.json()
        except Exception as e:
            logger.error(e)
            raise LogicException("获取github用户信息错误，请重新登录")

        uid = result.get("id")
        avatar = result.get("avatar_url")
        name = result.get("name")
        email = result.get("email")

        if uid is None:
            raise LogicException("请求Github认证时错误，请重新登录")

        # 获取 uid
        uid_str = str(uid)

        github_user = GitHubUser.objects.select_related('user').filter(uid=uid_str).first()

        # 如果找不到该用户就新建一个
        if github_user is None:

            github_user = GitHubUser()
            github_user.uid = uid_str
            github_user.avatar = avatar
            github_user.name = name
            if email:
                right, email = email_rightful(email)
            else:
                right, email = False, None
            github_user.email = email

            # 判断是否有对应邮箱的账号
            if right:
                user = User.objects.filter(Q(username=email)|Q(email=email)).first()
                if user is None:
                    username = email
                    password = random_password(length=12)
                    created, user = create_account(
                        username=username,
                        password=password,
                        register_type=account_constant.ACCOUNT_REGISTER_TYPE_GITHUB,
                        avatar=github_user.avatar,
                        nickname=github_user.name,
                        email=github_user.email
                    )
                    if not created:
                        raise LogicException("创建用户失败")
                    # 发送新用户的邮件
                    send_email_html_oauth_once_pwd(
                        name=name,
                        password=password,
                        oauth_register='github',
                        address_email=email
                    )
                else:
                    # 发送新用户的邮件
                    send_email_html_oauth_old_account(
                        name=name,
                        oauth_register='github',
                        address_email=email
                    )
            else:
                username = f'github_{uid_str}'
                password = random_password(length=12)
                created, user = create_account(
                    username=username,
                    password=password,
                    register_type=account_constant.ACCOUNT_REGISTER_TYPE_GITHUB,
                    avatar=github_user.avatar,
                    nickname=github_user.name,
                    email=github_user.email
                )
                if not created:
                    raise LogicException("创建用户失败")

            github_user.user = user
            github_user.save()

        login(request, github_user.user)
        return Response({"login": "success"})
