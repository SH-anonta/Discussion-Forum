from forum.tests.functional_tests.base_testcase import BaseTestCase
from forum.tests.unit_tests.modelFactory import *
from forum.models import UserProfile

class CreatePostTests(BaseTestCase):
    #todo add test for checking markdown converts to html correctly

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

        PostFactory.createPosts(1, author= u)

    def test_DeleteButtonUnavailableWhenNotLoggedIn(self):

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

        # the user sees a delete button at the top right
        post_detail_page.clickDeletePostButton()
        # the page shows a confirm dialogue box
        # the user clicks yes

        post_detail_page.clickYesOnConfirmPostDeleteDialogue()

        # the post is deleted and the user is redirected to the
        # board posts page of the board that contained said post

        #only one post was created (in loadData)
        # that post has been

        # todo fix test
        # deleted_post_count= Post.objects.filter(deleted=True).count()
        # self.assertEqual(deleted_post_count, 1)

class EditPostTest(BaseTestCase):

    def loadData(self):
        user1= UserFactory.createUser('Admin', 'password')
        admin= UserFactory.createUser('User1', 'password')
        user2= UserFactory.createUsers(1)

        PostFactory.createPosts(1, user1)

    def loginAsUser1(self):
        self.login('User1', 'password')

    def loginAsAdmin(self):
        self.login('Admin', 'password')

    def test_unAuthenticatedUserCanNotSeeEditButton(self):
        homepage = self.homepage
        board_posts_page = self.board_posts_page
        post_detail_page = self.post_detail_page

        # the user goes to the home page, sees list of (links to)boards
        self.goToHomePage()

        # the user clicks on the first board link
        boards = homepage.getBoardLinks()
        boards[0].click()

        # the user is sent to the board's board_posts page
        self.assertBoardPostsPageLoaded()

        #the user sees a list of (1) posts
        # first post is created by User1
        # user clicks on the first post link

        posts = board_posts_page.getPostLinks()
        posts[0].click()

        # the user is sent to the post's post detail page
        self.assertFalse(self.assertPostDetailPageLoaded())


        # the user does not see any edit button on the post
        post_detail_page.editButtonAvailable()

    #todo write test for
    # unauthenticated users doesn't see edit button
    # admins can edit other user's posts
    # users can edit their own posts
    # users can't edit other's post