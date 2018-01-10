from django.test import TestCase
from forum.models import User

class UserTest(TestCase):
    def test_creation(self):
        uname = 'user'
        pw= 'password'

        u = User(username= uname)
        u.set_password(pw)

        u.save()




