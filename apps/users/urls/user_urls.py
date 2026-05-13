from django.urls import path
from apps.users.views.user import MeView, UpdateProfile
from apps.users.views.status import UpdateUserStatusView


urlpatterns = [
    path('me/', MeView.as_view(), name='me'),
    path('me/profile/', UpdateProfile.as_view(), name='profile'),
    path('<uuid:user_uuid>/status/', UpdateUserStatusView.as_view(), name='update_user_status'),
]
