'''
re module provides support for validating email
requests module provides support for obtaining url information
imghdr module provides support for checking image file type
PIL module provides support for obtaining image dimensions
'''
import re
import imghdr
import urllib
import requests
from PIL import Image
from data import data
from error import InputError, AccessError
from helper_functions import u_id_finder

def user_profile(token, u_id):
    '''
    The user_profile function takes in 2 parameters, token and u_id
    and raises an InputError when either a user with u_id is not a
    valid user or the token entered is invalid. For a valid user, a
    dictionary called 'user' is returned which contains a list of
    dictionaries, with information about the user's user_id, email,
    first name, last name and handle
    '''
    valid_token = False
    valid_u_id = False
    user_detail = {}
    for user in data['users']:
        if 'token' in data['users'][user]:
            if data['users'][user]['token'] == token:
                valid_token = True
        if data['users'][user]['u_id'] == u_id:
            valid_u_id = True
            user_detail = {
                'u_id': data['users'][user]['u_id'],
                'email': data['users'][user]['email'],
                'name_first': data['users'][user]['name_first'],
                'name_last': data['users'][user]['name_last'],
                'handle_str': data['users'][user]['handle_str']
            }
            if 'profile_img_url' in data['users'][user]:
                user_detail['profile_img_url'] = data['users'][user]['profile_img_url']
    if not valid_token:
        raise AccessError('Invalid token entered')

    if not valid_u_id:
        raise InputError('Invalid u_id entered')

    return {'user': user_detail}

def user_profile_setname(token, name_first, name_last):
    '''
    The user_profile_setname function takes in 3 parameters, which
    are token, name_first and name_last. An InputError is raised
    when name_first is not between 1 and 50 characters, name_last is
    not between 1 and 50 characters, as well as if an invalid token
    is entered. This function returns an empty dictionary and
    updates the authorised user's first and last name_first
    '''
    if len(name_first) > 50:
        raise InputError('First name cannot be more than 50 characters long')

    if len(name_first) < 1:
        raise InputError('First name cannot be less than 1 character long')

    if len(name_last) > 50:
        raise InputError('Last name cannot be more than 50 characters long')

    if len(name_last) < 1:
        raise InputError('Last name cannot be less than 1 character long')

    u_id = u_id_finder(token, data)
    data['users'][u_id]['name_first'] = name_first
    data['users'][u_id]['name_last'] = name_last
    for channel in data['users'][u_id]['channel_membership']:
        for member in data['channels'][channel['channel_id']]['all_members']:
            if member['u_id'] == u_id:
                member['name_first'] = name_first
                member['name_last'] = name_last
        for owner in data['channels'][channel['channel_id']]['owner_members']:
            if owner['u_id'] == u_id:
                owner['name_first'] = name_first
                owner['name_last'] = name_last
    return {}

def user_profile_setemail(token, email):
    '''
    The user_profile_setemail function takes in 2 parameters, which
    are token and email. An InputError is raised when the email
    entered is not a valid email, email address is already being used
    by another user or an invalid token has been entered. This
    function returns an empty dictionary and updates the authorised
    user's email address
    '''
    # Python program to validate an Email

    # import re module

    # re module provides support
    # for regular expressions

    # Make a regular expression
    # for validating an Email
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    # for custom mails use: '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'

    # pass the regular expression
    # and the string in search() method
    if not re.search(regex, email):
        raise InputError('Invalid email address entered')

    if any(email == user['email'] for _, user in data['users'].items()):
        raise InputError('Email address is already being used by another user')

    valid_token = False
    for user in data['users']:
        if 'token' in data['users'][user]:
            if data['users'][user]['token'] == token:
                valid_token = True
                data['users'][user]['email'] = email

    if not valid_token:
        raise AccessError('Invalid token entered')

    return {
    }

def user_profile_sethandle(token, handle_str):
    '''
    The user_profile_sethandle function takes in 2 parameters, which
    are token and email. An InputError is raised when the handle_str
    is not between 3 and 20 characters, the handle is already used
    by another user or an invalid token has been entered. This
    function returns an empty dictionary and updates the authorised
    user's handle
    '''
    if len(handle_str) > 20:
        raise InputError('Handle cannot be more than 20 characters long')

    if len(handle_str) < 3:
        raise InputError('Handle cannot be less than 3 characters long')

    if any(handle_str == user['handle_str'] for _, user in data['users'].items()):
        raise InputError('Handle is already being used by another user')

    valid_token = False
    for user in data['users']:
        if 'token' in data['users'][user]:
            if data['users'][user]['token'] == token:
                valid_token = True
                data['users'][user]['handle_str'] = handle_str

    if not valid_token:
        raise AccessError('Invalid token entered')

    return {
    }

def user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end, base_url):
    '''
    user_profile_uploadphoto takes a URL of an image on the internet and crops it within bounds
    (takes an extra base_url string variable to obtain base url and store image url)
    '''
    # checking for valid HTTP status for img_url
    try:
        response = requests.head(img_url)
    except requests.ConnectionError:
        raise InputError('Invalid URL provided')
    if response.status_code != 200:
        raise InputError('URL provided does not have a HTTP status of 200')

    # storing img_url image in file
    urllib.request.urlretrieve(img_url, 'static/temp_img_file.jpg')

    # checking image saved is in JPG format
    if imghdr.what('static/temp_img_file.jpg') != 'jpeg':
        raise InputError('Image uploaded is not a JPG')

    # checking cropping dimensions are valid
    img_object = Image.open('static/temp_img_file.jpg')
    width, height = img_object.size
    x_min = 0
    y_min = 0
    x_max = width
    y_max = height
    if x_start < x_min or x_end > x_max or x_start >= x_end:
        raise InputError('Width dimensions (x) are not within the image dimensions at the URL')
    if y_start < y_min or y_end > y_max or y_start >= y_end:
        raise InputError('Height dimensions (y) are not within the image dimensions at the URL')

    # cropping image
    cropped_img = img_object.crop((x_start, y_start, x_end, y_end))

    # checking if token is valid, obtaining user info and storing url
    u_id = u_id_finder(token, data)
    cropped_img.save(f'static/profile_img{u_id}.jpg')
    profile_img_url = f'{base_url}/imgurl/profile_img{u_id}.jpg'
    data['users'][u_id]['profile_img_url'] = profile_img_url
    for channel in data['users'][u_id]['channel_membership']:
        for member in data['channels'][channel['channel_id']]['all_members']:
            if member['u_id'] == u_id:
                member['profile_img_url'] = profile_img_url
        for owner in data['channels'][channel['channel_id']]['owner_members']:
            if owner['u_id'] == u_id:
                owner['profile_img_url'] = profile_img_url
    return {}
