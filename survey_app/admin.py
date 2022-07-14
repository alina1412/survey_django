from django.contrib import admin


from .models import User, Answer, Choice, Survey, Question


# admin.site.register(User)
admin.site.register(Answer)
admin.site.register(Choice)
admin.site.register(Survey)
admin.site.register(Question)