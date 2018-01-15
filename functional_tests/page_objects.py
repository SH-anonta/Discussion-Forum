# This file hosts all the page object classes of site
from selenium import webdriver

class HomePage:
    def __init__(self, web_driver):
        self.browser= web_driver

    def getBoardLinks(self):
        return self.browser.find_elements_by_class_name('BoardLink')



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


class BoardPostsPage:
    def __init__(self, web_driver):
        self.browser= web_driver

    def newPostButtonIsPresent(self):
        new_post_buttons = self.browser.find_elements_by_id('NewPostBTN')
        return len(new_post_buttons) != 0

    def clickNewPostButton(self):
        new_post_button = self.browser.find_element_by_id('NewPostBTN')
        new_post_button.click()


class PostDetailPage:
    def __init__(self, web_driver):
        self.browser= web_driver

    def getPostTitle(self):
        return self.browser.find_element_by_id('PostTitle').text

    def getPostContent(self):
        return self.browser.find_element_by_id('PostContent').text

class PostEditorPage:
    def __init__(self, web_driver):
        self.browser= web_driver

    def enterPostTitleField(self, title):
        self.browser.find_element_by_id('PostTitleTB').send_keys(title)

    def enterPostContentField(self, content):
        self.browser.find_element_by_id('PostContentTA').send_keys(content)

    def clickPostButton(self):
        """click the button that submits the form"""
        button = self.browser.find_element_by_id('PostFormSubmitBTN')
        button.click()

    def _dummy(self):
        #todo delete method
        c = webdriver.Chrome()
        c.find_element_by_id('')