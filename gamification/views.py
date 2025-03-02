from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Badge, Achievement, Point, UserBadge, UserAchievement

# Create your views here.

@login_required
def leaderboard(request):
    # Get top users by points
    top_users = Point.objects.values('user__username').annotate(
        total_points=Sum('points')
    ).order_by('-total_points')[:10]
    
    return render(request, 'gamification/leaderboard.html', {
        'top_users': top_users
    })

@login_required
def achievements(request):
    # Get user's badges
    user_badges = UserBadge.objects.filter(user=request.user).select_related('badge')
    
    # Get user's achievements
    user_achievements = UserAchievement.objects.filter(user=request.user).select_related('achievement')
    
    # Get total points
    total_points = Point.objects.filter(user=request.user).aggregate(
        total=Sum('points')
    )['total'] or 0
    
    # Get available badges (not yet earned)
    available_badges = Badge.objects.exclude(
        id__in=user_badges.values_list('badge_id', flat=True)
    )
    
    return render(request, 'gamification/achievements.html', {
        'user_badges': user_badges,
        'user_achievements': user_achievements,
        'total_points': total_points,
        'available_badges': available_badges
    })

@login_required
def progress_overview(request):
    user_progress = UserProgress.objects.filter(user=request.user)
    
    # Calculate overall statistics
    total_courses = user_progress.count()
    completed_courses = user_progress.filter(completed_lessons__count=Course.objects.filter(
        id__in=user_progress.values_list('course_id', flat=True)
    ).annotate(total_lessons=Count('modules__lessons')).values_list('total_lessons', flat=True)
    ).count()
    
    total_points = request.user.leaderboard_set.first().points if request.user.leaderboard_set.exists() else 0
    
    # Get course progress details
    course_progress = []
    for progress in user_progress:
        total_lessons = progress.course.modules.aggregate(
            total=Count('lessons')
        )['total']
        completed_lessons = progress.completed_lessons.count()
        
        if total_lessons > 0:
            completion_percentage = (completed_lessons / total_lessons) * 100
        else:
            completion_percentage = 0
            
        course_progress.append({
            'course': progress.course,
            'completed_lessons': completed_lessons,
            'total_lessons': total_lessons,
            'completion_percentage': completion_percentage
        })
    
    return render(request, 'gamification/progress.html', {
        'total_courses': total_courses,
        'completed_courses': completed_courses,
        'total_points': total_points,
        'course_progress': course_progress
    })
