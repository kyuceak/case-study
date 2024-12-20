from django import forms
from django.contrib.auth.models import User
from .models import Team, Part, AIRCRAFT_CHOICES


class RegisterForm(forms.ModelForm):
    team = forms.ModelChoiceField(queryset=Team.objects.all(), required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password', 'team')


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
    )



class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = ['type', 'aircraft']

