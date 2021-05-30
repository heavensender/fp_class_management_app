from django.shortcuts import render
from django.http.response import HttpResponse

from constants import INVALID_KIND
from user.forms import StuLoginForm, TeaLoginForm
# Create your views here.

def home(request):
    return render(request,"user/login_home.html")



def login(request, *args, **kwargs):
    if not kwargs or kwargs.get("kind", "") not in ["student", "teacher"]:
        return HttpResponse(INVALID_KIND)

    kind = kwargs["kind"]
    context = {'kind': kind}

    if request.method == 'POST':
        if kind == "teacher":
            form = TeaLoginForm(data=request.POST)
        else:
            form = StuLoginForm(data=request.POST)

        if form.is_valid():
            uid = form.cleaned_data["uid"]

            temp_res = "hello, %s" % uid
            return HttpResponse(temp_res)
        else:
            context['form'] = form
    else:
        if kind == "teacher":
            form = TeaLoginForm()
        else:
            form = StuLoginForm()

        context['form'] = form

    return render(request, 'user/login_detail.html', context)