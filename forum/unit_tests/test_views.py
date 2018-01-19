from unittest import skip

from django.test import TestCase
from forum.unit_tests.modelFactory import UserFactory
from forum.unit_tests.utility import UrlContainer, TemplateNames


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

class UserDetailTest(TestCase):
    def test_pageLoads(self):
        user = UserFactory.createUsers(1)[0]

        url = UrlContainer.getUserDetailUrl(user.pk)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    #todo implement

class RegisterTest(TestCase):
    def test_RegisterPageLoads(self):
        url = UrlContainer.getLoginPageUrl()

        resp= self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_RegisterPostValidData(self):
        pass
        #todo implement

