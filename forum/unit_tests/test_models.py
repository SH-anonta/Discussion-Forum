from django.test import TestCase
from django.contrib.auth import get_user_model

from forum.models import User

class UserTest(TestCase):
    def test_creation(self):
        uname = 'user'
        pw= 'password'

        u = User(username= uname)
        u.set_password(pw)

        u.save()


    def test_CustomUserModelIsInUse(self):
        self.assertEqual(User, get_user_model(), 'Customer User model is not in use')

