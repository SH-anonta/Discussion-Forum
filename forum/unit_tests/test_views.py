from django.http import HttpRequest
from django.test import TestCase
from forum.views import HomePage

class HomePageTest(TestCase):
    def test_pageLoads(self):
        homepage = HomePage()
        resp = homepage.get(HttpRequest())
        self.assertEqual(resp.status_code, 200)
