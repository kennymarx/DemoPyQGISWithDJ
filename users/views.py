import requests
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import AuthorizedUser

WECHAT_LOGIN_URL = 'https://api.weixin.qq.com/sns/jscode2session'

class WeChatLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        code = request.data.get('code')
        if not code:
            return Response({'code': 400, 'message': '缺少code参数'}, status=status.HTTP_400_BAD_REQUEST)

        params = {
            'appid': settings.WECHAT_APP_ID,
            'secret': settings.WECHAT_APP_SECRET,
            'js_code': code,
            'grant_type': 'authorization_code'
        }

        try:
            response = requests.get(WECHAT_LOGIN_URL, params=params)
            data = response.json()
        except Exception as e:
            return Response({'code': 500, 'message': '微信服务器请求失败'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if 'errcode' in data and data['errcode'] != 0:
            return Response({'code': data['errcode'], 'message': data.get('errmsg', '登录失败')}, status=status.HTTP_400_BAD_REQUEST)

        openid = data.get('openid')
        if not openid:
            return Response({'code': 400, 'message': '获取openid失败'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            authorized_user = AuthorizedUser.objects.get(openid=openid)
            if not authorized_user.is_active:
                return Response({'code': 403, 'message': '用户未授权或已禁用'}, status=status.HTTP_403_FORBIDDEN)
        except AuthorizedUser.DoesNotExist:
            return Response({'code': 403, 'message': '非授权人员，请联系管理员'}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(None)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response({
            'code': 0,
            'message': '登录成功',
            'data': {
                'openid': openid,
                'nickname': authorized_user.nickname,
                'avatar': authorized_user.avatar,
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        })

class UserPermissionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        openid = request.query_params.get('openid')
        if not openid:
            return Response({'code': 400, 'message': '缺少openid参数'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            authorized_user = AuthorizedUser.objects.get(openid=openid)
            if not authorized_user.is_active:
                return Response({'code': 403, 'message': '用户已禁用'}, status=status.HTTP_403_FORBIDDEN)
            return Response({
                'code': 0,
                'message': '用户已授权',
                'data': {
                    'is_authorized': True,
                    'nickname': authorized_user.nickname,
                    'avatar': authorized_user.avatar
                }
            })
        except AuthorizedUser.DoesNotExist:
            return Response({'code': 403, 'message': '非授权人员'}, status=status.HTTP_403_FORBIDDEN)

class CheckAuthView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        # 
        print("CheckAuthView:",request.data)
        code = request.data.get('code')
        if not code:
            return Response({'code': 400, 'message': '缺少code参数'}, status=status.HTTP_400_BAD_REQUEST)

        params = {
            'appid': settings.WECHAT_APP_ID,
            'secret': settings.WECHAT_APP_SECRET,
            'js_code': code,
            'grant_type': 'authorization_code'
        }

        try:
            response = requests.get(WECHAT_LOGIN_URL, params=params)
            data = response.json()
        except Exception as e:
            return Response({'code': 500, 'message': '微信服务器请求失败'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if 'errcode' in data and data['errcode'] != 0:
            return Response({'code': data['errcode'], 'message': data.get('errmsg', '验证失败')}, status=status.HTTP_400_BAD_REQUEST)

        openid = data.get('openid')
        if not openid:
            return Response({'code': 400, 'message': '获取openid失败'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            print("openid:",openid)
            authorized_user = AuthorizedUser.objects.get(openid=openid)
            if not authorized_user.is_active:
                return Response({
                    'code': 403,
                    'message': '用户已禁用',
                    'data': {'is_authorized': False}
                })
            else:
                print("authorized_user:",authorized_user)
            from rest_framework_simplejwt.tokens import RefreshToken
            refresh = RefreshToken.for_user(None)
            access_token = str(refresh.access_token)
            
            return Response({
                'code': 0,
                'message': '用户已授权',
                'data': {
                    'is_authorized': True,
                    'openid': openid,
                    'nickname': authorized_user.nickname,
                    'avatar': authorized_user.avatar,
                    'access_token': access_token
                }
            })
        except AuthorizedUser.DoesNotExist:
            return Response({
                'code': 403,
                'message': '非授权人员，请联系管理员',
                'data': {'is_authorized': False}
            })
