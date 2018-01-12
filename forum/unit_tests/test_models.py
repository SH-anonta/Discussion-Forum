from datetime import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model

from forum.models import User, Board, Post, Reply


class UserTest(TestCase):
    def test_creation(self):
        uname = 'user'
        pw= 'password'

        u = User(username= uname)
        u.set_password(pw)

        u.save()

        self.assertEqual(User.objects.count(), 1)

    def test_CustomUserModelIsInUse(self):
        self.assertEqual(User, get_user_model(), 'Customer User model is not in use')

    # todo write tests for invalid data handling

class BoardTest(TestCase):
    def test_creation(self):
        Board.objects.create(title='Announcements')
        Board.objects.create(title='General Discussion')
        self.assertEqual(Board.objects.count(), 2)

class PostTest(TestCase):
    def test_creation(self):
        user= User.objects.create_user(username='User', password='password')
        board= Board.objects.create(title='Announcements')

        post = Post.objects.create(creator= user, title='Summer break', content= 'title', board= board)

        self.assertEqual(Post.objects.count(), 1)

        # check default values
        self.assertEqual(post.deleted, False)
        self.assertEqual(post.creator, user)
        self.assertEqual(post.board, board)

class ReplyTest(TestCase):
    def test_creation(self):
        user = User.objects.create_user(username='User', password='password')
        board = Board.objects.create(title='Announcements')

        post = Post.objects.create(creator=user, title='Summer break', content='title', board=board)

        reply = Reply.objects.create(content = 'Good post,', reply_to= post, creator= user)

        self.assertEqual(Reply.objects.count(), 1)

