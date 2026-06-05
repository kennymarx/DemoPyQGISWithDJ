from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import AuthorizedUser


class AuthorizedUserJWTAuthentication(JWTAuthentication):
    """
    自定义 JWT 认证类 - 使用 AuthorizedUser 作为用户模型
    
    替代默认的 JWTAuthentication，这样认证时会从 AuthorizedUser 表查找用户，
    而不是从 Django 默认的 auth_user 表查找。
    """
    
    def get_user(self, validated_token):
        """
        根据验证后的 token 获取用户对象
        
        Args:
            validated_token: 验证后的 JWT token，包含 user_id 字段
            
        Returns:
            AuthorizedUser: 找到的用户对象
            
        Raises:
            AuthorizedUser.DoesNotExist: 用户不存在时抛出异常
        """
        # 从 token payload 中获取 user_id
        user_id = validated_token['user_id']
        
        # 从 AuthorizedUser 表中查找用户（而不是从 auth_user 表）
        return AuthorizedUser.objects.get(id=user_id)
