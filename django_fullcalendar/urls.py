"""django_fullcalendar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

from django.conf.urls.static import static
from django.conf import settings

from app.views import HomeView, LessonListView, LessonAddView, LessonUpdateView, LessonDelView, LessonTakePartInView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user-profile/', include('user_profile.urls', namespace='user_profile')),
    re_path('^$', HomeView.as_view(), name="home"),
    path('lesson-list/', LessonListView.as_view(), name="lesson-list"),
    path('lesson-add/', LessonAddView.as_view(), name="lesson-add"),
    path('lesson-update/', LessonUpdateView.as_view(), name="lesson-update"),
    path('lesson-del/', LessonDelView.as_view(), name="lesson-del"),
    path('competition-take/', LessonTakePartInView.as_view(), name="lesson-take"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)