from forumsite.settings import *
import logging

#WARNING: This setting should be used only when testing

# overwrite settings for better suiting to testing

DEBUG= False

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

logging.disable(logging.CRITICAL)