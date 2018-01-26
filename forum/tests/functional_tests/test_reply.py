from forum.tests.functional_tests.base_testcase import BaseTestCase
from forum.tests.unit_tests.modelFactory import *
from forum.models import UserProfile

class CreateReplyTest(BaseTestCase):
    def loadData(self):
        PostFactory.createPosts(1)
        uname= 'User'
        pw= 'password'
        u= User.objects.create_user(username= uname, password= pw)
        UserProfile.objects.create(user= u)

    def test_createReply(self):
        browser = self.browser

        homepage = self.homepage
        board_posts_page = self.board_posts_page
        post_detail_page = self.post_detail_page

        uname = 'User'
        pw = 'password'
        #The user logs in
        self.login(uname, pw)

        # The user visits the homepage
        self.goToHomePage()

        # sees there is a board in the boards table
        # he clicks on the first board's link
        homepage.clickNthBoardLinkInHomePage(1)

        # the board's page loads [board posts page]
        # the sees a table of posts and clicks on the first post link
        board_posts_page.clickNthPostLink(1)

        #The user is brought to the post's detail page
        # where he can see the post's title and content and other replies
        self.assertPostDetailPageLoaded()

        #The sees a form for writing replies and enters some text
        reply_content= 'This is my reply'

        post_detail_page.enterQuickReplyTextArea(reply_content)

        # user clicks on the post button in quick reply form
        post_detail_page.clickQuickReplyPostButton()

        # the page reloads
        self.assertPostDetailPageLoaded()

        #and the user sees his post in it
        self.assertTrue(post_detail_page.pageHasReply(reply_content))

    #todo create test for trying to reply unauthorized