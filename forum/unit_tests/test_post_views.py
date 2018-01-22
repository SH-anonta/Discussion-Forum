from unittest import skip

from django.test import TestCase
from django.urls import reverse

from forum.models import Post
from forum.unit_tests.utility import UrlContainer, TemplateNames
from forum.unit_tests.modelFactory import PostFactory, UserFactory, BoardFactory
from forum.utility import MarkdownToHtmlConverter


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

class CreatePostTest(TestCase):
    def setUp(self):
        self.author= UserFactory.createUser('Author', 'password')
        self.board= BoardFactory.createBoards(1)[0]

    def loginAsAuthor(self):
        success = self.client.login(username= 'Author', password= 'password')
        self.assertTrue(success)

    def sendPostRequest(self, data):
        """send request and return response"""
        url = UrlContainer.getCreatePostUrl()
        return self.client.post(url, data)

    def sendGetRequest(self):
        url = UrlContainer.getCreatePostUrl()
        data = {
            'board_id': self.board.pk,
        }

        return self.client.get(url, data)

    def getValidData(self):
        title = 'Post Title'
        content = '**Post content**'

        data = {
            'post_title' : title,
            'post_content' : content,
            'post_to_board_id' : self.board.pk,
        }

        return data

    def test_editorPageLoadsForUsers(self):
        self.loginAsAuthor()
        resp = self.sendGetRequest()
        self.assertTemplateUsed(resp, TemplateNames.create_post_editor)

    def verifyPostData(self, post, data):
        self.assertEqual(post.title, data['post_title'])
        self.assertEqual(post.content, data['post_content'])

        converted_data = MarkdownToHtmlConverter.convert(data['post_content'])
        self.assertEqual(post.content_processed, converted_data)


    def test_validData(self):
        self.loginAsAuthor()

        data = self.getValidData()
        resp = self.sendPostRequest(data)

        #1 post should be created
        post_count = Post.objects.all().count()
        self.assertEqual(post_count, 1)

        post = Post.objects.get(pk= 1)

        # validate author of the post
        self.assertEqual(post.creator, self.author.userprofile)

        self.verifyPostData(post, data)

        # after successful post creation user should be redirected to
        # the post's detail page
        self.assertRedirects(resp, UrlContainer.getPostDetailUrl(post.pk))

    # todo test for invalid data

class EditPostTest(TestCase):

    def setUp(self):
        self.author = UserFactory.createUser('Author', 'password')
        self.user = UserFactory.createUser('User', 'password')
        self.admin = UserFactory.createUser('Admin', 'password', staff=True)

        self.post = PostFactory.createPosts(1, author=self.author)[0]

        self.new_title = 'New title of post'
        self.new_content = 'New content of post'

    def getRequestData(self):
        data = {
            'post_id': self.post.pk,
            'post_title' : self.new_title,
            'post_content' : self.new_content,
            'post_to_board_id': self.post.pk,      # this is not being changed
        }

        return data

    def sendPostEditRequest(self):
        """Helper class, sends a post request to url"""

        data = self.getRequestData()
        resp = self.client.post(UrlContainer.getEditPostUrl(), data)
        return resp

    def editWasSuccessful(self):
        #IMPORTANT: get updated post object from db
        post = Post.objects.get(pk=self.post.pk)

        expected_converted_data= MarkdownToHtmlConverter.convert(self.new_content)
        post_content = post.content == self.new_content
        content_processed = post.content_processed == expected_converted_data
        post_title = post.title == self.new_title

        return post_content and content_processed and post_title

    def loginAsAuthor(self):
        loggen_in= self.client.login(username= 'Author', password='password')
        if not loggen_in:
            raise ValueError('Login failed')


    def loginAsUser(self):
        self.client.login(username= 'User', password='password')

    def loginAsAdmin(self):
        self.client.login(username='Admin', password='password')

    def test_postAuthorCanEdit(self):
        self.loginAsAuthor()

        resp = self.sendPostEditRequest()

        # edit was successful an uesr was redirected to the post's post detail page
        self.assertRedirects(resp, UrlContainer.getPostDetailUrl(self.post.pk))
        self.assertTrue(self.editWasSuccessful())


    def test_adminCanEditAnyPost(self):
        self.loginAsAdmin()

        resp = self.sendPostEditRequest()

        # edit was successful an uesr was redirected to the post's post detail page
        self.assertRedirects(resp, UrlContainer.getPostDetailUrl(self.post.pk))
        self.assertTrue(self.editWasSuccessful())

    def test_nonAuthorNonAdminCanNotEdit(self):
        self.loginAsUser()

        resp = self.sendPostEditRequest()

        # edit was unsuccessful an user was shown error msg
        self.assertFalse(self.editWasSuccessful())

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

class DeleteRestorePostTest(TestCase):
    delete_post_url = url = reverse('forum:delete_post')

    def setUp(self):
        self.post_author = UserFactory.createUser('Author', 'password')
        self.user = UserFactory.createUser('User', 'password')
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

        # login as the non admin non author of the post
        self.client.login(username= 'NonAuthor', password='password')
        resp = self.client.post(url, data)

        # initially 1 post was deleted and the delete attempt has failed
        self.assertDeletedPostCount(1)

    def test_nonAuthorNonAdminCanNotDeletePost(self):
        """
            Non Admin users should not be able to delete other user's posts
        """
        data= {
            'post_id' : self.post.pk
        }

        self.client.login(username= 'User', password= 'password')
        url = UrlContainer.getDeletePostUrl()
        resp = self.client.post(url, data)

        # initially there was 1 post, one post delete attempt should fail have
        self.assertDeletedPostCount(0)

class RecentPostListTest(TestCase):
    def setUp(self):
        self.posts = PostFactory.createPosts(2)

    def test_pageLoads(self):
        """This page should be accessible to all"""

        url = UrlContainer.getRecentPostsUrl()

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, TemplateNames.recent_posts_list)



