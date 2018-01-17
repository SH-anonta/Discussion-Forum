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
    def getRestorePostUrl(cls):
        return reverse('forum:restore_post')

    @classmethod
    def getLoginPageUrl(self):
        return reverse('forum:loginpage')

    @classmethod
    def getPostDetailUrl(self, post_id):
        return  reverse('forum:post_detail', args=[post_id])

    @classmethod
    def getAboutPage(cls):
        return reverse('forum:about_page')

    @classmethod
    def getRegisterPage(cls):
        return reverse('forum:registration_page')

    @classmethod
    def getUserDetailUrl(cls, user_id):
        return reverse('forum:user_detail', args=[user_id])


class HomePageTest(TestCase):
    def test_pageLoads(self):
        homepage = HomePage()
        resp = homepage.get(HttpRequest())
        self.assertEqual(resp.status_code, 200)

class LoginTest(TestCase):
    def test_pageLoads(self):
        url = UrlContainer.getLoginPageUrl()
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

# class RegisterTest(TestCase):
#     def test_pageLoads(self):
#         reg = Register()
#         resp = reg.get(HttpRequest())
#         self.assertEqual(resp.status_code, 200)


class AboutPageTest(TestCase):
    def test_pageLoads(self):
        url = UrlContainer.getAboutPage()

        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

class PostDetailTest(TestCase):
    def test_pageLoads(self):
        posts= PostFactory.createPosts(5)

        #url to first post
        url = UrlContainer.getPostDetailUrl(posts[0].pk)
        resp= self.client.get(url)

        self.assertEqual(resp.status_code, 200)

class UserDetailTest(TestCase):
    def test_pageLoads(self):
        user = UserFactory.createUsers(1)[0]

        url = UrlContainer.getUserDetailUrl(user.pk)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    #todo implement

class DeleteRestorePostTest(TestCase):
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
        self.assertContains(response, 'Post deleted successfully')

        #1 post was created then deleted
        self.assertDeletedPostCount(1)

    def test_adminsCanDeleteOtherUsersPost(self):
        """Admins can delete any user's post"""
        client = self.client

        # login as author
        self.client.login(username='Admin', password='password')
        post = self.post
        data = {'post_id': post.pk}

        response = client.post(self.delete_post_url, data)

        # delete successful and admin is redirected to the post's board's board posts page
        self.assertContains(response, 'Post deleted successfully')

        # 1 post was created then deleted
        self.assertDeletedPostCount(1)

    def test_nonAdminUserCanNotRestorePost(self):

        #deleting the post initially
        self.post.deleted= True
        self.post.save()

        url = UrlContainer.getRestorePostUrl()

        data= {
            'post_id' : self.post.pk
        }

        resp = self.client.post(url, data)

        # self.assertContains(resp, 'You are not authorized to restore this post')

        # initially 1 post was deleted and the delete attempt has failed
        self.assertDeletedPostCount(1)


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

class RegisterTest(TestCase):
    def test_RegisterPageLoads(self):
        url = UrlContainer.getLoginPageUrl()

        resp= self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_RegisterPostValidData(self):
        pass
        #todo implement