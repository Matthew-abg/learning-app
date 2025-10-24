from django.contrib import admin
from .models import LearningContentModel, LearningBlockModel, LearningUnitModel

@admin.register(LearningContentModel)
class LearningContentAdmin(admin.ModelAdmin):
    list_display = ("id", "data")

@admin.register(LearningBlockModel)
class LearningBlockAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "xp", "created_at")

@admin.register(LearningUnitModel)
class LearningUnitAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "type", "xp", "created_at")