from django import forms
from django.core.exceptions import ValidationError

from forum import validators


class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        validators=[
            validators.validate_username,
        ],
    )
    email = forms.EmailField(
        validators=[
            validators.validate_email,
        ],
    )

    password = forms.CharField(

        validators=[
            validators.validate_password,
        ],
    )

    confirm_password  = forms.CharField(
        validators=[
            validators.validate_password,
        ],
    )

    def clean_confirm_password(self):
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            raise ValidationError('Passwords do not match')
