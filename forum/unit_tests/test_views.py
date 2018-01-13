from unittest import skip

from django.http import HttpRequest
from django.test import TestCase
from forum.views import HomePage, Login, Register, AboutPage, PostDetail


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


class AboutPageTest(TestCase):
    def test_pageLoads(self):
        view = AboutPage()

        resp = view.get(HttpRequest())
        self.assertEqual(resp.status_code, 200)

class PostDetailTest(TestCase):
    def test_pageLoads(self):
        view = PostDetail()
        # todo implement

class UserDetailTest(TestCase):
    def test_pageLoads(self):
        pass
    #todo implement