from forum.models import Board, Post, User
from functional_tests.base_testcase import BaseTestCase
from forum.unit_tests.modelFactory import *

class BoardTest(BaseTestCase):
    def loadData(self):
        BoardFactory.createBoards(1)
        UserFactory.createUsers(1)

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

