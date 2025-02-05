from django import forms
from userauths.models import Profile
from userauths.models import User, Profile
from django.forms.widgets import ClearableFileInput

class ProfileUpdateForm(forms.ModelForm):
        """Profile update form"""
        name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Profile.name"}))
        school = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Profile.school"}))
        grade_level = forms.ChoiceField(
        choices=[
            ('Grade 1', 'Grade 1'),
            ('Grade 2', 'Grade 2'),
            ('Grade 3', 'Grade 3'),
            ('Grade 4', 'Grade 4'),
            ('Grade 5', 'Grade 5'),
            ('Grade 6', 'Grade 6'),
            ('Grade 7', 'Grade 7'),
            ('Grade 8', 'Grade 8'),
            ('Grade 9', 'Grade 9'),
            ('Grade 10', 'Grade 10'),
            ('Grade 11', 'Grade 11'),
            ('Grade 12', 'Grade 12'),
            ('Form 1', 'Form 1'),
            ('Form 2', 'Form 2'),
            ('Form 3', 'Form 3'),
            ('Form 4', 'Form 4'),
        ],
        widget=forms.Select(attrs={"class": "select-grade", "placeholder": "Profile.grade" })
    )
        class Meta:
            model = Profile
            fields = ['name', 'school', 'profile_picture', 'grade_level']
            widgets = {
                'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
                }

