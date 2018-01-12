from django.test import TestCase

from forum.forms import UserRegistrationForm

class UserFormtest(TestCase):
    def getValidData(self):
        valid_data = {
            'username': 'user',
            'password': 'passowrd',
            'email': 'example@aiuu.com',
            'confirm_password': 'passowrd',
        }

        return valid_data


    def test_validData(self):
        #valid data
        data = self.getValidData()

        form = UserRegistrationForm(data= data)
        self.assertTrue(form.is_valid())

    def test_short_uname(self):
        data = self.getValidData()
        data['username']= 'aa'  #inentionaly invalid data

        form = UserRegistrationForm(data=data)
        self.assertFalse(form.is_valid())

    # todo bug empty form gets accepted
    # todo create more invalid data tests