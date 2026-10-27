from django.db import models
from .category import  Category
from .user import User


# Create your models here.
class Post(models.Model):
    title_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models. TextField()

    auther = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', blank=True)
    categories = models.ManyToManyField(Category, related_name='posts', blank=True, null=True)

    def __str__(self):
        return self.title