from unittest import skip

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
import re

# This class is to be inherited, don't put test code in here
class BaseTestCase(StaticLiveServerTestCase):
    """Host common helper methods and setup, tear down code"""

    def setUp(self):
        self.loadData()
        self.home_page_url = self.live_server_url + reverse('forum:homepage')
        self.login_page_url = self.live_server_url + reverse('forum:loginpage')
        self.registeration_page_url = self.live_server_url + reverse('forum:registration_page')
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    # Helper methods
    def loadData(self):
        """Load data in database for each test
            This is the first thing setUp() calls"""
        pass

    def getBrowser(self):
        return self.browser

    # helpers: Location getters
    def getHomePageAddress(self):
        return self.home_page_url

    def getLoginPageAddress(self):
        return self.login_page_url

    def getRegisterPageAddress(self):
        return self.registeration_page_url

    # helpers: custom asserts
    def assertHomepageLoaded(self):
        """test if he browser is currently in the homepage"""
        self.assertTrue(self.getHomePageAddress() in self.browser.current_url)

    def assertLoginPageLoaded(self):
        """test if he browser is currently in the login page"""
        self.assertTrue(self.getLoginPageAddress() in self.browser.current_url)

    def aseertBoardPostsPageLoaded(self):
        """test if he browser is currently in the Board posts page"""
        # self.assertTrue(self.getBoardPostsPageAddress() in self.browser.current_url)

        #url pattern of board posts page url
        pattern = 'https?://[0-9a-zA-Z.]+:\d+/forum/board/\d+'
        self.assertRegex(self.browser.current_url, pattern)


    def login(self, uname, pw):
        # User opens browser and goes to the login page
        browser = self.getBrowser()
        browser.get(self.getLoginPageAddress())

        # The user sees a login
        uname_tb = browser.find_element_by_id('usernameTB')
        pass_tb = browser.find_element_by_id('passwordTB')
        login_btn = browser.find_element_by_id('loginBTN')

        # The user enters valid username and password then clicks on login button
        uname_tb.send_keys(uname)
        pass_tb.send_keys(pw)
        login_btn.click()