from selenium import webdriver
from functional_tests.base_testcase import BaseTestCase
from time import sleep

class LoginTest(BaseTestCase):
    def setUp(self):
        self.loadData()
        self.home_page_url = self.live_server_url + '/forum'
        self.login_page_url = self.live_server_url + '/forum/login'
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def loadData(self):
        """Load data in database for this test"""
        pass

    # tests
    def test_user_login(self):
        browser = self.getBrowser()
        browser.get(self.getLoginpageAddress())

        uname_tb = browser.find_element_by_id('usernameTB')
        pass_tb  = browser.find_element_by_id('passwordTB')
        login_btn = browser.find_element_by_id('loginBTN')

        uname_tb.send_keys('user')
        pass_tb.send_keys('password')
        login_btn.click()

        self.fail('Test is incomplete!')

