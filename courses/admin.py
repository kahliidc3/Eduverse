from django.contrib import admin
from .models import (
    Category, Course, Module, Lesson,
    Quiz, Question, Choice, UserNote,
    Comment, QuizAttempt, QuizAnswer, CourseEnrollment, Review
)
from .forms import CourseForm

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    form = CourseForm
    list_display = ['title', 'instructor', 'category', 'is_published', 'created_at']
    list_filter = ['is_published', 'category', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']
    list_filter = ['course']
    search_fields = ['title', 'description']
    ordering = ['course', 'order']

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'order', 'points', 'estimated_time']
    list_filter = ['module__course', 'module']
    search_fields = ['title', 'content']
    ordering = ['module', 'order']

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'passing_score']
    list_filter = ['lesson__module__course']
    search_fields = ['title', 'description']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'text', 'order', 'points']
    list_filter = ['quiz__lesson__module__course']
    search_fields = ['text']
    ordering = ['quiz', 'order']

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['question', 'text', 'is_correct']
    list_filter = ['question__quiz', 'is_correct']
    search_fields = ['text']

@admin.register(UserNote)
class UserNoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'created_at', 'updated_at']
    list_filter = ['lesson__module__course', 'user']
    search_fields = ['content']
    date_hierarchy = 'created_at'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'created_at', 'parent']
    list_filter = ['lesson__module__course', 'user']
    search_fields = ['content']
    date_hierarchy = 'created_at'

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'completed_at']
    list_filter = ['quiz__lesson__module__course', 'user']
    date_hierarchy = 'completed_at'

@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'question', 'selected_choice']
    list_filter = ['attempt__quiz', 'question']
