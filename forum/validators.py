
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
POST_CONTENT_MAX_LEN= 5000
POST_CONTENT_MIN_LEN= 1

REPLY_CONTENT_MAX_LEN= 500
REPLY_CONTENT_MIN_LEN= 16

# validators

def validate_username(uname):
    l= len(uname)
    if l < USER_NAME_MIN_LEN:
        raise ValidationError('User name must be at least %d characters long' % (USER_NAME_MIN_LEN,))
    if l > USER_NAME_MAX_LEN:
        raise ValidationError('User name can not be longer than %d characters' % (USER_NAME_MAX_LEN,))

def validate_password(password):
    l= len(password)
    if l < USER_PASSWORD_MIN_LEN:
        raise ValidationError('Password must be at least %d characters long' % (USER_PASSWORD_MIN_LEN,))
    if l > USER_PASSWORD_MAX_LEN:
        raise ValidationError('Password can not be longer than %d characters' % (USER_PASSWORD_MAX_LEN,))
