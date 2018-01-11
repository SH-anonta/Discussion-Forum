from unittest import skip

from django.http import HttpRequest
from django.test import TestCase
from forum.views import HomePage, Login

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