from django.db import models
# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=30)
    department = models.CharField(max_length=100)
    branch = models.CharField(max_length=200)
    roll_no = models.IntegerField()
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class FileUpload(models.Model):
    """Represents file upload model class."""

    owner = models.CharField(max_length=250)
    file = models.FileField(upload_to='csv_uploads/%y/%m')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return file name."""
        return self.file.name