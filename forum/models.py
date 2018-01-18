from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import timedelta, datetime

# models
from forum.validators import validate_username, POST_TITLE_MAX_LEN
from forum.validators import POST_CONTENT_MAX_LEN, REPLY_CONTENT_MAX_LEN, USER_NAME_MAX_LEN

class UserProfile(models.Model):
    """
        IMPORTANT: A one to one mapping must be created between
        this class and from django.contrib.auth.models import User
        right after a new instance of from django.contrib.auth.models import User is
        created. or else the application will not work properly
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Board(models.Model):
    title = models.CharField(max_length= POST_TITLE_MAX_LEN, unique= True)

    def postCount(self):
        """return count of posts in this board (excluding deleted posts)"""
        return self.post_set.filter(deleted=False).count()

class Post(models.Model):
    title = models.CharField(max_length= POST_TITLE_MAX_LEN)
    content = models.TextField(max_length= POST_CONTENT_MAX_LEN)
    creation_date= models.DateTimeField(auto_now_add= True, blank= True)
    deleted = models.BooleanField(default= False)

    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    board= models.ForeignKey(Board, on_delete=models.CASCADE)

    def older_than_one_day(self):
        return timezone.now() - self.creation_date > timedelta(days=1)

    def userIsAuthorizedToEditPost(self, user):
        """Only admins and the post's author can delete posts"""
        return user.is_staff or self.creator.user == user

    def userIsAuthorizedToDeletePost(self, user):
        """Only admins and the post's author can delete posts"""
        return user.is_staff or self.creator.user == user

    def userIsAuthorizedToViewPost(self, user):
        deleted= self.deleted
        # if the post is deleted, only Admins can view it
        return not deleted or deleted and user.is_staff

class Reply(models.Model):
    content = models.TextField(max_length=REPLY_CONTENT_MAX_LEN)
    creation_date= models.DateTimeField(auto_now_add= True, blank= True)
    reply_to = models.ForeignKey(Post, on_delete=models.CASCADE)
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def userAuthorizedToDeleteReply(self, user):
        return user.is_staff or self.creator.user == user