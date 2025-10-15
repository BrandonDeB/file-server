from django.db import models

def recurse_get_fp(folder):
    if folder.parent is None:
        return folder.name
    return f"{recurse_get_fp(folder.parent)}/{folder.name}"

def user_directory_path(instance, filename):
    folder_path = recurse_get_fp(instance.folder)
    return f"{folder_path}/{filename}"

# Create your models here.
class Folder(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)

class User(models.Model):
    master = models.ForeignKey(Folder, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=255)

class File(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True)
    upload = models.FileField(upload_to=user_directory_path, null=False)

