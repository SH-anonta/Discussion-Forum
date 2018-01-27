from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from forum import validators
from forum.models import User
from forum.validators import validate_password, validate_username


class UserRegistrationForm(forms.Form):
    username = forms.CharField(validators= [validate_username])
    email = forms.CharField()
    password = forms.CharField(validators= [validate_password])
    confirm_password = forms.CharField()

    def clean_username(self):
        if User.objects.filter(username= self.cleaned_data['username']).exists():
            raise ValueError('User name not avalable')

    def clean_confirm_password(self):
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            raise ValueError('Passwords don\'t match')

    #todo write and validators for confirm_password and email fields

class RegistrationForm(forms.Form):
    username = forms.CharField(
        validators=[
            validators.validate_username,
        ],
        max_length= validators.USER_NAME_MAX_LEN,
        widget= forms.fields.TextInput(attrs={
            'class' : 'form-control',
            'placeholder': 'User Name',
        }) 
    )
    email = forms.EmailField(
        validators=[
        ],
        max_length= validators.EMAIL_ADDRESS_NAME_MAX_LEN,
        widget= forms.fields.EmailField(attrs={
            'class' : 'form-control',
            'placeholder': 'Email',
        })
    )

    password = forms.CharField(
        validators=[
            validators.validate_password,
        ],
        max_length= validators.USER_PASSWORD_MAX_LEN,
        widget=forms.PasswordInput( attrs={
             'class': 'form-control'
        })
    )

    confirm_password  = forms.CharField(
        max_length= validators.USER_PASSWORD_MAX_LEN,
        widget=forms.PasswordInput( attrs={
             'class': 'form-control'
        })
    )

    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            raise ValueError('Passwords do not match')

    
    


class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]