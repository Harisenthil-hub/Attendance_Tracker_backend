from django.urls import path
from apps.users.views.user import MeView
from apps.users.views.status import UpdateUserStatusView


urlpatterns = [
    path('me/', MeView.as_view(), name='me'),
    path('<uuid:user_uuid>/status/', UpdateUserStatusView.as_view(), name='update_user_status'),
]
