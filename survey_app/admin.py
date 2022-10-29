from django.contrib import admin

from .models import Answer, Choice, Question, Survey

admin.site.register(Answer)
admin.site.register(Choice)
admin.site.register(Survey)
admin.site.register(Question)
