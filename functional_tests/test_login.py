from django.test import LiveServerTestCase
from selenium import webdriver
from time import sleep

class LoginTest(LiveServerTestCase):
    def setUp(self):
        self.home_page = self.live_server_url + '/forum'
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def getBrowser(self):
        return self.browser

    def getHomepageAddress(self):
        return self.home_page

    def test_user_login(self):
        browser = self.getBrowser()
        browser.get(self.getHomepageAddress())

        # self.fail('Test is incomplete!')

