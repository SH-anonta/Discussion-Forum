from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

# This class is to be inherited, don't put test code in here
class BaseTestCase(StaticLiveServerTestCase):
    """Host common helper methods and setup, tear down code"""

    def setUp(self):
        self.loadData()
        self.home_page_url = self.live_server_url + '/forum'
        self.login_page_url = self.live_server_url + '/forum/login'
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    # Helper methods
    def loadData(self):
        """Load data in database for each test"""
        pass

    def getBrowser(self):
        return self.browser

    def getHomepageAddress(self):
        return self.home_page_url

    def getLoginpageAddress(self):
        return self.login_page_url

    def assertHomepageLoaded(self):
        """test if he browser is currently in the homepage"""
        self.assertTrue(self.getHomepageAddress() in self.browser.current_url)

    def assertLoginPageLoaded(self):
        """test if he browser is currently in the login page"""
        self.assertTrue(self.getLoginpageAddress() in self.browser.current_url)

    def login(self, uname, pw):
        # User opens browser and goes to the login page
        browser = self.getBrowser()
        browser.get(self.getLoginpageAddress())

        # The user sees a login
        uname_tb = browser.find_element_by_id('usernameTB')
        pass_tb = browser.find_element_by_id('passwordTB')
        login_btn = browser.find_element_by_id('loginBTN')

        # The user enters valid username and password then clicks on login button
        uname_tb.send_keys(uname)
        pass_tb.send_keys(pw)
        login_btn.click()