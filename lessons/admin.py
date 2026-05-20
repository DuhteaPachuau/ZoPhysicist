from django.contrib import admin

from .models import Category, FeaturedLesson, Lesson, PracticeQuestion, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "accent_color")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "publish_date", "reading_time", "is_featured", "is_published")
    list_filter = ("is_featured", "is_published", "category", "tags", "publish_date")
    search_fields = ("title", "short_description", "full_content")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    date_hierarchy = "publish_date"
    readonly_fields = ("created_at", "updated_at", "views")


@admin.register(FeaturedLesson)
class FeaturedLessonAdmin(admin.ModelAdmin):
    list_display = ("lesson", "headline", "priority", "is_active")
    list_editable = ("priority", "is_active")
    search_fields = ("lesson__title", "headline")


@admin.register(PracticeQuestion)
class PracticeQuestionAdmin(admin.ModelAdmin):
    list_display = ("title", "exam", "year", "category", "difficulty", "correct_option", "is_published")
    list_filter = ("exam", "year", "difficulty", "category", "tags", "is_published")
    search_fields = ("title", "question", "solution", "formula_used")
    filter_horizontal = ("tags",)
    autocomplete_fields = ("related_lesson",)