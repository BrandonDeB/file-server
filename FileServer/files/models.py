from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

def recurse_get_fp(folder):
    if folder.parent is None:
        return folder.name
    return f"{recurse_get_fp(folder.parent)}/{folder.name}"

def user_directory_path(instance, filename):
    folder_path = recurse_get_fp(instance.folder)
    return f"{folder_path}/{filename}"

# Create your models here.
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Folder(models.Model):
    name = models.CharField(max_length=255, null=False)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class File(models.Model):
    class FileType(models.TextChoices):
        TEXT = "TXT", _("Text File")
        MEDIA = "MED", _("Media File")

    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=False)
    upload = models.FileField(upload_to=user_directory_path, null=False)
    file_type = models.CharField(
        max_length = 3,
        choices=FileType,
        default=FileType.MEDIA,
    )
    shared_with = models.ManyToManyField(Client, blank=True, related_name='shared_files')
    owner = models.ForeignKey(Client, on_delete=models.CASCADE, null=False, related_name='owned_files')

    def can_access(self, user):
        return user == self.owner or self.shared_with.filter(id=user.id).exists()

    def is_editable(self):
        return self.file_type == "TXT"

    def __str__(self):
        return self.upload.name
