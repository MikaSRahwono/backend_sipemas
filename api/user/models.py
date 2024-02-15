from django.db import models
from django.contrib.auth.models import User

from api.user.storage import ImageStorage
from ..marketplace.models import Field
from django.utils.translation import gettext_lazy as _

class UserDetail(models.Model):
    class UserType(models.TextChoices):
        LECTURER = 'LEC', _('Dosen')
        STUDENT = 'STU', _('Mahasiswa')

    user = models.OneToOneField(User, on_delete=models.CASCADE,  related_name='user_detail')
    email = models.CharField(max_length=256)
    kode_identitas = models.CharField(max_length=256)
    role = models.CharField(
        max_length=3,
        choices=UserType.choices,
        default=UserType.STUDENT,
    )
    is_external = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,  related_name='user_profile')
    name = models.CharField(max_length=256)
    major = models.CharField(max_length=256)
    about = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_imgs/', null=True, blank=True, storage=ImageStorage())
    line_id = models.CharField(max_length=256, blank=True)
    linkedin_url = models.CharField(max_length=256, blank=True)
    github_url = models.CharField(max_length=256, blank=True)
    is_open = models.BooleanField(default=True)
    fields = models.ManyToManyField(Field, related_name='field_of_interest')

class Experience(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)