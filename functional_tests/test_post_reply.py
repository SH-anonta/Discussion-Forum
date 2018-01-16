from time import sleep
from unittest import skip

from functional_tests.base_testcase import BaseTestCase
from forum.unit_tests.modelFactory import *
from forum.models import UserProfile

class CreatePostTests(BaseTestCase):
    def loadData(self):
        BoardFactory.createBoards(1)
        uname= 'User'
        pw= 'password'
        u= User.objects.create_user(username= uname, password= pw)
        UserProfile.objects.create(user=u)

    def test_CreatePostButtonUnavailableWhenNotLoggedIn(self):
        """
            "New thread" button in board_posts template should
            be unavailable when the user is not logged in
        """
        browser = self.browser

        homepage = self.homepage
        board_posts_page = self.board_posts_page

        # The user goes to the home page
        self.goToHomePage()

        # The user clicks on the first link and is brought to the board's posts page
        homepage.clickNthBoardLinkInHomePage(1)

        # the the browser gets the board's board posts page
        self.assertBoardPostsPageLoaded()

        #He looks at the top right of the page and does not see any button named "New Post"
        self.assertFalse(board_posts_page.newPostButtonIsPresent())

    def test_CreatePost(self):
        browser = self.browser

        homepage = self.homepage
        board_posts_page = self.board_posts_page
        post_detail_page = self.post_detail_page
        post_editor_page = self.post_editor_page

        # The use logs in
        uname = 'User'
        pw = 'password'
        self.login(uname, pw)

        # User goes to the homepage
        self.goToHomePage()

        # User sees a table of boards and clicks the first one
        homepage.clickNthBoardLinkInHomePage(1)

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

class DeletePostTest(BaseTestCase):
    def loadData(self):
        uname= 'User'
        pw= 'password'
        u = User.objects.create_user(username= uname, password= pw)
        UserProfile.objects.create(user=u)

        PostFactory.createPosts(1, user= u)

    def test_DeleteButtonUnavailableWhenNotLoggedIn(self):
        browser = self.browser

        homepage = self.homepage
        board_posts_page = self.board_posts_page
        post_detail_page = self.post_detail_page

        # The user visits the homepage
        self.goToHomePage()

        # sees there is a board in the boards table
        # he clicks on the first board's link
        homepage.clickNthBoardLinkInHomePage(1)

        # the board's page loads [board posts page]
        # the sees a table of posts and clicks on the first post link
        board_posts_page.clickNthPostLink(1)

        # The user is brought to the post's detail page
        # where he can see the post's title and content and other replies
        self.assertPostDetailPageLoaded()

        # The user want's to delete the post but realizes there is no
        # delete button since he's not logged in
        self.assertFalse(post_detail_page.deletePostButtonIsAvailable())

    def test_DeleteOwnPostSuccessful(self):
        browser = self.browser

        homepage = self.homepage
        board_posts_page = self.board_posts_page
        post_detail_page = self.post_detail_page

        # user logs in
        uname = 'User'
        pw = 'password'
        self.login(uname, pw)

        # The user visits the homepage
        self.goToHomePage()

        # the user sees list of boards and clicks the first one
        homepage.clickNthBoardLinkInHomePage(1)

        # the user is in the board's board posts page
        self.assertBoardPostsPageLoaded()

        #the user clicks on the first post link
        board_posts_page.clickNthPostLink(1)

        # the post's post detail page loads
        self.assertPostDetailPageLoaded()
