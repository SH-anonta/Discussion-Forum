from unittest import skip

from selenium.common.exceptions import NoSuchElementException
from functional_tests.base_testcase import BaseTestCase
from selenium import webdriver

from forum.unit_tests.modelFactory import *
from forum.models import User
from functional_tests.page_objects import HomePage, BoardPostsPage, PostEditorPage, PostDetailPage


class BoardTest(BaseTestCase):
    def loadData(self):
        BoardFactory.createBoards(1)
        uname= 'User'
        pw= 'password'
        User.objects.create_user(username= uname, password= pw)

    def test_CreatePostButtonUnavailableWhenNotLoggedIn(self):
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
        self.assertBoardPostsPageLoaded()

        #He looks at the top right of the page and does not see any button named "New Post"
        self.assertFalse(board_posts_page.newPostButtonIsPresent())

    def test_CreatePostButtonAvalableWhenLoggedIn(self):
        browser = self.browser

        homepage= HomePage(browser)
        board_posts_page= BoardPostsPage(browser)

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
        self.assertBoardPostsPageLoaded()

        # He looks at the top right of the page and sees any button named "New Post"
        self.assertTrue(board_posts_page.newPostButtonIsPresent())

    def test_CreatePost(self):
        browser = self.browser

        homepage = HomePage(browser)
        board_posts_page = BoardPostsPage(browser)
        post_editor_page = PostEditorPage(browser)
        post_detail_page = PostDetailPage(browser)

        # The use logs in
        uname = 'User'
        pw = 'password'
        self.login(uname, pw)

        # User goes to the homepage
        browser.get(self.getHomePageAddress())
        self.assertHomepageLoaded()

        # User sees a table of boards and clicks the first one
        board_links = homepage.getBoardLinks()
        board_links[0].click()

        #The user is brought to the board's board_posts_view
        self.assertBoardPostsPageLoaded()

        #The user sees a button "New post" and clicks it
        board_posts_page.newPostButtonIsPresent()
        board_posts_page.clickNewPostButton()

        # The user is brought to the PostEditor page
        self.assertPostEditorPageLoaded()

        #User sees a form with board, post title and post content fields

        # valid post data form
        post_title = 'Post1 title'
        post_content = 'Post1 content'

        # the user sees the dropdown menu for board, is already selected to the
        # board page from which the "new post" button was clicked
        # The user leaves it unchanged

        # User Enters Post title and content
        post_editor_page.enterPostTitleField(post_title)
        post_editor_page.enterPostContentField(post_content)

        # The user then clicks the post
        post_editor_page.clickPostButton()

        # the post is submitted, and the user is redirected to the new created post's
        # post-detail page

        self.assertPostDetailPageLoaded()

        # user sees his post name and url in there
        self.assertEqual(post_title, post_detail_page.getPostTitle())
        self.assertEqual(post_content, post_detail_page.getPostContent())
