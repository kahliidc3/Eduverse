from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('my-courses/', views.my_courses, name='my_courses'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<slug:slug>/', views.course_detail, name='course_detail'),
    path('courses/<slug:course_slug>/modules/<int:module_id>/', views.module_detail, name='module_detail'),
    path('courses/<slug:course_slug>/modules/<int:module_id>/lessons/<int:lesson_id>/', 
         views.lesson_detail, name='lesson_detail'),
    
    # Notes endpoints
    path('courses/<slug:course_slug>/lessons/<int:lesson_id>/notes/', 
         views.save_notes, name='save_notes'),
    
    # Comments endpoints
    path('courses/<slug:course_slug>/lessons/<int:lesson_id>/comments/', 
         views.add_comment, name='add_comment'),
    
    # Quiz endpoints
    path('courses/<slug:course_slug>/lessons/<int:lesson_id>/quiz/', 
         views.submit_quiz, name='submit_quiz'),
]
