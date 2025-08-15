import rest_framework_simplejwt.views as django_rest_fw_simplejwt_views

from django.urls import path

from .role import views as user_role_views
from .user import views as user_authencation_views


urlpatterns = [
    path('role', user_role_views.UserRoleViews.as_view(), name='user-role'),
    path('register', user_authencation_views.UserRegisterView.as_view(), name='register'),
    path('login', user_authencation_views.UserLoginView.as_view(), name='login'),
    path('logout', user_authencation_views.UserLogoutView.as_view(), name='logout'),
    path('update-profile', user_authencation_views.UserProfileView.as_view(), name='profile'),
    path('token/refresh', django_rest_fw_simplejwt_views.TokenRefreshView.as_view(), name='token-refresh'),
    path('change-password', user_authencation_views.UserChangePasswordView.as_view(), name='user-change-password')
]
