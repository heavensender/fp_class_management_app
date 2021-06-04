import json

from django.core.paginator import PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import authenticate, login, logout
from user_profile.models import UserProfile
from django.db.models import Q
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile


#1Auth,from back-end
from utils.custom_paginator import CustomPaginator


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


#2Register
class RegisterView(View):
    def get(self, request):
        return render(request, 'user_profile/register.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        sex = int(request.POST.get('sex', 0))
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        user = UserProfile.objects.filter(Q(username=username))
        if user:   
            return render(request, 'user_profile/register.html', {'error': 'Account exist'})
        if phone and len(phone) != 11:
            return render(request, 'user_profile/register.html', {'error': 'Phone number should be 8 digit'})

        obj = UserProfile.objects.create(username=username, sex=sex, phone=phone, address=address)
        obj.set_password(password)
        obj.is_active = 1
        obj.save()

        return HttpResponseRedirect(reverse('user_profile:login'))


#3Login
class LoginRequiredMixin(View):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view, login_url='/user-profile/login/')


#4Logout
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('user_profile:login'))


#5Loginprocess
class LoginView(View):
    def get(self, request):
        return render(request, 'user_profile/login.html')

    def post(self, request):
        username = request.POST.get('user')
        password = request.POST.get('pwd')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("home"))
            else:
                return render(request, "user_profile/login.html", {"error": "Username or password is wrong"})


#Userinformation
class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user_id = request.GET.get("user_id")
        if not user_id:
            return render(request, 'user_profile/profile.html', {"user": request.user, 'myself': True})
        else:
            try:
                obj = UserProfile.objects.get(id=int(user_id))
            except Exception as e:
                return render(request, 'user_profile/error.html', {"error": "User not exist"})
            if obj.id == request.user.id:
                return render(request, 'user_profile/profile.html', {"user": obj, 'myself': True})
            return render(request, 'user_profile/profile.html', {"user": obj, 'myself': False})

    def post(self, request):
        user_id = request.POST.get("id")
        sex = request.POST.get("sex")
        phone = request.POST.get("phone")
        college = request.POST.get("college")
        address = request.POST.get("address")
        obj = UserProfile.objects.get(id=int(user_id))
        obj.college = college
        obj.sex = int(sex)
        obj.address = address
        obj.phone = phone
        obj.save()
        return HttpResponseRedirect(reverse("user_profile:profile") + "?id=" + user_id)


#Passwordreset
class ResetPasswordView(LoginRequiredMixin, View):
    def post(self, request):
        obj = UserProfile.objects.get(id=request.user.id)
        password = request.POST.get("password")
        obj.set_password(password)
        obj.save()
        return HttpResponse(json.dumps({'code':0, "avatar": obj.image.url}), content_type="application/json")
