from forum.models import Board
from functional_tests.base_testcase import BaseTestCase


class BoardTest(BaseTestCase):
    def loadData(self):
        b1= Board.objects.create(title='Announcements')
        b2= Board.objects.create(title='General discussion')
        b3= Board.objects.create(title='Programming')

    def test_board(self):
        browser= self.getBrowser()

        browser.get(self.getHomePageAddress())