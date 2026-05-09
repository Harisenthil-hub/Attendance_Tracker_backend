from django.urls import path
from apps.users.views.auth import RegisterView, LoginView
from apps.users.views.otp import SendOTPView, VerifyOTPView, ResetPasswordView
from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns = [
    path('register/', RegisterView.as_view(), name='user_register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('otp/send/', SendOTPView.as_view(), name='send_otp'),
    path('otp/verify/', VerifyOTPView.as_view(), name='verify_otp'),
    path('password/reset/', ResetPasswordView.as_view(), name='reset_password'),
]
