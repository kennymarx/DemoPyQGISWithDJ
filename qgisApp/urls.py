from django.urls import path
from .views import CreateMapByCoord

urlpatterns = [
    path('create_map/', CreateMapByCoord.as_view(), name='create_map'),
]
