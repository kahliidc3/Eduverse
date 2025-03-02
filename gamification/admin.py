from django.contrib import admin
from .models import Badge, UserBadge, Achievement, UserAchievement, Point

# Register your models here.

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'icon', 'required_points']
    search_fields = ['name', 'description']
    list_filter = ['required_points']

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'awarded_at']
    list_filter = ['badge', 'awarded_at']
    search_fields = ['user__username', 'user__email']
    date_hierarchy = 'awarded_at'

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'points_reward']
    search_fields = ['name', 'description']
    list_filter = ['points_reward']

@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'achievement', 'achieved_at']
    list_filter = ['achievement', 'achieved_at']
    search_fields = ['user__username', 'user__email']
    date_hierarchy = 'achieved_at'

@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    list_display = ['user', 'points', 'action', 'created_at']
    list_filter = ['action', 'created_at']
    search_fields = ['user__username', 'user__email', 'action']
    date_hierarchy = 'created_at'
