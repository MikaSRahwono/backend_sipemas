from django.db import models
from api.user.models import User

from api.activity.models import Activity

# Create your models here.
class Note(models.Model):        
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='notes')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes_creator')
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(blank=True, auto_now=False, null=True)