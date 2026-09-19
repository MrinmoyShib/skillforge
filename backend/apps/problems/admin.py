from django.contrib import admin
from .models import Category, Tag, DifficultyXPConfig, Problem, TestCase


class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 1
    fields = ('order', 'is_sample', 'input_data', 'expected_output')


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'difficulty', 'challenge_level', 'category', 'xp_reward', 'is_published', 'created_at')
    list_filter = ('language', 'difficulty', 'challenge_level', 'category', 'is_published')
    search_fields = ('title', 'description', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    inlines = [TestCaseInline]
    actions = ['publish_selected', 'unpublish_selected']

    @admin.action(description="Publish selected problems")
    def publish_selected(self, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description="Unpublish selected problems")
    def unpublish_selected(self, request, queryset):
        queryset.update(is_published=False)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'display_order')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'problem', 'is_sample', 'order')
    list_filter = ('is_sample', 'problem')


@admin.register(DifficultyXPConfig)
class DifficultyXPConfigAdmin(admin.ModelAdmin):
    list_display = ('difficulty', 'xp_reward')

