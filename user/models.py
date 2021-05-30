from django.db import models
from django.db.models import constraints

# Create your models here.

genders = [
        ('m', 'male'),
        ('f', 'female')
    ]

class Student(models.Model):
    

    name = models.CharField(max_length=50, verbose_name="Name")
    gender = models.CharField(max_length=10, choices=genders, default='m', verbose_name="gender")
    birthday = models.DateField(verbose_name="DOB")
    email = models.EmailField(verbose_name="Email")
    grade = models.CharField(max_length=4, verbose_name="Year of Exp")
    number = models.CharField(max_length=6, verbose_name="Student Num")
    password = models.CharField(max_length=10, verbose_name="Password")


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['grade','number'], name='student_id')
        ]
    
    def get_id(self):
        return "%s%s" % (self.grade, self.number)

    def __str__(self):
        return "%s(%s)" % (self.get_id(), self.name)



class Teacher(models.Model):
    

    name = models.CharField(max_length=50, verbose_name="Name")
    gender = models.CharField(max_length=10, choices=genders, default='m', verbose_name="gender")
    birthday = models.DateField(verbose_name="DOB")
    email = models.EmailField(verbose_name="Email")
    info = models.CharField(max_length=255, verbose_name="Bio", help_text="Max 250 words")

    department_no = models.CharField(max_length=3, verbose_name="course num")
    number = models.CharField(max_length=6, verbose_name="Teacher Num")
    password = models.CharField(max_length=10, verbose_name="Password")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['department_no', 'number'], name='teacher_id'),
        ]
    
    def get_id(self):
        return "%s%s" % (self.department_no, self.number)

    def __str__(self):
        return "%s(%s)" % (self.get_id(), self.name)

