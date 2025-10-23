from django.contrib import admin
from .models import LearningBlockModel

@admin.register(LearningBlockModel)
class LearningBlockAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "xp", "created_at")