from unittest import skip

from django.contrib.auth import login
from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse

from forum.models import Post
from forum.unit_tests.modelFactory import PostFactory, UserFactory
from forum.views import HomePage, Login, Register, AboutPage, PostDetail, DeletePost, RestorePost, EditPost


class UrlContainer:
    @classmethod
    def getDeletePostUrl(cls):
        return reverse('forum:delete_post')

    @classmethod
    def getLoginPageUrl(self):
        return reverse('forum:loginpage')

    @classmethod
    def getPostUrl(self, post_id):
        return  reverse('forum:post_detail', args=[post_id])


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

# todo, test of views that require login are not working, fix
class AboutPageTest(TestCase):
    def test_pageLoads(self):
        view = AboutPage()

        resp = view.get(HttpRequest())
        self.assertEqual(resp.status_code, 200)

class PostDetailTest(TestCase):
    def test_pageLoads(self):
        posts= PostFactory.createPosts(5)

        #url to first post
        url = UrlContainer.getPostUrl(posts[0].pk)
        resp= self.client.get(url)

        self.assertEqual(resp.status_code, 200)

class UserDetailTest(TestCase):
    def test_pageLoads(self):
        pass
    #todo implement

class DeletePostTest(TestCase):
    delete_post_url = url = reverse('forum:delete_post')

    def setUp(self):
        self.post_author = UserFactory.createUser('Author', 'password')
        self.admin = UserFactory.createUser('Admin', 'password', staff=True)
        self.post = PostFactory.createPosts(1, author=self.post_author)[0]

    def assertDeletedPostCount(self, n):
        deleted_posts = Post.objects.filter(deleted=True).count()
        self.assertEqual(deleted_posts, n)

    def test_postAuthorCanDeletePost(self):
        """
            A user should be able to delete their own post
        """
        client = self.client

        # login as author
        self.client.login(username='Author', password= 'password')
        post = self.post
        data = {'post_id': post.pk}

        response = client.post(self.delete_post_url , data)

        # delete successful and user is redirected to the post's board's board posts page
        self.assertRedirects(response, reverse('forum:board_posts', args=[post.board.pk]))

        #1 post was created then deleted

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

        self.post = PostFactory.createPosts(1, author= self.author)

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