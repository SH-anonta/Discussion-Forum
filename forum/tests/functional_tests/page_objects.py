# This file hosts all the page object classes of site
from selenium import webdriver
from selenium.webdriver.common.alert import Alert


class HomePage:
    def __init__(self, web_driver):
        self.browser= web_driver

    def getBoardLinks(self):
        return self.browser.find_elements_by_class_name('BoardLink')

    def clickNthBoardLinkInHomePage(self, n):
        """
            Click the n-th link in
            here n starts from 1
        """
        board_links = self.getBoardLinks()
        board_links[n-1].click()


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

    def getPostLinks(self):
        return self.browser.find_elements_by_class_name('PostLink')

    def clickNthPostLink(self, n):
        """
            n starts from 1
        """
        post_links = self.getPostLinks()
        post_links[n-1].click()

    def deletePostButtonIsAvailable(self):
        buttons= self.browser.find_elements_by_id('DeletePostBTN')
        return len(buttons) != 0

    def restorePostButtonIsAvailable(self):
        buttons= self.browser.find_elements_by_id('RestorePostBTN')
        return len(buttons) != 0

class PostDetailPage:
    def __init__(self, web_driver):
        self.browser= web_driver

    def getPostTitle(self):
        return self.browser.find_element_by_id('PostTitle').text

    def getPostContent(self):
        return self.browser.find_element_by_id('PostContentDIV').text

    def quickReplyFormIsAvailable(self):
        reply_text_areas= self.browser.find_elements_by_id('QuickReplyTA')
        return len(reply_text_areas) != 0

    def enterQuickReplyTextArea(self, content):
        reply_text_area = self.browser.find_element_by_id('QuickReplyTA')
        reply_text_area.send_keys(content)

    def clickQuickReplyPostButton(self):
        btn= self.browser.find_element_by_id('QuickReplySubmitBTN')
        btn.click()

    def pageHasReply(self, content):
        return content in self.browser.page_source

    def deletePostButtonIsAvailable(self):
        delete_post_btns = self.browser.find_elements_by_id('DeletePostBTN')
        return len(delete_post_btns) != 0

    def clickDeletePostButton(self):
        button = self.browser.find_element_by_id('DeletePostBTN')
        button.click()

    def clickYesOnConfirmPostDeleteDialogue(self):
        alert = self.browser.switch_to.alert
        alert.accept()

        # todo accept does not work for some reason
        # ff= webdriver.Firefox()
        # al = ff.switch_to.alert()
        # Alert(self.browser).accept()

    def editButtonAvailable(self):
        return self.browser.find_elements_by_id('EditPostBTN') != 0

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
        e = c.find_element_by_class_name('')
