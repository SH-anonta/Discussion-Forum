import re

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# constants
USER_NAME_MIN_LEN= 4
USER_NAME_MAX_LEN= 20

USER_PASSWORD_MIN_LEN= 8
USER_PASSWORD_MAX_LEN= 512

BOARD_TITLE_MAX_LEN= 1
BOARD_TITLE_MIN_LEN= 30

POST_TITLE_MAX_LEN= 50
POST_TITLE_MIN_LEN= 1
POST_CONTENT_MAX_LEN= 10000
POST_CONTENT_MIN_LEN= 1

REPLY_CONTENT_MAX_LEN= 1000
REPLY_CONTENT_MIN_LEN= 16

EMAIL_ADDRESS_NAME_MIN_LEN= 4
EMAIL_ADDRESS_NAME_MAX_LEN= 50

valid_username_pattern = re.compile(r'^\w{4,20}$')
# validators

def validate_username(uname):
    msg = 'Invalid UserName!\nUser name must be 4-10 characters long and only contain alpha numeric characters'
    global valid_username_pattern

    if not valid_username_pattern.search(uname):
        raise ValidationError(msg)

    # check for existing username uniqueness
    if User.objects.filter(username= uname).exists():
        raise ValidationError('User name is not available')

def validate_password(password):
    l= len(password)
    if l < USER_PASSWORD_MIN_LEN:
        raise ValidationError('Password must be at least %d characters long' % (USER_PASSWORD_MIN_LEN,))
    if l > USER_PASSWORD_MAX_LEN:
        raise ValidationError('Password can not be longer than %d characters' % (USER_PASSWORD_MAX_LEN,))

def validate_email(email):
    if User.objects.filter(email=email).exists():
        raise ValidationError('This email is being used in an existing account')