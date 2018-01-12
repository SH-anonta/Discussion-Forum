
from django.core.exceptions import ValidationError


MIN_USER_NAME_LEN= 4
MAX_USER_NAME_LEN= 20

MIN_PASSWORD_LEN= 8
MAX_PASSWORD_LEN= 512

def validate_username(uname):
    l= len(uname)
    if l < MIN_USER_NAME_LEN:
        raise ValidationError('User name must be at least %d characters long' % (MIN_USER_NAME_LEN,))
    if l > MAX_USER_NAME_LEN:
        raise ValidationError('User name can not be longer than %d characters' % (MAX_USER_NAME_LEN,))

def validate_password(password):
    l= len(password)
    if l < MIN_PASSWORD_LEN:
        raise ValidationError('Password must be at least %d characters long' %(MIN_PASSWORD_LEN,))
    if l > MAX_PASSWORD_LEN:
        raise ValidationError('Password can not be longer than %d characters' %(MAX_PASSWORD_LEN,))

