from unittest import skip
from django.test import TestCase
from django.contrib.auth.models import User

from forum.unit_tests.modelFactory import UserFactory, PostFactory
from forum.unit_tests.utility import UrlContainer, TemplateNames

class UserDetailTest(TestCase):
    def test_pageLoads(self):
        user = UserFactory.createUsers(1)[0]

        url = UrlContainer.getUserDetailUrl(user.pk)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, TemplateNames.user_detail)


class EditUserProfileTest(TestCase):
    def setUp(self):
        self.admin = UserFactory.createUser('Admin', 'password', staff=True)
        #only user1's profile will be changed, everyone will attempt to change it
        self.user1 = UserFactory.createUser('User1', 'password')
        self.user2 = UserFactory.createUser('User2', 'password')

    def loginAsAdmin(self):
        success = self.client.login(username='Admin', password='password')
        self.assertTrue(success)

    def loginAsUser1(self):
        success = self.client.login(username='User1', password='password')
        self.assertTrue(success)

    def loginAsUser2(self):
        success = self.client.login(username='User2', password='password')
        self.assertTrue(success)

    def sendGetRequestToEditUser1(self):
        url = UrlContainer.getEditUserProfileUrl(self.user1.pk)
        return self.client.get(url)

    def getValidFormData(self):
        data = {
            'email': 'newEmail@email.com',
            'new_password': 'newpassword',
            'confirm_password': 'newpassword',
        }

        return data

    def sendPostRequestToEditUser1Email(self, data):

        url = UrlContainer.getEditUserProfileUrl(self.user1.pk)
        return self.client.post(url, data)

    def user1EditWasSuccessful(self, data):
        """test post request edits the user's profile"""

        # get updated user object from db
        self.user1 = User.objects.get(pk= self.user1.pk)

        pw_changed= self.user1.check_password(data['new_password'])
        email_changed = self.user1.email == data['email']

        return pw_changed and email_changed

    # get request tests
    def test_editorPageLoadsForAdmin(self):
        """Admin should be able to access editor to edit User1's account"""
        self.loginAsAdmin()

        resp = self.sendGetRequestToEditUser1()

        self.assertTemplateUsed(resp, TemplateNames.user_profile_editor)

    def test_editorPageLoadsForProfileOwner(self):
        """User1 should be able to access editor page when trying to edit his own account"""
        self.loginAsUser1()

        resp = self.sendGetRequestToEditUser1()

        self.assertTemplateUsed(resp, TemplateNames.user_profile_editor)

    def test_editorPageDoesNotLoadForUser2(self):
        """User2 should not be able to access editor page when trying to edit User1's profile"""
        self.loginAsUser2()

        resp = self.sendGetRequestToEditUser1()

        # User2 is shown message that he does not have permission to edit profiles
        self.assertTemplateUsed(resp, TemplateNames.show_message)

    # post request tests
    def test_AdminCanEditProfiles(self):
        self.loginAsAdmin()

        data = self.getValidFormData()
        resp= self.sendPostRequestToEditUser1Email(data)

        self.assertTrue(self.user1EditWasSuccessful(data))

        # edit was successful and user is redirected to the edited user profile's detail page
        self.assertRedirects(resp, UrlContainer.getUserDetailUrl(self.user1.pk))

    def test_user1CanEditOwnProfile(self):
        self.loginAsUser1()

        data = self.getValidFormData()
        resp = self.sendPostRequestToEditUser1Email(data)

        self.assertTrue(self.user1EditWasSuccessful(data))

        # edit was successful and user is redirected to the edited user profile's detail page
        self.assertRedirects(resp, UrlContainer.getUserDetailUrl(self.user1.pk))

    def test_user2CanNotEditUser1Profile(self):
        """non admin users should not be able to edit other user's profiles"""

        self.loginAsUser2()

        data = self.getValidFormData()
        resp = self.sendPostRequestToEditUser1Email(data)

        self.assertFalse(self.user1EditWasSuccessful(data))

        # edit was unsuccessful and user shown you don't have permission message
        self.assertTemplateUsed(resp, TemplateNames.show_message)

    #todo test for invalid data


class UserListTest(TestCase):
    def setUp(self):
        self.posts = PostFactory.createPosts(5)

    def test_PageLoads(self):
        """page should load for anyone"""

        # not logged in,

        url = UrlContainer.getRecentPostsUrl()
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, TemplateNames.recent_posts_list)
