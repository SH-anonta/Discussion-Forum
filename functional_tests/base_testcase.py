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
        """Load data in database for this test"""
        pass

    # Helper classes
    def getBrowser(self):
        return self.browser

    def getHomepageAddress(self):
        return self.home_page_url

    def getLoginpageAddress(self):
        return self.login_page_url