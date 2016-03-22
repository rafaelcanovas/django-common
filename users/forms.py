from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm

from users.models import User


class UserSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('full_name', 'email', 'password')
        widgets = {
            'password': forms.PasswordInput()
        }

    def save(self, commit=True):
        m = super().save(commit=False)
        m.set_password(self.cleaned_data.get('password'))

        if commit:
            m.save()

        return m


class UserLoginForm(AuthenticationForm):
    pass


class UserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
