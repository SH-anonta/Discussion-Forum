from forum.models import Board, Post, User
from functional_tests.base_testcase import BaseTestCase


class BoardTest(BaseTestCase):
    def loadData(self):
        u = User.objects.create_user(username= 'Adminss', password='passwordss')

        b1= Board.objects.create(title='Announcements')
        b2= Board.objects.create(title='General discussion')
        b3= Board.objects.create(title='Programming')

        post_content='Welcome new members to our community.'
        p1= Post.objects.create(title='Welcome to the community', creator=u, board=b1, content=post_content)


    def test_board(self):
        browser= self.getBrowser()

        # User goes to the homepage
        browser.get(self.getHomePageAddress())

        # user sees a table of boards, including links to the board's posts
        class_name= 'BoardLink' #class of the board links

        # The user sees 3 entries in the board table (3 boards were created in loadData method)
        links = browser.find_elements_by_class_name('BoardLink')
        self.assertEqual(len(links), 3)

        # The user clicks on the first board link

        links[0].click()

        # The user is brought to the a page that shows all the posts of the board link he clicked
        # He sees a table that shows all the posts of this board,
        # in this case here is one.

