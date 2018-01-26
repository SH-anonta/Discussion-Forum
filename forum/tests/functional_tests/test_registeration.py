from forum.tests.functional_tests.base_testcase import BaseTestCase
from forum.tests.functional_tests.page_objects import RegistrationPage

class RegistrationTest(BaseTestCase):
    def loadData(self):
        pass

    def test_basicRegistration(self):
        browser = self.browser
        #Page object
        reg_page= RegistrationPage(browser)

        # user goes to the registration page
        browser.get(self.getRegisterPageAddress())

        #The page loads and he sees a registration form
        # with username, email, password and repeat password fields
        # user enters valid data to these fields

        uname = 'Fielex'
        pw = 'password'
        email= 'fielex@inlook.com'

        reg_page.enterUserName(uname)
        reg_page.enterEmail(email)
        reg_page.enterPassword(pw)
        reg_page.enterConfirmPassword(pw)

        #Then he clicks the Register button
        reg_page.clickRegisterButton()


        # Registration is successful and he is redirected to the Login page
        self.assertLoginPageLoaded()

        #He then logs in with his newly created account
        self.login(uname, pw)

        #The login is successful and he is brought the homepage
        self.assertHomepageLoaded()

        #Success!

    # todo: write test for invalid registration attempt