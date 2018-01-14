from datetime import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model

from forum.models import User, Board, Post, Reply
from forum.unit_tests import modelFactory


class UserTest(TestCase):
    def test_creation(self):
        modelFactory.UserFactory.createUsers(2)
        self.assertEqual(User.objects.count(), 2)

    def test_CustomUserModelIsInUse(self):
        self.assertEqual(User, get_user_model(), 'Customer User model is not in use')

    # todo write tests for invalid data handling

class BoardTest(TestCase):
    def test_creation(self):
        modelFactory.BoardFactory.createBoards(2)
        self.assertEqual(Board.objects.count(), 2)

class PostTest(TestCase):
    def test_creation(self):
        modelFactory.PostFactory.createPosts(5)
        self.assertEqual(Post.objects.count(), 5)

class ReplyTest(TestCase):
    def test_creation(self):
        modelFactory.ReplyFactory.createReplies(3)
        self.assertEqual(Reply.objects.count(), 3)

