'''
requests is imported to obtain data from flask server
urllib module provides support in obtaining images from URL
PIL module provides support for cropping and comparing images
'''
import urllib
import requests
import pytest
from PIL import Image, ImageChops

@pytest.mark.usefixtures("url")
def test_url(url):
    '''
    A simple sanity test to check that your server is set up properly
    '''
    assert url.startswith("http")

# Tests for user_profile:
def test_user_profile_http_invalid_u_id(url):
    '''
    raises InputError if user with u_id is not a valid user
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    invalid_u_id = register_payload['u_id'] + 100

    input_url = f"{url}/user/profile?token={register_payload['token']}&u_id={invalid_u_id}"
    response = requests.get(input_url)
    user_details_payload = response.json()
    assert user_details_payload['code'] == 400
    assert user_details_payload['message'] == '<p>Invalid u_id entered</p>'

def test_user_profile_http_invalid_token(url):
    '''
    raises InputError if given token is invalid
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    invalid_token = register_payload['token'] + 'abc'

    input_url = f"{url}/user/profile?token={invalid_token}&u_id={register_payload['u_id']}"
    response = requests.get(input_url)
    user_details_payload = response.json()
    assert user_details_payload['code'] == 400
    assert user_details_payload['message'] == '<p>Invalid token entered</p>'

def test_user_profile_http_valid_inputs(url):
    '''
    test to check that user with valid u_id and token returns
    correct information
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    in_url = f"{url}/user/profile?token={register_payload['token']}&u_id={register_payload['u_id']}"
    response = requests.get(in_url)
    user_details_payload = response.json()
    assert user_details_payload['user'] == {'u_id': register_payload['u_id'],
                                            'email': 'ankitrai326@gmail.com',
                                            'name_first': 'tom',
                                            'name_last': 'hardy',
                                            'handle_str': 'tomhardy'
                                           }

# Tests for user_profile_setname:
def test_user_profile_setname_http_valid_name_first(url):
    '''
    tests to check that name_first is valid (between 1-50 characters)
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    response = requests.put(f'{url}/user/profile/setname', json={
        'token': register_payload['token'],
        'name_first': 'A',
        'name_last': 'hardy'
    })
    user_details_payload = response.json()
    assert user_details_payload == {}

    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    response = requests.put(f'{url}/user/profile/setname', json={
        'token': register_payload['token'],
        'name_first': 'A' * 50,
        'name_last': 'hardy'
    })
    user_details_payload = response.json()
    assert user_details_payload == {}

def test_user_profile_setname_http_invalid_name_first(url):
    '''
    raises InputError if name_first is invalid (not between 1-50
    characters)
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    response = requests.put(f'{url}/user/profile/setname', json={
        'token': register_payload['token'],
        'name_first': '',
        'name_last': 'hardy'
    })
    user_details_payload = response.json()
    error_message = '<p>First name cannot be less than 1 character long</p>'
    assert user_details_payload['code'] == 400
    assert user_details_payload['message'] == error_message

    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    response = requests.put(f'{url}/user/profile/setname', json={
        'token': register_payload['token'],
        'name_first': 'A' * 51,
        'name_last': 'hardy'
    })
    user_details_payload = response.json()
    error_message = '<p>First name cannot be more than 50 characters long</p>'
    assert user_details_payload['code'] == 400
    assert user_details_payload['message'] == error_message

def test_user_profile_setname_http_valid_name_last(url):
    '''
    tests to check that name_last is valid (between 1-50 characters)
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    response = requests.put(f'{url}/user/profile/setname', json={
        'token': register_payload['token'],
        'name_first': 'tom',
        'name_last': 'A'
    })
    user_details_payload = response.json()
    assert user_details_payload == {}

    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    response = requests.put(f'{url}/user/profile/setname', json={
        'token': register_payload['token'],
        'name_first': 'tom',
        'name_last': 'A' * 50
    })
    user_details_payload = response.json()
    assert user_details_payload == {}

def test_user_profile_setname_http_invalid_name_last(url):
    '''
    raises InputError if name_last is invalid (not between 1-50
    characters)
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    response = requests.put(f'{url}/user/profile/setname', json={
        'token': register_payload['token'],
        'name_first': 'tom',
        'name_last': ''
    })
    user_details_payload = response.json()
    error_message = '<p>Last name cannot be less than 1 character long</p>'
    assert user_details_payload['code'] == 400
    assert user_details_payload['message'] == error_message

    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    response = requests.put(f'{url}/user/profile/setname', json={
        'token': register_payload['token'],
        'name_first': 'tom',
        'name_last': 'A' * 51
    })
    user_details_payload = response.json()
    error_message = '<p>Last name cannot be more than 50 characters long</p>'
    assert user_details_payload['code'] == 400
    assert user_details_payload['message'] == error_message

def test_user_profile_setname_http_valid_token(url):
    '''
    test to check that given token is valid
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    response = requests.put(f'{url}/user/profile/setname', json={
        'token': register_payload['token'],
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user_details_payload = response.json()
    assert user_details_payload == {}

def test_user_profile_setname_http_invalid_token(url):
    '''
    raises InputError if given token is invalid
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    invalid_token = register_payload['token'] + 'abc'
    response = requests.put(f'{url}/user/profile/setname', json={
        'token': invalid_token,
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user_details_payload = response.json()
    assert user_details_payload['code'] == 400
    assert user_details_payload['message'] == '<p>Invalid token entered</p>'

def test_user_profile_setname_http_updated_name(url):
    '''
    checks if user's name_first and name_last has been updated
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    response = requests.put(f'{url}/user/profile/setname', json={
        'token': register_payload['token'],
        'name_first': 'dark',
        'name_last': 'knight'
    })
    user_details_payload = response.json()
    assert user_details_payload == {}
    in_url = f"{url}/user/profile?token={register_payload['token']}&u_id={register_payload['u_id']}"
    response = requests.get(in_url)
    user_profile_payload = response.json()
    assert user_profile_payload['user'] == {'u_id': register_payload['u_id'],
                                            'email': 'ankitrai326@gmail.com',
                                            'name_first': 'dark',
                                            'name_last': 'knight',
                                            'handle_str': 'tomhardy'
                                           }

# Tests for user_profile_setemail:
def test_user_profile_setemail_valid_email(url):
    '''
    test to check that given email is valid
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    response = requests.put(f'{url}/user/profile/setemail', json={
        'token': register_payload['token'],
        'email': 'ankitrai001@gmail.com'
    })
    user_details_payload = response.json()
    assert user_details_payload == {}

    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    response = requests.put(f'{url}/user/profile/setemail', json={
        'token': register_payload['token'],
        'email': 'my.ownsite@ourearth.org'
    })
    user_details_payload = response.json()
    assert user_details_payload == {}

def test_user_profile_setemail_http_invalid_email(url):
    '''
    raises InputError if given email is invalid
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    response = requests.put(f'{url}/user/profile/setemail', json={
        'token': register_payload['token'],
        'email': 'ankitrai326.com'
    })
    user_details_payload = response.json()
    assert user_details_payload['code'] == 400
    assert user_details_payload['message'] == '<p>Invalid email address entered</p>'

def test_user_profile_setemail_http_email_in_use(url):
    '''
    raises InputError if given email is already in use by another
    user
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    response = requests.put(f'{url}/user/profile/setemail', json={
        'token': register_payload['token'],
        'email': 'ankitrai326@gmail.com'
    })
    user_details_payload = response.json()
    error_message = '<p>Email address is already being used by another user</p>'
    assert user_details_payload['code'] == 400
    assert user_details_payload['message'] == error_message

    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()

    requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai001@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    response = requests.put(f'{url}/user/profile/setemail', json={
        'token': register_payload['token'],
        'email': 'ankitrai001@gmail.com'
    })
    user_details_payload = response.json()
    error_message = '<p>Email address is already being used by another user</p>'
    assert user_details_payload['code'] == 400
    assert user_details_payload['message'] == error_message

def test_user_profile_setemail_http_valid_token(url):
    '''
    test to check that given token is valid
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    response = requests.put(f'{url}/user/profile/setemail', json={
        'token': register_payload['token'],
        'email': 'ankitrai001@gmail.com'
    })
    user_details_payload = response.json()
    assert user_details_payload == {}

def test_user_profile_setemail_http_invalid_token(url):
    '''
    raises InputError if given token is invalid
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    invalid_token = register_payload['token'] + 'abc'
    response = requests.put(f'{url}/user/profile/setemail', json={
        'token': invalid_token,
        'email': 'ankitrai001@gmail.com'
    })
    user_details_payload = response.json()
    assert user_details_payload['code'] == 400
    assert user_details_payload['message'] == '<p>Invalid token entered</p>'

def test_user_profile_setemail_http_updated_email(url):
    '''
    checks if user's email has been updated
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    response = requests.put(f'{url}/user/profile/setemail', json={
        'token': register_payload['token'],
        'email': 'ankitrai001@gmail.com'
    })
    user_details_payload = response.json()
    assert user_details_payload == {}
    in_url = f"{url}/user/profile?token={register_payload['token']}&u_id={register_payload['u_id']}"
    response = requests.get(in_url)
    user_profile_payload = response.json()
    assert user_profile_payload['user'] == {'u_id': register_payload['u_id'],
                                            'email': 'ankitrai001@gmail.com',
                                            'name_first': 'tom',
                                            'name_last': 'hardy',
                                            'handle_str': 'tomhardy'
                                           }

# Tests for user_profile_sethandle:
def test_user_profile_sethandle_http_valid_handle(url):
    '''
    test to check that handle_str is valid (between 3-20 characters)
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    response = requests.put(f'{url}/user/profile/sethandle', json={
        'token': register_payload['token'],
        'handle_str': 'A' * 3
    })
    user_details_payload = response.json()
    assert user_details_payload == {}

    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    response = requests.put(f'{url}/user/profile/sethandle', json={
        'token': register_payload['token'],
        'handle_str': 'A' * 20
    })
    user_details_payload = response.json()
    assert user_details_payload == {}

def test_user_profile_sethandle_http_invalid_handle(url):
    '''
    raises InputError if handle_str is invalid (not between 3-20 characters)
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    response = requests.put(f'{url}/user/profile/sethandle', json={
        'token': register_payload['token'],
        'handle_str': 'A' * 2
    })
    user_details_payload = response.json()
    error_message = '<p>Handle cannot be less than 3 characters long</p>'
    assert user_details_payload['code'] == 400
    assert user_details_payload['message'] == error_message

    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    response = requests.put(f'{url}/user/profile/sethandle', json={
        'token': register_payload['token'],
        'handle_str': 'A' * 21
    })
    user_details_payload = response.json()
    error_message = '<p>Handle cannot be more than 20 characters long</p>'
    assert user_details_payload['code'] == 400
    assert user_details_payload['message'] == error_message

def test_user_profile_sethandle_http_handle_in_use(url):
    '''
    raises InputError if handle_str entered is already in use
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    response = requests.put(f'{url}/user/profile/sethandle', json={
        'token': register_payload['token'],
        'handle_str': 'tomhardy'
    })
    user_details_payload = response.json()
    error_message = '<p>Handle is already being used by another user</p>'
    assert user_details_payload['code'] == 400
    assert user_details_payload['message'] == error_message

    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()

    requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai001@gmail.com',
        'password': '12345678',
        'name_first': 'christian',
        'name_last': 'bale'
    })

    response = requests.put(f'{url}/user/profile/sethandle', json={
        'token': register_payload['token'],
        'handle_str': 'christianbale'
    })
    user_details_payload = response.json()
    error_message = '<p>Handle is already being used by another user</p>'
    assert user_details_payload['code'] == 400
    assert user_details_payload['message'] == error_message

def test_user_profile_sethandle_http_valid_token(url):
    '''
    test to check that given token is valid
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    response = requests.put(f'{url}/user/profile/sethandle', json={
        'token': register_payload['token'],
        'handle_str': 'christianbale'
    })
    user_details_payload = response.json()
    assert user_details_payload == {}

def test_user_profile_sethandle_http_invalid_token(url):
    '''
    raises InputError if given token is invalid
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    invalid_token = register_payload['token'] + 'abc'
    response = requests.put(f'{url}/user/profile/sethandle', json={
        'token': invalid_token,
        'handle_str': 'christianbale'
    })
    user_details_payload = response.json()
    assert user_details_payload['code'] == 400
    assert user_details_payload['message'] == '<p>Invalid token entered</p>'

def test_user_profile_sethandle_http_updated_handle(url):
    '''
    checks if user's handle has been updated
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    response = requests.put(f'{url}/user/profile/sethandle', json={
        'token': register_payload['token'],
        'handle_str': 'ChristianBale'
    })
    user_details_payload = response.json()
    assert user_details_payload == {}
    in_url = f"{url}/user/profile?token={register_payload['token']}&u_id={register_payload['u_id']}"
    response = requests.get(in_url)
    user_profile_payload = response.json()
    assert user_profile_payload['user'] == {'u_id': register_payload['u_id'],
                                            'email': 'ankitrai326@gmail.com',
                                            'name_first': 'tom',
                                            'name_last': 'hardy',
                                            'handle_str': 'ChristianBale'
                                           }

# Tests for user_profile_uploadphoto:
def test_user_profile_uploadphoto_http_invalid_http_status(url):
    '''
    checks if InputError is raised when invalid http status (not 200) is entered
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    response = requests.post(f'{url}/user/profile/uploadphoto', json={
        'token': register_payload['token'],
        'img_url': 'https://www.aiwdhaohdahdwo.awdjoadj',
        'x_start': 200,
        'y_start': 200,
        'x_end': 400,
        'y_end': 400
    })
    payload = response.json()

    assert payload['code'] == 400
    assert payload['message'] == '<p>Invalid URL provided</p>'

def test_user_profile_uploadphoto_http_invalid_x_dimensions(url):
    '''
    checks if InputError is raised when invalid x dimensions are entered
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    response = requests.post(f'{url}/user/profile/uploadphoto', json={
        'token': register_payload['token'],
        'img_url': 'https://pbs.twimg.com/profile_images/976522723445936128/RDTP0iCK_400x400.jpg',
        'x_start': -1,
        'y_start': 200,
        'x_end': 400,
        'y_end': 400
    })
    payload = response.json()

    assert payload['code'] == 400
    error_message = '<p>Width dimensions (x) are not within the image dimensions at the URL</p>'
    assert payload['message'] == error_message

    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    response = requests.post(f'{url}/user/profile/uploadphoto', json={
        'token': register_payload['token'],
        'img_url': 'https://pbs.twimg.com/profile_images/976522723445936128/RDTP0iCK_400x400.jpg',
        'x_start': 0,
        'y_start': 200,
        'x_end': 401,
        'y_end': 400
    })
    payload = response.json()

    assert payload['code'] == 400
    error_message = '<p>Width dimensions (x) are not within the image dimensions at the URL</p>'
    assert payload['message'] == error_message

def test_user_profile_uploadphoto_http_invalid_y_dimensions(url):
    '''
    checks if InputError is raised when invalid y dimensions are entered
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    response = requests.post(f'{url}/user/profile/uploadphoto', json={
        'token': register_payload['token'],
        'img_url': 'https://pbs.twimg.com/profile_images/976522723445936128/RDTP0iCK_400x400.jpg',
        'x_start': 200,
        'y_start': -1,
        'x_end': 400,
        'y_end': 400
    })
    payload = response.json()

    assert payload['code'] == 400
    error_message = '<p>Height dimensions (y) are not within the image dimensions at the URL</p>'
    assert payload['message'] == error_message

    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    response = requests.post(f'{url}/user/profile/uploadphoto', json={
        'token': register_payload['token'],
        'img_url': 'https://pbs.twimg.com/profile_images/976522723445936128/RDTP0iCK_400x400.jpg',
        'x_start': 200,
        'y_start': 200,
        'x_end': 400,
        'y_end': 401
    })
    payload = response.json()

    assert payload['code'] == 400
    error_message = '<p>Height dimensions (y) are not within the image dimensions at the URL</p>'
    assert payload['message'] == error_message

def test_user_profile_uploadphoto_http_invalid_token(url):
    '''
    checks if InputError is raised when invalid token is entered
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    invalid_token = register_payload['token'] + 'abc'
    response = requests.post(f'{url}/user/profile/uploadphoto', json={
        'token': invalid_token,
        'img_url': 'https://pbs.twimg.com/profile_images/976522723445936128/RDTP0iCK_400x400.jpg',
        'x_start': 200,
        'y_start': 200,
        'x_end': 400,
        'y_end': 400
    })
    payload = response.json()

    assert payload['code'] == 400
    assert payload['message'] == '<p>Invalid token entered</p>'

def test_user_profile_uploadphoto_http_img_not_jpg(url):
    '''
    checks if InputError is raised when image uploaded is not a JPG (e.g. gif)
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    response = requests.post(f'{url}/user/profile/uploadphoto', json={
        'token': register_payload['token'],
        'img_url': 'https://compote.slate.com/images/697b023b-64a5-49a0-8059-27b963453fb1.gif',
        'x_start': 200,
        'y_start': 200,
        'x_end': 400,
        'y_end': 400
    })
    payload = response.json()

    assert payload['code'] == 400
    assert payload['message'] == '<p>Image uploaded is not a JPG</p>'

def test_user_profile_uploadphoto_http_uncropped_valid_img(url):
    '''
    checks if picture is loaded when full dimensions are entered (no cropping tested)
    '''
    requests.delete(f'{url}/clear')
    img_url = 'https://pbs.twimg.com/profile_images/976522723445936128/RDTP0iCK_400x400.jpg'
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    reg_payload = response.json()
    response = requests.post(f'{url}/user/profile/uploadphoto', json={
        'token': reg_payload['token'],
        'img_url': img_url,
        'x_start': 0,
        'y_start': 0,
        'x_end': 400,
        'y_end': 400
    })
    return_val = response.json()
    assert return_val == {}
    input_url = f"{url}/user/profile?token={reg_payload['token']}&u_id={reg_payload['u_id']}"
    response = requests.get(input_url)
    user_details_payload = response.json()
    output_url = user_details_payload['user']['profile_img_url']
    urllib.request.urlretrieve(img_url, 'static/input_img.jpg')
    urllib.request.urlretrieve(output_url, 'static/output_img.jpg')
    in_img = Image.open('static/input_img.jpg')
    out_img = Image.open('static/output_img.jpg')
    assert ImageChops.difference(in_img, out_img).getbbox() == (0, 0, 400, 400)

def test_user_profile_uploadphoto_http_cropped_valid_img(url):
    '''
    checks if picture is loaded when dimensions are entered (cropping tested)
    '''
    requests.delete(f'{url}/clear')
    img_url = 'https://pbs.twimg.com/profile_images/976522723445936128/RDTP0iCK_400x400.jpg'
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    reg_payload = response.json()
    response = requests.post(f'{url}/user/profile/uploadphoto', json={
        'token': reg_payload['token'],
        'img_url': img_url,
        'x_start': 200,
        'y_start': 100,
        'x_end': 300,
        'y_end': 350
    })
    return_val = response.json()
    assert return_val == {}
    input_url = f"{url}/user/profile?token={reg_payload['token']}&u_id={reg_payload['u_id']}"
    response = requests.get(input_url)
    user_details_payload = response.json()
    output_url = user_details_payload['user']['profile_img_url']
    urllib.request.urlretrieve(img_url, 'static/input_img.jpg')
    urllib.request.urlretrieve(output_url, 'static/output_img.jpg')
    in_img = Image.open('static/input_img.jpg')
    cropped_img = in_img.crop((200, 100, 300, 350))
    out_img = Image.open('static/output_img.jpg')
    assert ImageChops.difference(out_img, cropped_img).getbbox() == (0, 0, 100, 250)
