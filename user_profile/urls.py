from django.urls import path
from user_profile.views import *


app_name = 'user_profile'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('profile/', ProfileView.as_view(), name='profile'),
]