from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Problem(models.Model):
    problem_ID = models.CharField(max_length=5, primary_key=True)
    content = models.TextField()


class Hint(models.Model):
    problem_ID = models.CharField(max_length=5, primary_key=True)
    hint1 = models.TextField(null=True)
    hint2 = models.TextField(null=True)
    hint3 = models.TextField(null=True)


class Question_Creator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)
    last_update = models.DateField()