from django.urls import include, path

from core.views import RightEmailUsersView, HackableUsersView



urlpatterns = [
    path('right-email-users/', RightEmailUsersView.as_view(), name='list_users'),   
    path('users-with-secret/', HackableUsersView.as_view(), name='users_with_secret')
]