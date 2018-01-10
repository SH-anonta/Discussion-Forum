from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models

class ModelConstraints:
    min_user_name_len= 4
    min_password_len= 8

# validators
def usernameIsValid(uname):
    if (len(uname) < ModelConstraints.min_user_name_len):
        raise ValidationError('User name can not be less than 4 characters long')

# models
class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('UserName not provided')
        if not password:
            raise ValueError('Password not provided')

        user = self.model(username= username)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_staffuser(self, username, password=None):
        user = self.create_user(username=username, password= password)
        user.staff= True
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(username=username, password=password)
        user.staff= True
        user.admin= True
        user.save(using= self._db)

        return user

class User(AbstractBaseUser):
    objects = UserManager()

    username= models.CharField(
        max_length= 20,
        unique= True,
        verbose_name= 'User Name',
        validators=[usernameIsValid,],
    )

    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __str__(self):
        return  self.username

    def has_perm(self, perm, obj=None):
        # todo do permision checking
        return True

    def has_module_perms(self, app_label):
        # todo do permision checking
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active