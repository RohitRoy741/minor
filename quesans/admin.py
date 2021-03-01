from django.contrib import admin
from .models import Question,Answer,QuestionGroups
admin.site.register(Question)
admin.site.register(QuestionGroups)
admin.site.register(Answer)
