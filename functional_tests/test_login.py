from django.test import LiveServerTestCase
from selenium import webdriver
from time import sleep

class LoginTest(LiveServerTestCase):
    def setUp(self):
        self.home_page_url = self.live_server_url + '/forum'
        self.login_page_url = self.live_server_url + '/forum/login'
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    # Helper classes
    def getBrowser(self):
        return self.browser

    def getHomepageAddress(self):
        return self.home_page_url

    def getLoginpageAddress(self):
        return self.login_page_url

    # tests
    def test_user_login(self):
        browser = self.getBrowser()
        browser.get(self.getLoginpageAddress())

        # self.fail('Test is incomplete!')

