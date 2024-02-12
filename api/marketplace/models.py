from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField

class UserDetail(models.Model):
    class UserType(models.TextChoices):
        LECTURER = 'LEC', _('Dosen')
        STUDENT = 'STU', _('Mahasiswa')

    username = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    kode_identitas = models.CharField(max_length=256)
    role = models.CharField(
        max_length=3,
        choices=UserType.choices,
        default=UserType.STUDENT,
    )
    is_external = models.BooleanField(default=False)

class Field(models.Model):
    name = models.CharField(max_length=256)
    code = models.CharField(max_length=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(UserDetail, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    major = models.CharField(max_length=256)
    about = models.TextField(blank=True)
    profile_image = models.CharField(max_length=256, blank=True)
    line_id = models.CharField(max_length=256, blank=True)
    linkedin_url = models.CharField(max_length=256, blank=True)
    github_url = models.CharField(max_length=256, blank=True)
    is_open = models.BooleanField(default=True)
    fields = models.ManyToManyField(Field, related_name='field_of_interest')

class Experience(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)

class Course(models.Model):
    class CourseType(models.TextChoices):
        ONETOONE = 'OO', _('One to One')
        ONETOMANY = 'OM', _('One to Many')

    title = models.CharField(max_length=256)
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

class Topic(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    is_open = models.BooleanField(default=True)
    num_of_people = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    fields = models.ManyToManyField(Field)
    supervisors = models.ManyToManyField(UserDetail)

    def __str__(self):
        return self.title

class TopicInformation(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
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

class Application(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    praproposal = models.CharField(max_length=256)
    is_approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

class ApplicationApproval(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    approvee = models.ManyToManyField(UserDetail)
    is_approved = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(blank=True, auto_now=False, null=True)
    

