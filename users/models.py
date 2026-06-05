from django.db import models
from django.contrib.auth.models import AbstractUser


class AuthorizedUser(models.Model):
    openid = models.CharField(max_length=100, unique=True, verbose_name='微信OpenID')
    nickname = models.CharField(max_length=100, blank=True, null=True, verbose_name='昵称')
    avatar = models.URLField(blank=True, null=True, verbose_name='头像URL')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '授权用户'
        verbose_name_plural = '授权用户列表'

    def __str__(self):
        return self.nickname or self.openid

    # 以下是 Django User 模型需要的属性和方法
    @property
    def is_authenticated(self):
        """总是返回 True，因为这是一个已认证的用户"""
        return True

    @property
    def is_anonymous(self):
        """总是返回 False，因为这不是匿名用户"""
        return False

    def get_username(self):
        """返回用户名，使用 openid 作为用户名"""
        return self.openid

class UserProfile(models.Model):
    user = models.OneToOneField('AuthorizedUser', on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField(blank=True, null=True, verbose_name='邮箱')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='手机号')

    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料列表'

    def __str__(self):
        return self.user.nickname or self.user.openid