from django.db import models

# Create your models here.
from user_profile.models import UserProfile


class LessonModel(models.Model):
    name = models.CharField(verbose_name="Course Name", max_length=255)
    class_time = models.DateTimeField(verbose_name="Course Time")
    person_num = models.IntegerField(verbose_name="Num of students", default=0)
    teacher_name = models.CharField(verbose_name="Instructor", max_length=255)
    description = models.TextField(verbose_name="Course info")

    class Meta:
        db_table = "lesson"


class LessonUserModel(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    lesson = models.ForeignKey(LessonModel, on_delete=models.CASCADE)

    class Meta:
        db_table = "lesson_user"




