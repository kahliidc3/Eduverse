from django import forms
from .models import Course
from users.models import CustomUser

class CourseForm(forms.ModelForm):
    instructor = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role='instructor'),
        empty_label="Select an instructor",
        widget=forms.Select(attrs={
            'class': 'form-select block w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Update the instructor queryset to show full name instead of email
        self.fields['instructor'].label_from_instance = lambda obj: f"{obj.get_full_name() or obj.username}"

    class Meta:
        model = Course
        fields = ['title', 'slug', 'description', 'category', 'instructor', 'thumbnail', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input block w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Enter course title'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-input block w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Enter URL slug'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea block w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Enter course description',
                'rows': 4
            }),
            'category': forms.Select(attrs={
                'class': 'form-select block w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
            }),
            'thumbnail': forms.FileInput(attrs={
                'class': 'form-input block w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'accept': 'image/*'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-checkbox h-4 w-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500'
            })
        }
