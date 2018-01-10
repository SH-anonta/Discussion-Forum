from forum.models import User
from functional_tests.base_testcase import BaseTestCase
from time import sleep

class LoginTest(BaseTestCase):

    def loadData(self):
        """Load data in database for this test"""
        u = User(username= 'User')
        u.set_password('password')
        u.save()

    # todo refactor code

    # tests
    def test_user_login(self):
        browser = self.getBrowser()
        browser.get(self.getLoginpageAddress())

        uname_tb = browser.find_element_by_id('usernameTB')
        pass_tb  = browser.find_element_by_id('passwordTB')
        login_btn = browser.find_element_by_id('loginBTN')

        uname_tb.send_keys('User')
        pass_tb.send_keys('password')
        login_btn.click()

        self.assertTrue('User' in browser.page_source)

    # todo create test for fail
