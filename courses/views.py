from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from .models import (
    Course, Module, Lesson, Category, UserNote, Comment,
    Quiz, QuizAttempt, QuizAnswer
)

def home(request):
    featured_courses = Course.objects.filter(is_published=True)[:6]
    return render(request, 'home.html', {
        'featured_courses': featured_courses
    })

def course_list(request):
    categories = Category.objects.all()
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q')
    
    courses = Course.objects.filter(is_published=True)
    
    if category_slug:
        courses = courses.filter(category__slug=category_slug)
    
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    return render(request, 'courses/course_list.html', {
        'categories': categories,
        'courses': courses,
        'current_category': category_slug,
        'search_query': search_query
    })

@login_required
def my_courses(request):
    # Get courses where the user is enrolled
    enrolled_courses = Course.objects.filter(students=request.user)
    
    # If user is an instructor, also get their created courses
    if request.user.role == 'instructor':
        teaching_courses = Course.objects.filter(instructor=request.user)
    else:
        teaching_courses = Course.objects.none()
    
    context = {
        'enrolled_courses': enrolled_courses,
        'teaching_courses': teaching_courses,
    }
    return render(request, 'courses/my_courses.html', context)

def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    modules = course.modules.all().order_by('order')
    
    # Get course statistics
    total_lessons = sum(module.lessons.count() for module in modules)
    total_students = course.students.count()
    
    # Get average rating safely
    try:
        avg_rating = course.reviews.aggregate(avg_rating=models.Avg('rating'))['avg_rating'] or 0
    except:
        avg_rating = 0
    
    # Get user progress if authenticated
    user_progress = None
    if request.user.is_authenticated:
        user_progress, _ = request.user.progress.get_or_create(course=course)
    
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'modules': modules,
        'total_lessons': total_lessons,
        'total_students': total_students,
        'avg_rating': avg_rating,
        'user_progress': user_progress
    })

@login_required
def module_detail(request, course_slug, module_id):
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    module = get_object_or_404(Module, id=module_id, course=course)
    lessons = module.lessons.all().order_by('order')
    
    # Get user progress
    user_progress, _ = request.user.progress.get_or_create(course=course)
    completed_lessons = user_progress.completed_lessons.filter(module=module)
    
    return render(request, 'courses/module_detail.html', {
        'course': course,
        'module': module,
        'lessons': lessons,
        'completed_lessons': completed_lessons
    })

@login_required
def lesson_detail(request, course_slug, module_id, lesson_id):
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    module = get_object_or_404(Module, id=module_id, course=course)
    lesson = get_object_or_404(Lesson, id=lesson_id, module=module)
    
    # Get user progress and notes
    user_progress, _ = request.user.progress.get_or_create(course=course)
    user_notes = UserNote.objects.filter(user=request.user, lesson=lesson).first()
    
    # Get quiz information if it exists
    quiz_attempt = None
    if hasattr(lesson, 'quiz'):
        quiz_attempt = QuizAttempt.objects.filter(
            user=request.user,
            quiz=lesson.quiz
        ).first()
    
    # Get next and previous lessons
    next_lesson = Lesson.objects.filter(
        module=module,
        order__gt=lesson.order
    ).order_by('order').first()
    
    prev_lesson = Lesson.objects.filter(
        module=module,
        order__lt=lesson.order
    ).order_by('-order').first()
    
    # Handle lesson completion
    if request.method == 'POST' and 'complete_lesson' in request.POST:
        if lesson not in user_progress.completed_lessons.all():
            user_progress.completed_lessons.add(lesson)
            messages.success(request, f'Congratulations! You earned {lesson.points} points!')
        return redirect('courses:lesson_detail', course_slug=course.slug, module_id=module.id, lesson_id=lesson.id)
    
    # Calculate progress percentage
    total_lessons = module.lessons.count()
    completed_count = user_progress.completed_lessons.filter(module=module).count()
    progress = (completed_count / total_lessons) * 100 if total_lessons > 0 else 0
    
    return render(request, 'courses/lesson_detail.html', {
        'course': course,
        'module': module,
        'lesson': lesson,
        'user_notes': user_notes,
        'quiz_attempt': quiz_attempt,
        'next_lesson': next_lesson,
        'prev_lesson': prev_lesson,
        'progress': progress,
        'comments': lesson.comments.filter(parent=None)  # Only top-level comments
    })

@login_required
def save_notes(request, course_slug, lesson_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course__slug=course_slug)
    content = request.POST.get('notes', '').strip()
    
    if content:
        note, created = UserNote.objects.update_or_create(
            user=request.user,
            lesson=lesson,
            defaults={'content': content}
        )
        messages.success(request, 'Notes saved successfully!')
    else:
        UserNote.objects.filter(user=request.user, lesson=lesson).delete()
        messages.info(request, 'Notes cleared successfully!')
    
    return redirect('courses:lesson_detail', course_slug=course_slug, module_id=lesson.module.id, lesson_id=lesson_id)

@login_required
def add_comment(request, course_slug, lesson_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course__slug=course_slug)
    content = request.POST.get('content', '').strip()
    parent_id = request.POST.get('parent_id')
    
    if not content:
        messages.error(request, 'Comment cannot be empty!')
        return redirect('courses:lesson_detail', course_slug=course_slug, module_id=lesson.module.id, lesson_id=lesson_id)
    
    parent = None
    if parent_id:
        parent = get_object_or_404(Comment, id=parent_id, lesson=lesson)
    
    Comment.objects.create(
        user=request.user,
        lesson=lesson,
        content=content,
        parent=parent
    )
    
    messages.success(request, 'Comment added successfully!')
    return redirect('courses:lesson_detail', course_slug=course_slug, module_id=lesson.module.id, lesson_id=lesson_id)

@login_required
def submit_quiz(request, course_slug, lesson_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course__slug=course_slug)
    
    if not hasattr(lesson, 'quiz'):
        messages.error(request, 'This lesson does not have a quiz!')
        return redirect('courses:lesson_detail', course_slug=course_slug, module_id=lesson.module.id, lesson_id=lesson_id)
    
    # Check if user has already completed the quiz
    existing_attempt = QuizAttempt.objects.filter(user=request.user, quiz=lesson.quiz).first()
    if existing_attempt:
        messages.info(request, 'You have already completed this quiz!')
        return redirect('courses:lesson_detail', course_slug=course_slug, module_id=lesson.module.id, lesson_id=lesson_id)
    
    # Process quiz answers
    total_points = 0
    total_possible = 0
    
    quiz_attempt = QuizAttempt.objects.create(
        user=request.user,
        quiz=lesson.quiz,
        score=0  # Will be updated after processing answers
    )
    
    for question in lesson.quiz.questions.all():
        total_possible += question.points
        selected_choice_id = request.POST.get(f'question_{question.id}')
        
        if selected_choice_id:
            selected_choice = get_object_or_404(Choice, id=selected_choice_id, question=question)
            QuizAnswer.objects.create(
                attempt=quiz_attempt,
                question=question,
                selected_choice=selected_choice
            )
            
            if selected_choice.is_correct:
                total_points += question.points
    
    # Calculate percentage score
    score_percentage = (total_points / total_possible * 100) if total_possible > 0 else 0
    quiz_attempt.score = score_percentage
    quiz_attempt.save()
    
    # Check if user passed the quiz
    if score_percentage >= lesson.quiz.passing_score:
        user_progress, _ = request.user.progress.get_or_create(course=lesson.module.course)
        user_progress.completed_lessons.add(lesson)
        messages.success(request, f'Congratulations! You passed the quiz with {score_percentage:.1f}% and earned {lesson.points} points!')
    else:
        messages.warning(request, f'You scored {score_percentage:.1f}%. You need {lesson.quiz.passing_score}% to pass the quiz.')
    
    return redirect('courses:lesson_detail', course_slug=course_slug, module_id=lesson.module.id, lesson_id=lesson_id)
