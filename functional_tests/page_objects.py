# This file hosts all the page object classes of site

class RegistrationPage:
    """
        A page object that hides html details of Register template from test cases
    """
    def __init__(self, webdriver):
        self.browser = webdriver

    def enterUserName(self, uname):
        tb = self.browser.find_element_by_id('UserNameTB')
        tb.send_keys(uname)

    def enterEmail(self, email):
        tb = self.browser.find_element_by_id('EmailTB')
        tb.send_keys(email)

    def enterPassword(self, pw):
        tb = self.browser.find_element_by_id('PasswordTB')
        tb.send_keys(pw)

    def enterConfirmPassword(self, pw):
        tb = self.browser.find_element_by_id('ConfirmPasswordTB')
        tb.send_keys(pw)

    def clickRegisterButton(self):
        btn = self.browser.find_element_by_id('RegisterBTN')
        btn.click()
