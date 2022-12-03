'''
re module provides support for validating email
random module provides support for generating reset_code
smtplib and ssl module provides support for sending emails
'''
import re
import random
import smtplib
import ssl
from helper_functions import generate_handle, generate_token
from data import data
from error import InputError
# Python program to validate an Email

# import re module

# re module provides support
# for regular expressions

# Make a regular expression
# for validating an Email
REGEX = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
# for custom mails use: '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'

# pass the regular expression
# and the string in search() method

def auth_login(email, password):
    '''
    The auth_login function takes in 2 parameters, which are email and password
    and raises an InputError when an invalid email is entered, email entered
    does not belong to a user, or an incorrect password is given. The function
    returns a dictionary containing the u_id and token of the user if the login
    is successful. A valid token will have to be generated for the user to
    remain authenticated.
    '''
    if not re.search(REGEX, email):
        raise InputError('Invalid email address entered')

    if not any(email == user['email'] for _, user in data['users'].items()):
        raise InputError('Email entered does not belong to a user')

    for user in data['users']:
        if data['users'][user]['email'] == email and data['users'][user]['password'] != password:
            raise InputError('Password entered is incorrect')

    token = generate_token(data)

    u_id = 0
    for user in data['users']:
        if data['users'][user]['email'] == email and data['users'][user]['password'] == password:
            data['users'][user]['token'] = str(token)
            u_id = data['users'][user]['u_id']

    return {
        'u_id': u_id,
        'token': str(token),
    }

def auth_logout(token):
    '''
    The auth_logout function takes in 1 parameter, which is token. Given an
    active token, the token will be invalidated to log the user out, meaning
    that the token will no longer be valid and cannot be used for
    authentication. If a valid token is given and the user has been
    successfully logged out, the function returns true. Otherwise, it returns
    false. The function returns a dictionary containing is_success, which is
    either True or False.
    '''
    for user in data['users']:
        if 'token' in data['users'][user]:
            if data['users'][user]['token'] == token:
                del data['users'][user]['token']
                return {
                    'is_success': True,
                }
    return {
        'is_success': False,
    }

def auth_register(email, password, name_first, name_last):
    '''
    The auth_register function takes in 4 parameters, which is email, password,
    name_first and name_last. An InputError will be raised when an invalid email
    is entered, email entered is already being used by another user, password
    entered is less than 6 characters long, name_first is not between 1 and 50
    characters inclusively in length and name_last is not between 1 and 50
    characters inclusively in length. This function will create a new account
    for the user and return a new token for authentication during their session.
    A handle is also generated that is the concatenation of a lowercase only
    first name and last name. If the concatenation is longer than 20 characters.
    it is cutoff at 20 characters. If the handle is already taken, the handle
    will be modified in a way such that it is unique, whilst maintaining the
    20 character limit. This function returns a dictionary containing the u_id
    of the user and the token generated.
    '''
    if len(name_first) > 50 or len(name_first) < 1:
        raise InputError('Invalid first name')

    if len(name_last) > 50 or len(name_last) < 1:
        raise InputError('Invalid last name')

    if len(password) < 6:
        raise InputError('Password cannot be less than 6 characters long')

    if any(email == user['email'] for _, user in data['users'].items()):
        raise InputError('Email address is already being used by another user')

    if not re.search(REGEX, email):
        raise InputError('Invalid email address entered')

    u_id = len(data['users']) + 1
    handle = generate_handle(name_first, name_last, data)

    token = generate_token(data)

    permission_id = 2
    if u_id == 1:
        permission_id = 1

    data['users'][u_id] = {
        'email': email,
        'password' : password,
        'name_first' : name_first,
        'name_last' : name_last,
        'u_id' : u_id,
        'token' : str(token),
        'handle_str' : handle,
        'channel_membership' : [],
        'permission_id': permission_id
    }

    return {
        'u_id': data['users'][u_id]['u_id'],
        'token': data['users'][u_id]['token'],
    }

def auth_passwordreset_request(email):
    '''
    Takes in an email address and checks if the user is registered, the
    user is sent an email contaning a reset code that authenticates
    the user as the individual who is trying to reset their password
    '''
    reset_code = str(random.randrange(10000000, 90000000))
    is_registered = False
    for user in data['users']:
        if data['users'][user]['email'] == email:
            is_registered = True
            data['users'][user]['reset_code'] = reset_code
    if not is_registered:
        raise InputError("User is not registered")

    port = 0
    smtp_server = "smtp.gmail.com"
    sender_email = "deathofthebachelor1@gmail.com"
    receiver_email = email
    email_content = """
    Subject: Resetting your password

    This is your secret code as proof of authentication to reset your password:
        {}

    Warning: Don't share this code with anyone else, or your account might get hacked into!
    """.format(reset_code)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, 'p!atd123')
        server.sendmail(sender_email, receiver_email, email_content)
    return {}

def auth_passwordreset_reset(reset_code, new_password):
    '''
    Given reset_code of user, sets that user's password to new_password. Raises
    InputError when reset_code or new_password is invalid.
    '''
    if len(new_password) < 6:
        raise InputError('Password cannot be less than 6 characters long')

    valid_reset_code = False
    for user in data['users']:
        if 'reset_code' in data['users'][user]:
            if data['users'][user]['reset_code'] == reset_code:
                valid_reset_code = True
                data['users'][user]['password'] = new_password
                del data['users'][user]['reset_code']

    if not valid_reset_code:
        raise InputError('Invalid reset code entered')

    return {}
