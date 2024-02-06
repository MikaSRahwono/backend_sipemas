from django.db import models
from django.utils.translation import gettext_lazy as _


class Course(models.Model):
    class CourseType(models.TextChoices):
        ONETOONE = 'OO', _('One to One')
        ONETOMANY = 'OM', _('One to Many')

    title = models.CharField(max_length=256)
    course_type = models.CharField(
        max_length=2,
        choices=CourseType.choices,
        default=CourseType.ONETOONE,
    )
    is_allowed_new_topic = models.BooleanField(default=True)
    topic_count = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'courses'

    def __str__(self):
        return self.title

class Field(models.Model):
    name = models.CharField(max_length=256) 
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Topic(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    is_open = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    fields = models.ManyToManyField(Field)

    def __str__(self):
        return self.title

class TopicInformation(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    html = models.TextField(blank=False)

    def __str__(self):
        return self.html

class Prerequisite(models.Model):
    class PrerequisiteType(models.TextChoices):
        SKS = 'SKS', _('Jumlah SKS')
        SEMESTER = 'SMT', _('Semester')
        COURSE = 'CRS', _('Mata Kuliah')
    
    course =  models.ForeignKey(Course, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=3,
        choices=PrerequisiteType.choices,
        default=PrerequisiteType.SKS,
    )
    minimum = models.IntegerField(default=0)
    maximum = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.title
