from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from app.models import Profile, Question, Answer


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_password(self):
        data = self.cleaned_data['password']
        if len(data) < 3:
            raise ValidationError("Password length must be > 3 characters")

        return data


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'required': True})
        self.fields['last_name'].widget.attrs.update({'required': True})
        self.fields['username'].widget.attrs.update({'required': True})
        self.fields['email'].widget.attrs.update({'required': True})
        self.fields['password'].widget.attrs.update({'type': 'password', 'required': True})

    def clean_username(self):
        data = self.cleaned_data['username']
        if len(data) < 5:
            raise ValidationError("Username length must be > 5 characters", code='invalid')

        return data

    def clean_password(self):
        data = self.cleaned_data['password']
        if len(data) < 3:
            raise ValidationError("Password length must be > 3 characters", code='invalid')

        return data

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


class ProfileEdit(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']


class UserEdit(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class QuestionForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Question
        fields = ['title', 'content', 'tags']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
