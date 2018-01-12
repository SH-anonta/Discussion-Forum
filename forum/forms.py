from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

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


# For forms admin site
class RegisterForm(forms.ModelForm):
    password1= forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)


    class Meta:
        model = User
        fields= ('username',)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)

        if qs.exists():
            raise forms.ValidationError('Username is unavailable')

        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return password2

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