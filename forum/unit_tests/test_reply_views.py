from unittest import skip

from django.test import TestCase

from forum.models import Reply
from forum.unit_tests.modelFactory import PostFactory, UserFactory, ReplyFactory
from forum.unit_tests.utility import UrlContainer, TemplateNames
from forum.utility import MarkdownToHtmlConverter


class CreateReplyTest(TestCase):
    def setUp(self):
        self.user = UserFactory.createUser('User', 'password')

    def loginAsUser(self):
        succes = self.client.login(username='User', password= 'password')
        self.assertTrue(succes)

    def getValidData(self):
        post = PostFactory.createPosts(1)[0]

        data ={
            'reply_to_post_pk': post.pk,
            'content' : 'random text goes here'
        }

        return data

    def sendPostRequestToCreateReply(self, data):
        url = UrlContainer.getCreateReplyUrl()
        self.client.post(url, data)

    def assertReplyCreationSuccessful(self, data):
        #only one reply should have been crated
        self.assertTrue(Reply.objects.count(), 1)

        reply = Reply.objects.get(pk=1)
        self.assertEqual(reply.content, data['content'])

        expected_data = MarkdownToHtmlConverter.convert(data['content'])
        self.assertEqual(reply.content_processed, expected_data)
        self.assertEqual(reply.creator.pk, self.user.pk)

    def test_userCanCreateReply(self):
        self.loginAsUser()
        data= self.getValidData()
        self.sendPostRequestToCreateReply(data)
        self.assertReplyCreationSuccessful(data)

    # todo text for invalid data

class DeleteReplyTest(TestCase):

    def setUp(self):
        self.author = UserFactory.createUser('Author', 'password')
        self.user = UserFactory.createUser('User', 'password')
        self.admin = UserFactory.createUser('Admin', 'password', staff=True)

        self.reply = ReplyFactory.createReplies(1, user=self.author)[0]

    @property
    def request_data(self):
        data = {'reply_id': 1}
        return data

    def test_replyAuthorCanDelete(self):
        self.client.login(username='Author', password='password')
        url = UrlContainer.getDeleteReplyUrl()

        resp = self.client.post(url, self.request_data)

        # one reply was created and it's author deleted it
        self.assertEqual(Reply.objects.count(), 0)

        # after successful delete, user should be redirected to the post(that contained the reply)
        self.assertRedirects(resp, UrlContainer.getPostDetailUrl(self.reply.reply_to.pk))

    def test_adminCanDeleteAnyReply(self):
        self.client.login(username='Admin', password='password')
        url = UrlContainer.getDeleteReplyUrl()

        resp = self.client.post(url, self.request_data)

        # one reply was created and the admin deleted it
        self.assertEqual(Reply.objects.count(), 0)

        # after successful delete, the admin should be redirected to the post(that contained the reply)
        self.assertRedirects(resp, UrlContainer.getPostDetailUrl(self.reply.reply_to.pk))

    def test_nonAuthorNonAdminCanNotDelete(self):
        self.client.login(username='User', password='password')
        url = UrlContainer.getDeleteReplyUrl()

        resp = self.client.post(url, self.request_data)

        # one reply was created and non author, non admin tried to delete it but failed
        self.assertEqual(Reply.objects.count(), 1)

        # after unsuccessful delete, user should be shown an "you dont have permission message"
        self.assertTemplateUsed(resp, TemplateNames.show_message)

class EditReplyTest(TestCase):
    def setUp(self):
        # only user1's reply will be edited, everyone will attempt to edit it
        self.user1 = UserFactory.createUser('user1', 'password')
        self.user2 = UserFactory.createUser('User2', 'password')
        self.admin = UserFactory.createUser('Admin', 'password', staff=True)

        self.reply = ReplyFactory.createReplies(1, user=self.user1)[0]

    def loginAsUser1(self):
        success = self.client.login(username='User1', password='password')
        self.assertTrue(success)

    def loginAsUser2(self):
        success = self.client.login(username='User2', password='password')
        self.assertTrue(success)

    def loginAsAdmin(self):
        success = self.client.login(username='Admin', password='password')
        self.assertTrue(success)

    # for get requests

    # for post requests
    def getFormDataToEditUser1Reply(self):
        data = {
            'reply_id': 1
        }

        return data

    def test_adminCanEditUser1Reply(self):
        pass

    def test_user1canEditOwnReply(self):
        self.client.login(username='Admin', password='password')
        pass

    def test_user2CanNotEditUser1Reply(self):
        pass