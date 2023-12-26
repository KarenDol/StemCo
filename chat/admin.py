from django.contrib import admin
from .models import Problem, Hint, Question_Creator
# Register your models here.

admin.site.register(Problem)
admin.site.register(Hint)
admin.site.register(Question_Creator)