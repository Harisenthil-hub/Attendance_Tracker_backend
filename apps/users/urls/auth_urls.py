from django.urls import path
from apps.users.views.auth import CreateUserView, LoginView, LogoutView, ChangePasswordView
from apps.users.views.otp import SendOTPView, VerifyOTPView, ResetPasswordView
from apps.users.authentication.refreshToken import CookieTokenRefreshView



urlpatterns = [
    path('create/user/', CreateUserView.as_view(), name='user_register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('otp/send/', SendOTPView.as_view(), name='send_otp'),
    path('otp/verify/', VerifyOTPView.as_view(), name='verify_otp'),
    path('password/reset/', ResetPasswordView.as_view(), name='reset_password'),
]
