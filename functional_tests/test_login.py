from django.urls import reverse

from forum.models import User
from functional_tests.base_testcase import BaseTestCase
from time import sleep

class LoginTest(BaseTestCase):

    def loadData(self):
        """Load data in database for this test"""
        u = User(username= 'User')
        u.set_password('password')
        u.save()

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


    # tests
    def test_user_login_logout(self):
        """Simple login and logout test"""

        # User logs in using valid username and password
        uname = 'User'
        pw = 'password'
        self.login(uname, pw)

        browser = self.getBrowser()

        # login is successful and user is redirected to the home page
        self.assertTrue(self.getHomepageAddress() in browser.current_url)

        # the user can see there is a logout link in the header of the page
        logout_link= browser.find_element_by_id('logoutLNK')
        self.assertTrue('Logout' in logout_link.text)

        # the user clicks the link and
        logout_link.click()

        # The user is logged out and is redirected to the homepage
        # Where he can see the login link

        logout_link = browser.find_element_by_id('loginLNK')
        self.assertTrue('Login' in logout_link.text)

    # todo create test for invalid login

    # todo create test for relogin attemp for logged in users

    def test_relogin_attempt(self):
        """
            User logs in successfully then tries to login again,
            but is redirected to homepage instead of getting the login form
        """
        # User logs in using valid username and password
        uname = 'User'
        pw = 'password'
        self.login(uname, pw)

        browser = self.getBrowser()

        # login is successful and user is redirected to the home page
        self.assertTrue(self.getHomepageAddress() in browser.current_url)

        # User tries to go to the login page again
        browser.get(self.getLoginpageAddress())

        # but he is redirected back to homepage
        self.assertTrue(self.getHomepageAddress() in browser.current_url)