from unittest import skip

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from forum.models import UserProfile
from forum.unit_tests.modelFactory import UserFactory
from forum.unit_tests.utility import UrlContainer, TemplateNames
from forum.utility import MarkdownToHtmlConverter


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
        self.assertTemplateUsed(resp, TemplateNames.about_page)

class UserDetailTest(TestCase):
    def test_pageLoads(self):
        user = UserFactory.createUsers(1)[0]

        url = UrlContainer.getUserDetailUrl(user.pk)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, TemplateNames.user_detail)

class RegisterTest(TestCase):
    def test_RegisterPageLoads(self):
        url = UrlContainer.getLoginPageUrl()

        resp= self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def sendPostRequest(self, data):
        url = UrlContainer.getRegisterPage()
        return self.client.post(url, data)

    valid_data= {
        'username' : 'UserName',
        'email' : 'username@example.com',
        'password' : 'password',
        'confirm_password' : 'password',
    }

    def verifyUserData(self, user, data):
        self.assertEqual(user.username, data['username'])
        self.assertEqual(user.email, data['email'])

    def test_RegisterPostValidData(self):
        self.sendPostRequest(self.valid_data)

        #one user account should have been created
        self.assertEqual(User.objects.count(), 1)
        #one UserProfile should be created for one uer
        self.assertEqual(UserProfile.objects.count(), 1)
        
        user = User.objects.get(username=self.valid_data['username'])
        self.assertIsNotNone(user.userprofile)
        self.verifyUserData(user, self.valid_data)

class MarkDownToHtmlTest(TestCase):
    def loginAsUser(self):
        UserFactory.createUser('User', 'password')
        self.client.login(username='User', password='password')


    def test_conversion(self):
        self.loginAsUser()

        data = """ 
                ###markdown data
                `code syntax goes here`
            > this is a block quote
            > this is another block quote
            
            [link](http://linkaddress.com)
            ![alternate text of image](http://linkaddress.com/img.jpg)
        """

        expected_data= MarkdownToHtmlConverter.convert(data)

        payload = {'md_text': data}
        resp= self.client.post(UrlContainer.getMarkDownToHtmlUrl(), payload)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(expected_data, resp.content.decode())


class EditUserProfileTest(TestCase):
    def setUp(self):
        self.admin = UserFactory.createUser('Admin', 'password', staff=True)
        self.user1 = UserFactory.createUser('User1', 'password')
        self.user2 = UserFactory.createUser('User2', 'password')

    def loginAsAdmin(self):
        self.client.login(username='Admin', password='password')

    def loginAsUser1(self):
        self.client.login(username='User1', password='password')

    def loginAsUser2(self):
        self.client.login(username='User2', password='password')

    def sendGetRequestToEditUser1(self):
        url = UrlContainer.getEditUserProfileUrl(self.user1.pk)
        return self.client.get(url)

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

    #todo implement tests for post requests

class UserListTest(TestCase):
    pass
    #todo implement

class RecentPostListTest(TestCase):
    pass
    #todo implement

