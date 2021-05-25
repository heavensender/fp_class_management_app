from django import forms
from user.models import Student, Teacher


class StuLoginForm(forms.Form):
    uid = forms.CharField(label='student_id', max_length=10)
    password = forms.CharField(label='password', max_length=30, widget=forms.PasswordInput)


class TeaLoginForm(forms.Form):
    uid = forms.CharField(label='teacher_id', max_length=10)
    password = forms.CharField(label='password', max_length=30, widget=forms.PasswordInput)