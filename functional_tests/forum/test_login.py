from functional_tests.forum.base_testcase import BaseTestCase
from unittest import skip
from time import sleep

from forum.models import User

class LoginTest(BaseTestCase):

    # helper methods
    def loadData(self):
        """Load data in database for this test"""
        u = User(username= 'User')
        u.set_password('password')
        u.save()

    # tests
    def test_user_login_logout(self):
        """Simple login and then logout test"""

        # User logs in using valid username and password
        uname = 'User'
        pw = 'password'
        self.login(uname, pw)

        browser = self.getBrowser()

        # login is successful and user is redirected to the home page
        self.assertHomepageLoaded()

        # the user can see there is a logout link in the header of the page
        logout_link= browser.find_element_by_id('logoutLNK')
        self.assertTrue('Logout' in logout_link.text)

        # the user clicks the link and
        logout_link.click()

        # The user is logged out and is redirected to the homepage
        # Where he can see the login link
        login_link = browser.find_element_by_id('loginLNK')
        self.assertTrue('Login' in login_link.text)

    def test_login_fail(self):
        """
            Story: User tries to login with invalid data
            the form page reloads and he sees "Login failed" message
        """
        browser = self.browser

        # user tries to login using wrong username and password
        uname = 'NONAME'    # intentionally wrong login data
        pw = 'wrongpw!'     # intentionally wrong login data
        self.login(uname, pw)

        # lhe login fails and the user is shown the login page again
        self.assertLoginPageLoaded()

        # and he sees the message 'Login failed' near the form
        self.assertTrue('Login failed' in browser.page_source)

        # The user tries to login again, but this time with valid username and wrong password
        uname = 'NONAME'  # valid login data
        pw = 'wrongpw!'  # intentionally wrong login data
        self.login(uname, pw)

        # lhe login fails and the user is shown the login page again
        self.assertLoginPageLoaded()
        # and he sees the message 'Login failed' near the form
        self.assertTrue('Login failed' in browser.page_source)

    def test_relogin_attempt(self):
        """
            Story: User logs in successfully then tries to login again,
            but is redirected to homepage instead of getting the login form
        """
        # User logs in using valid username and password
        uname = 'User'
        pw = 'password'
        self.login(uname, pw)

        browser = self.getBrowser()

        # login is successful and user is redirected to the home page
        self.assertHomepageLoaded()

        # User tries to go to the login page again
        browser.get(self.getLoginPageAddress())

        # but he is redirected back to homepage
        self.assertHomepageLoaded()