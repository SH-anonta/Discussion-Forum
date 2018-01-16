from datetime import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model

from forum.models import User, Board, Post, Reply
from forum.unit_tests import modelFactory
from forum.unit_tests.modelFactory import BoardFactory, PostFactory


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

    def testPostCount(self):
        """
            test that board models return correct number of post they contain
            important count excludes deleted posts (posts with field deleted=True)
        """
        board = BoardFactory.createBoards(1)[0]

        # create 5 posts in this board
        posts = PostFactory.createPosts(5, board= board)

        self.assertEqual(board.postCount(), 5)

        # let's delete 2 posts
        posts[0].deleted= True
        posts[0].save()
        posts[1].deleted= True
        posts[1].save()


        self.assertEqual(board.postCount(), 3)


class PostTest(TestCase):
    def test_creation(self):
        modelFactory.PostFactory.createPosts(5)
        self.assertEqual(Post.objects.count(), 5)

class ReplyTest(TestCase):
    def test_creation(self):
        modelFactory.ReplyFactory.createReplies(3)
        self.assertEqual(Reply.objects.count(), 3)

