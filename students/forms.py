from django import forms
from .models import students

class studentsForm(forms.ModelForm):
    class Meta:
        model = students
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}),
            'roll': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter roll number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'course': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter course name'}),
        }