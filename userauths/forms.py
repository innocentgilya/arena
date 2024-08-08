from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User, Profile
from django.forms.widgets import ClearableFileInput



class UserRegistrationForm(UserCreationForm):
    ''' '''
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Passowrd"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}))

    class Meta:
        model = User
        fields = ['username', 'email']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'birth_date', 'profile_picture']



class ProfileCreateForm(forms.ModelForm):
    '''Create profile form'''
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Profilename"}))
    school = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "School"}))
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
        widget=forms.Select(attrs={"class": "select-grade"})
    )

    class Meta:
        model = Profile
        fields = ['name', 'school', 'profile_picture', 'grade_level']
        widgets = {
            'profile_picture': ClearableFileInput(attrs={'class': 'form-control'}),
        }
        