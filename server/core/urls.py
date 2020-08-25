from django.urls import include, path

from core.views import ListUsers



urlpatterns = [
    path('users/', ListUsers.as_view(), name='list_users')
]