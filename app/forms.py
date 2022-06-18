from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from app.models import Profile, Question


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_password(self):
        data = self.cleaned_data['password']
        if len(data) < 3:
            raise ValidationError("Password length must be > 3 characters")

        return data


class QuestionForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Question
        fields = '__all__'


class SignUpForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'required': True})
        self.fields['last_name'].widget.attrs.update({'required': True})
        self.fields['username'].widget.attrs.update({'required': True})
        self.fields['email'].widget.attrs.update({'required': True})
        self.fields['password'].widget.attrs.update({'required': True}) # TODO: сделать незаметным ввод пароля

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

    # def clean(self):

    class Meta:
        model = Profile
        fields = '__all__'


class EditProfile(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Profile
        fields = '__all__'
