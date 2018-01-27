from django import forms
from forum import validators


class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        validators=[
            validators.validate_username,
        ],
    )
    email = forms.EmailField(
        validators=[
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

    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            self.errors['pw_error']= 'Passwords do not match'
            # raise ValueError('Passwords do not match')

        return cleaned_data