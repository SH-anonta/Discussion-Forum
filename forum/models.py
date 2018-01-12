from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


# models
from forum.validators import validate_username, POST_TITLE_MAX_LEN, POST_CONTENT_MAX_LEN


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
        validators=[validate_username, ],
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

class Board(models.Model):
    title = models.TextField(max_length= POST_TITLE_MAX_LEN)


class Post(models.Model):
    title = models.TextField(max_length= POST_TITLE_MAX_LEN)
    content = models.TextField(max_length= POST_CONTENT_MAX_LEN)
    creation_date= models.DateTimeField(auto_now_add= True, blank= True)
    deleted = models.BooleanField(default= False)

    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    board= models.ForeignKey(Board, on_delete=models.CASCADE)

class Reply(models.Model):
    creation_date= models.DateTimeField(auto_now_add= True, blank= True)

    reply_to = models.ForeignKey(Post, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
