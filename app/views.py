
import random

from django.core.paginator import PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from app.models import LessonModel, LessonUserModel
from user_profile.views import LoginRequiredMixin
from utils.custom_paginator import CustomPaginator
from utils.date_util import DateUtil


class HomeView(LoginRequiredMixin):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(HomeView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        lesson_list = LessonModel.objects.all()

        response = []
        for item in lesson_list:
            start = DateUtil.datetime_to_date_str(item.class_time)
            title = "%s:%s :%s" % (DateUtil.datetime_to_hour_minute_str(item.class_time), item.name, item.person_num)
            response.append({"title": title, "start": start})
        return render(request, 'app/index.html', {"data": response})


class LessonListView(LoginRequiredMixin):
    def get(self, request):
        obj_list = LessonModel.objects.all().order_by("-id")
        current_page = request.GET.get("page", '1')
        name = request.GET.get("name", "")
        if name:
            obj_list = obj_list.filter(card__contains=name)
        paginator = CustomPaginator(current_page, 9, obj_list, 10)
        try:
            paginator = paginator.page(current_page)  
        except PageNotAnInteger:
            # Error then show first page
            paginator = paginator.page(1)
        except EmptyPage:
            # Error then show last page
            paginator = paginator.page(paginator.num_pages)
        return render(request, 'app/lesson_list.html', {"paginator": paginator, "name": name})


class LessonAddView(LoginRequiredMixin):
    def get(self, request):
        return render(request, 'app/lesson_add.html')

    def post(self, request):
        name = request.POST.get("name")
        class_time = request.POST.get("class_time")
        teacher_name = request.POST.get("teacher_name")
        description = request.POST.get("description")
        if not name or not class_time or not teacher_name or not description:
            return render(request, 'app/lesson_add.html', {'error': 'wrong input'})
        else:

            LessonModel.objects.create(name=name, class_time=DateUtil.str_to_datetime(class_time),
                                       teacher_name=teacher_name, description=description)
            return HttpResponseRedirect(reverse('lesson-list'))


class LessonUpdateView(LoginRequiredMixin):
    def get(self, request):
        lesson_id = request.GET.get("id")
        lesson = LessonModel.objects.get(id=lesson_id)
        return render(request, 'app/lesson_update.html', {"lesson": lesson})

    def post(self, request):
        lesson_id = request.GET.get("id")
        lesson = LessonModel.objects.get(id=lesson_id)
        name = request.POST.get("name")
        class_time = request.POST.get("class_time")
        teacher_name = request.POST.get("teacher_name")
        description = request.POST.get("description")

        if not name or not class_time or not teacher_name or not description:
            return render(request, 'app/lesson_add.html', {'error': 'Wrong input '})
        else:

            lesson.name = name
            lesson.teacher_name = teacher_name
            lesson.class_time = DateUtil.str_to_datetime(class_time)
            lesson.description = description
            lesson.save()
            return HttpResponseRedirect(reverse('lesson-list'))


class LessonDelView(LoginRequiredMixin):
    def get(self, request):
        lesson_id = request.GET.get("id")
        LessonModel.objects.get(id=lesson_id).delete()
        LessonUserModel.objects.filter(lesson_id=lesson_id).delete()

        return HttpResponseRedirect(reverse('lesson-list'))


class LessonTakePartInView(LoginRequiredMixin):
    def get(self, request):
        user = request.user
        lesson_id = request.GET.get("id")
        lesson = LessonModel.objects.get(id=lesson_id)

        # Already booked
        if LessonUserModel.objects.filter(lesson=lesson, user=user):
            return render(request, 'app/error.html', {'error': 'You have already booked lesson'})

        LessonUserModel.objects.create(lesson=lesson, user=user)
        lesson.person_num += 1
        lesson.save()
        return HttpResponseRedirect(reverse('lesson-list'))

