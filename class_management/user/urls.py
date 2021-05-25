from user import views
from django.urls import path
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('login/', views.home,name="login"),
    path('login/<slug:kind>', views.login, name="login")
]


