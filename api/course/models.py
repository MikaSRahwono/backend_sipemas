from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField

class Course(models.Model):
    class CourseType(models.TextChoices):
        ONETOONE = 'OO', _('One to One')
        ONETOMANY = 'OM', _('One to Many')

    kd_mk = models.CharField(max_length=9, primary_key=True)
    nm_mk = models.CharField(max_length=256)
    sks = models.IntegerField()
    course_type = models.CharField(
        max_length=2,
        choices=CourseType.choices,
    )
    is_allowed_new_topic = models.BooleanField()
    topic_count = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'courses'

    def __str__(self):
        return self.title

class CourseInformation(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    html = RichTextField()

    def __str__(self):
        return self.html
    
class Prerequisite(models.Model):
    class PrerequisiteType(models.TextChoices):
        SKS = 'SKS', _('Jumlah SKS')
        SEMESTER = 'SMT', _('Semester')
        COURSE = 'CRS', _('Mata Kuliah')
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=3,
        choices=PrerequisiteType.choices,
        default=PrerequisiteType.SKS,
    )
    minimum = models.IntegerField(default=0)
    maximum = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.type
