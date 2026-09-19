from django.contrib import admin
from .models import Project, ProjectMilestone, UserProjectProgress


class ProjectMilestoneInline(admin.StackedInline):
    model = ProjectMilestone
    extra = 1
    fields = ('order', 'title', 'description', 'xp_reward', 'starter_code', 'test_harness_code')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'difficulty', 'challenge_level', 'xp_reward', 'is_published', 'order')
    list_filter = ('language', 'difficulty', 'challenge_level', 'is_published')
    search_fields = ('title', 'slug', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectMilestoneInline]


@admin.register(ProjectMilestone)
class ProjectMilestoneAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'order', 'title', 'xp_reward')
    list_filter = ('project__language', 'project')
    search_fields = ('title', 'description')


@admin.register(UserProjectProgress)
class UserProjectProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'status', 'current_milestone_order', 'started_at', 'completed_at')
    list_filter = ('status', 'project__language')
    search_fields = ('user__username', 'project__title')

