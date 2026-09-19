from django.contrib import admin
from .models import LevelRequirement, UserProgress, ActivityLog


@admin.register(LevelRequirement)
class LevelRequirementAdmin(admin.ModelAdmin):
    list_display = ('level', 'title', 'xp_threshold')
    ordering = ('level',)


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'problem', 'solved', 'xp_awarded', 'first_solved_at')
    list_filter = ('solved', 'first_solved_at')
    search_fields = ('user__username', 'problem__title')
    ordering = ('-first_solved_at',)


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'description', 'created_at')
    list_filter = ('activity_type', 'created_at')
    search_fields = ('user__username', 'description')
    ordering = ('-created_at',)

