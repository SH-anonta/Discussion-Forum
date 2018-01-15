from unittest import skip

from selenium.common.exceptions import NoSuchElementException
from functional_tests.base_testcase import BaseTestCase
from selenium import webdriver

from forum.unit_tests.modelFactory import *
from forum.models import User

class BoardPostsPage:
    def __init__(self, web_driver):
        self.browser= web_driver

    def newPostButtonIsPresent(self):
        new_post_buttons = self.browser.find_elements_by_id('NewPostBTN')
        return len(new_post_buttons) != 0


class HomePage:
    def __init__(self, web_driver):
        self.browser= web_driver

    def getBoardLinks(self):
        return self.browser.find_elements_by_class_name('BoardLink')

    def _dummy(self):
        #todo delete method
        c = webdriver.Chrome()

class BoardTest(BaseTestCase):
    def loadData(self):
        BoardFactory.createBoards(1)
        uname= 'User'
        pw= 'password'
        User.objects.create_user(username= uname, password= pw)

    def test_CreatePostButtonVisibleOnlyIfLoggedIn(self):
        browser = self.browser

        homepage= HomePage(browser)
        board_posts_page= BoardPostsPage(browser)

        # The user goes to the home page
        browser.get(self.getHomePageAddress())
        self.assertHomepageLoaded()

        # user sees a table of boards, there is 1 board in there
        board_links= homepage.getBoardLinks()
        self.assertEqual(len(board_links), 1)

        # The user clicks on the first link and is brought to the board's posts page
        board_links[0].click()
        self.aseertBoardPostsPageLoaded()

        #He looks at the top right of the page and does not see any button named "New Post"
        self.assertFalse(board_posts_page.newPostButtonIsPresent())

        #Now the user login
        # account created in loadData
        uname = 'User'
        pw = 'password'
        self.login(uname, pw)

        # The user goes to the home page
        browser.get(self.getHomePageAddress())
        self.assertHomepageLoaded()

        # user sees a table of boards, there is 1 board in there
        board_links = homepage.getBoardLinks()
        self.assertEqual(len(board_links), 1)

        # The user clicks on the first link and is brought to the board's posts page
        board_links[0].click()
        self.aseertBoardPostsPageLoaded()

        # He looks at the top right of the page and sees any button named "New Post"
        self.assertTrue(board_posts_page.newPostButtonIsPresent())

    def test_board(self):
        browser= self.getBrowser()

        # User goes to the homepage
        browser.get(self.getHomePageAddress())

        # user sees a table of boards, including links to the board's posts
        class_name= 'BoardLink' #class of the board links

        # The user sees 3 entries in the board table (3 boards were created in loadData method)
        links = browser.find_elements_by_class_name('BoardLink')
        self.assertEqual(len(links), 1)

        # The user clicks on the first board link

        links[0].click()

        # The user is brought to the a page that shows all the posts of the board link he clicked
        # He sees a table that shows all the posts of this board,
        # in this case here is one.

