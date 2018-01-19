from unittest import skip

from django.test import TestCase

from forum.models import Reply
from forum.unit_tests.modelFactory import PostFactory, UserFactory, ReplyFactory
from forum.unit_tests.utility import UrlContainer, TemplateNames


class CreateReplyTest(TestCase):
    #todo implement
    pass

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
        self.author = UserFactory.createUser('Author', 'password')
        self.user = UserFactory.createUser('User', 'password')
        self.admin = UserFactory.createUser('Admin', 'password', staff=True)

        self.reply = ReplyFactory.createReplies(1, user=self.author)[0]

    # todo implement
    @property
    def request_data(self):
        data = {'reply_id': 1}
        return data

    def test_replyAuthorCanDelete(self):
        pass

    def test_adminCanDeleteAnyReply(self):
        self.client.login(username='Admin', password='password')
        pass

    def test_nonAuthorNonAdminCanNotDelete(self):
        pass