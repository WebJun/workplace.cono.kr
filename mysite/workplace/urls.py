from django.urls import path

from . import views_front
from . import views_back

urlpatterns = [
    # 프론트
    path('', views_front.index),
    path('members_login_success', views_front.members_login_success),
    path('favicon.ico', views_front.favicon),

    # 백
    path('api/members', views_back.members_add),
    path('api/members/login', views_back.members_login),
    path('api/commute', views_back.commute),
]
