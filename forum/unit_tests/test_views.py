from unittest import skip

from django.http import HttpRequest
from django.test import TestCase

from forum.models import Post
from forum.unit_tests.modelFactory import PostFactory, UserFactory
from forum.views import HomePage, Login, Register, AboutPage, PostDetail, DeletePost, RestorePost, EditPost


class HomePageTest(TestCase):
    def test_pageLoads(self):
        homepage = HomePage()
        resp = homepage.get(HttpRequest())
        self.assertEqual(resp.status_code, 200)

@skip   #todo fix this test
class LoginTest(TestCase):
    def test_pageLoads(self):
        login = Login()
        resp = login.get(HttpRequest())
        self.assertEqual(resp.status_code, 200)

# class RegisterTest(TestCase):
#     def test_pageLoads(self):
#         reg = Register()
#         resp = reg.get(HttpRequest())
#         self.assertEqual(resp.status_code, 200)


class AboutPageTest(TestCase):
    def test_pageLoads(self):
        view = AboutPage()

        resp = view.get(HttpRequest())
        self.assertEqual(resp.status_code, 200)

class PostDetailTest(TestCase):
    def test_pageLoads(self):
        view = PostDetail()
        # todo implement

class UserDetailTest(TestCase):
    def test_pageLoads(self):
        pass
    #todo implement


class DeletePostTest(TestCase):
    def test_view(self):
        """
            Test that by sending a valid post id
            the post with said id gets deleted
        """

        posts = PostFactory.createPosts(1)

        view = DeletePost()

        req = HttpRequest()
        req.POST['post_id']= 1  # delete the post with id= 1
        req.method = 'POST'

        view.post(req)

        p= Post.objects.get(pk= 1)
        self.assertTrue(p.deleted)


class RestorePostTest(TestCase):
    def test_view(self):
        """
            Test that by sending a valid post id
            the post with said id gets deleted
        """

        PostFactory.createPosts(1)

        view = RestorePost()

        req = HttpRequest()
        req.POST['post_id']= 1  # delete the post with id= 1
        req.method = 'POST'

        view.post(req)

        p= Post.objects.get(pk= 1)
        self.assertFalse(p.deleted)

class EditPostTest(TestCase):

    def setUp(self):
        self.author = UserFactory.createUsers(1)[0]
        self.admin = UserFactory.createUsers(1, staff=True)[0]

        self.post = PostFactory.createPosts(1, user= self.author)

    def test_pageLoadsForPostAuthor(self):
        post= self.post
        # author = self.author
        # admin = self.admin
        #
        # view = EditPost()
        # req = HttpRequest()
        # req.GET['post_id']= post.pk
        #
        # view.get()

        # todo fix tests