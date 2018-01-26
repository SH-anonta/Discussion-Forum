from django.contrib.auth.models import User
from django.test import TestCase

from forum.models import UserProfile
from forum.tests.unit_tests.modelFactory import UserFactory
from forum.tests.unit_tests.utility import UrlContainer, TemplateNames
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
