from django.urls import path
from .views.auth import RegisterView, LoginView
from .views.otp import SendOTPView, VerifyOTPView, ResetPasswordView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='user_register'),
    path('login/', LoginView.as_view(), name='login'),
    path('otp/send/', SendOTPView.as_view(), name='send_otp'),
    path('otp/verify', VerifyOTPView.as_view(), name='verify_otp'),
    path('password/reset/', ResetPasswordView.as_view(), name='reset_password'),
]
