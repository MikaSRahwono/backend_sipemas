from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

from api.user.storage import ImageStorage
from django.utils.translation import gettext_lazy as _

class Field(models.Model):
    name = models.CharField(max_length=256)
    code = models.CharField(max_length=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Organization(models.Model):
    class Faculty(models.TextChoices):
        ILMU_KOMPUTER = 'ILMU KOMPUTER', _('Ilmu Komputer')

    id = models.CharField(max_length=11, primary_key=True)
    faculty = models.CharField(
        max_length=256, 
        choices=Faculty.choices, 
        default=Faculty.ILMU_KOMPUTER,
        blank=True)
    study_program = models.CharField(max_length=256, blank=True)
    educational_program = models.CharField(max_length=256, blank=True)

class UserDetail(models.Model):
    class UserType(models.TextChoices):
        SECRETARY = 'SEC', _('Secretary')
        LECTURER = 'LEC', _('Dosen')
        STUDENT = 'STU', _('Mahasiswa')

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_detail')
    full_name = models.CharField(max_length=256)
    id_code = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    role = models.CharField(
        max_length=3,
        choices=UserType.choices,
        default=UserType.STUDENT,
    )
    is_external = models.BooleanField(default=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='organization', null=True, blank=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,  related_name='user_profile')
    about = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_imgs/', null=True, blank=True, storage=ImageStorage())
    line_id = models.CharField(max_length=256, blank=True)
    linkedin_url = models.CharField(max_length=256, blank=True)
    github_url = models.CharField(max_length=256, blank=True)
    instagram_url = models.CharField(max_length=256, blank=True)
    website_url = models.CharField(max_length=256, blank=True)
    is_open = models.BooleanField(default=True)
    fields = models.ManyToManyField(Field, related_name='field_of_interest', blank=True)
    experiences = ArrayField(models.CharField(max_length=256, blank=True), default=list, blank=True)

class Experience(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)

