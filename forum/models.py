from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import timedelta, datetime

# models
from forum.validators import validate_username, POST_TITLE_MAX_LEN
from forum.validators import POST_CONTENT_MAX_LEN, REPLY_CONTENT_MAX_LEN, USER_NAME_MAX_LEN

class Board(models.Model):
    title = models.CharField(max_length= POST_TITLE_MAX_LEN, unique= True)

class Post(models.Model):
    title = models.CharField(max_length= POST_TITLE_MAX_LEN)
    content = models.TextField(max_length= POST_CONTENT_MAX_LEN)
    creation_date= models.DateTimeField(auto_now_add= True, blank= True)
    deleted = models.BooleanField(default= False)

    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    board= models.ForeignKey(Board, on_delete=models.CASCADE)

    def older_than_one_day(self):
        return timezone.now() - self.creation_date > timedelta(days=1)

class Reply(models.Model):
    content = models.TextField(max_length=REPLY_CONTENT_MAX_LEN)
    creation_date= models.DateTimeField(auto_now_add= True, blank= True)
    reply_to = models.ForeignKey(Post, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)