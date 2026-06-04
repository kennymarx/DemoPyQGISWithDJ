from django.urls import path
from .views import WeChatLoginView, UserPermissionView, CheckAuthView

urlpatterns = [
    path('wxlogin/', WeChatLoginView.as_view(), name='wx_login'),
    path('check_auth/', CheckAuthView.as_view(), name='check_auth'),
    path('permission/', UserPermissionView.as_view(), name='user_permission'),
]
