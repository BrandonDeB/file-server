from django.db import models
from django.contrib.auth.models import User

def recurse_get_fp(folder):
    if folder.parent is None:
        return folder.name
    return f"{recurse_get_fp(folder.parent)}/{folder.name}"

def user_directory_path(instance, filename):
    folder_path = recurse_get_fp(instance.folder)
    return f"{folder_path}/{filename}"

# Create your models here.
class Folder(models.Model):
    name = models.CharField(max_length=255, null=False)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Client(models.Model):
    master = models.ForeignKey(Folder, on_delete=models.CASCADE, null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class File(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=False)
    upload = models.FileField(upload_to=user_directory_path, null=False)

