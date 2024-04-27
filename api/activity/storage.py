from django.core.files.storage import FileSystemStorage
from uuid import uuid4
import os

class FileStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        root, ext = os.path.splitext(name)
        unique_id = str(uuid4())
        new_name = f"{root}_{unique_id}{ext}"
        return super().get_available_name(new_name, max_length)
