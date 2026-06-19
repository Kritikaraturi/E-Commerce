from django import forms
from .models import Customer
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation


class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Enter Password'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Confirm Password'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Enter Email'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email':'Email'}
        widgets = {'username': forms.TextInput(attrs={'class':'form-control'})}

class LoginForm(AuthenticationForm):
    username = UsernameField(widget = forms.TextInput(attrs={'autofocus':'True', 'class':'form-control'}))
    password = forms.CharField(label=("Password"), strip=False, widget = forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))


class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label = ("Old Password"), strip=False, widget = forms.PasswordInput(attrs={'autocomplete':'curret-password', 'autofocus':'current-password', 'class':'form-control'}))
    new_password1 = forms.CharField(label=("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}))


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['user_type', 'name', 'locality', 'city', 'state']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'locality': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
        }
        





from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'frost-input',
                'placeholder':'Username'
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class':'frost-input',
                'placeholder':'Password'
            }
        )
    )

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CustomerRegistrationForm(UserCreationForm):

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'frost-input',
            'placeholder': 'Enter Username',
            'id': 'username'
        })

        self.fields['email'].widget.attrs.update({
            'class': 'frost-input',
            'placeholder': 'Enter Email',
            'id': 'email'
        })

        self.fields['password1'].widget.attrs.update({
            'class': 'frost-input',
            'placeholder': 'Enter Password',
            'id': 'password'
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'frost-input',
            'placeholder': 'Confirm Password',
            'id': 'confirmPass'
        })