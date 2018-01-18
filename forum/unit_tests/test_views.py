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
    def getHomePageUrl(cls):
        return reverse('forum:homepage')

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

    @classmethod
    def getDeletedPostsUrl(cls):
        return reverse('forum:deleted_posts')

class TemplateNames:
    home_page= 'forum/home_page.html'
    about_page= 'forum/about_page.html'
    login_page = 'forum/login_page.html'
    board_posts= 'forum/board_posts.html'
    user_detail = 'forum/user_detail.html'
    post_detail = 'forum/post_detail.html'
    show_message = 'forum/show_message.html'
    deleted_posts= 'forum/deleted_posts.html'
    edit_post_editor= 'forum/edit_post_editor.html'
    registration_page = 'forum/registration_page.html'
    create_post_editor= 'forum/create_post_editor.html'
    global_base_template= 'forum/global_base_template.html'
    layout_base_template= 'forum/layout_base_template.html'

class HomePageTest(TestCase):
    def test_pageLoads(self):
        url = UrlContainer.getHomePageUrl()

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'forum/home_page.html')

class LoginTest(TestCase):
    def test_pageLoads(self):
        url = UrlContainer.getLoginPageUrl()
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def loginValidData(self):
        uname = 'User'
        pw = 'password'

        UserFactory.createUser(uname, pw)

        data= {
            'username': uname,
            'password': pw,
        }

        url = UrlContainer.getLoginPageUrl()

        resp = self.client.post(url, data)

        homepage_url = UrlContainer.getHomePageUrl()

        self.assertRedirects(resp, homepage_url)
        self.assertTemplateUsed(resp,'forum/home_page.html')

    def loginInvalidData(self):
        """
            login with invalid data, should fail and user will be redirected to login page again
        """
        uname = 'User'
        pw = 'password'

        UserFactory.createUser(uname, pw)

        # intentionally invalid data
        data= {
            'username': uname,
            'password': 'wrong password',
        }

        login_url= UrlContainer.getLoginPageUrl()

        resp = self.client.post(login_url, data)

        #login fails and the user is redirected to the login page
        self.assertRedirects(resp, login_url)
        self.assertTemplateUsed(resp,'forum/login_page.html')

class AboutPageTest(TestCase):
    def test_pageLoads(self):
        url = UrlContainer.getAboutPage()

        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

class PostDetailTest(TestCase):

    def setUp(self):
        self.author = UserFactory.createUser('Author', 'password')
        self.admin = UserFactory.createUser('Admin', 'password', staff=True)
        self.post= PostFactory.createPosts(1, author= self.author)[0]

    def getUrlToPost(self):
        return UrlContainer.getPostDetailUrl(self.post.pk)

    def assertPostWasLoaded(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/post_detail.html')

    def loginAsNonAdminAuthorOfPost(self):
        self.client.login(username='Author', password='password')

    def loginAsAdmin(self):
        self.client.login(username='Admin', password='password')

    def test_pageLoadsForNotLoggedInUser(self):

        #url to first post
        url = self.getUrlToPost()
        resp= self.client.get(url)

        self.assertPostWasLoaded(resp)

    def test_pageLoadsForLoggedInUser(self):
        url = self.getUrlToPost()

        # login as regular user
        self.loginAsNonAdminAuthorOfPost()

        resp= self.client.get(url)
        self.assertPostWasLoaded(resp)

    def test_deletedPostIsNotLoadedForNonAdmin(self):
        url = self.getUrlToPost()

        # delete the post to be loaded
        self.post.deleted= True
        self.post.save()

        # login as non admin user
        self.loginAsNonAdminAuthorOfPost()

        resp = self.client.get(url)

        self.assertContains(resp, 'Error: This post has been deleted.')
        self.assertTemplateUsed(resp, 'forum/show_message.html')

    def test_deletedPostIsLoadedForAdmin(self):
        """Admins should be able to view deleted posts"""

        url = self.getUrlToPost()

        # delete the post to be loaded
        self.post.deleted = True
        self.post.save()

        # login as non admin user
        self.loginAsAdmin()

        resp = self.client.get(url)

        self.assertContains(resp, self.post.content)
        self.assertTemplateUsed(resp, 'forum/post_detail.html')


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

class DeletedPostsTest(TestCase):
    
    def setUp(self):
        self.author = UserFactory.createUser('Author', 'password')
        self.admin = UserFactory.createUser('Admin', 'password', staff=True)

    def getUrlToPost(self):
        return UrlContainer.getPostDetailUrl(self.post.pk)

    def assertPostWasLoaded(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/post_detail.html')

    def loginAsNonAdminAuthorOfPost(self):
        self.client.login(username='Author', password='password')

    def loginAsAdmin(self):
        self.client.login(username='Admin', password='password')

    def test_adminsCanViewPage(self):
        self.loginAsAdmin()
        
        url = UrlContainer.getDeletedPostsUrl()

        resp = self.client.get(url)
        self.assertTemplateUsed(resp, TemplateNames.deleted_posts)

    def test_UsersCanNotLoadPage(self):
        self.loginAsNonAdminAuthorOfPost()

        url = UrlContainer.getDeletedPostsUrl()

        resp = self.client.get(url)
        self.assertTemplateUsed(resp, TemplateNames.show_message)
        self.assertContains(resp, 'You do not have permission to view this page.')