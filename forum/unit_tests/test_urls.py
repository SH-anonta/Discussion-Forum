from django.test import TestCase
from django.urls import resolve
from forum.views import HomePage


class URLtoViewMappings(TestCase):
    """Test that urls map to correct views"""

    # def test_homepage(self):
    #     url = '/forum/'
    #     (resolve(url)[0], HomePage.as_view())