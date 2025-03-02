from django.shortcuts import render
from courses.models import Course

# Create your views here.

def home(request):
    featured_courses = Course.objects.filter(is_published=True)[:6]
    return render(request, 'core/home.html', {
        'featured_courses': featured_courses
    })

def pricing(request):
    return render(request, 'core/pricing.html')

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

def terms(request):
    return render(request, 'core/terms.html')

def privacy(request):
    return render(request, 'core/privacy.html')
