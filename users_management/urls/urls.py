from django.urls import path, re_path

from users_management.views import ListUsers, RegisterUser, UserDetail

urlpatterns = [
    re_path(r'^users-list/$', ListUsers.as_view(), name='list-users'),
    path('register-user', RegisterUser.as_view(), name='register-user'),
    path('user/<str:pk>', UserDetail.as_view(), name='register-user'),
]
