from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField



class User(AbstractUser):
    pass

class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        abstract = True

class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Course(models.Model):
    subject = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to="course/%Y/%m", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.subject

class Lesson(BaseModel):
    subject = models.CharField(max_length=255)
    content = RichTextField()
    image = models.ImageField(upload_to="lesson/%Y/%m", null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
