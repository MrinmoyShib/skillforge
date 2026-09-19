from django.contrib import admin
from .models import Submission, SubmissionResult


class SubmissionResultInline(admin.TabularInline):
    model = SubmissionResult
    extra = 0
    readonly_fields = ('test_case', 'status', 'execution_time', 'memory_usage', 'actual_output', 'stderr_output')
    can_delete = False


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'problem', 'status', 'passed_test_cases_count',
        'total_test_cases_count', 'execution_time', 'memory_usage', 'is_sample_run', 'created_at'
    )
    list_filter = ('status', 'is_sample_run', 'language', 'created_at')
    search_fields = ('user__username', 'problem__title', 'id')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [SubmissionResultInline]


@admin.register(SubmissionResult)
class SubmissionResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'submission', 'test_case', 'status', 'execution_time', 'memory_usage')
    list_filter = ('status',)

