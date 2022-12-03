'''pytest is imported to check for errors and to run the tests'''
import pytest
from auth import auth_register
from user import user_profile, user_profile_setname, user_profile_setemail, user_profile_sethandle
from user import user_profile_uploadphoto
from error import InputError, AccessError
from other import clear

# Tests for user_profile:
def test_user_profile_invalid_u_id():
    '''
    raises InputError if user with u_id is not a valid user
    '''
    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    invalid_u_id = user_dict['u_id'] + 100
    with pytest.raises(InputError):
        assert user_profile(user_dict['token'], invalid_u_id)

def test_user_profile_invalid_token():
    '''
    raises AccessError if given token is invalid
    '''
    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    invalid_token = user_dict['token'] + "abc"
    with pytest.raises(AccessError):
        assert user_profile(invalid_token, user_dict['u_id'])

def test_user_profile_valid_inputs():
    '''
    test to check that user with valid u_id and token returns
    correct information
    '''
    clear()
    user_dict1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    user_dict2 = auth_register("ankitrai001@gmail.com", "12345678", "tom", "hardy")
    profile = user_profile(user_dict2['token'], user_dict1['u_id'])
    assert profile['user'] == {'u_id': user_dict1['u_id'],
                               'email': 'ankitrai326@gmail.com',
                               'name_first': 'tom',
                               'name_last': 'hardy',
                               'handle_str': 'tomhardy'
                              }

# Tests for user_profile_setname:
def test_user_profile_setname_valid_name_first():
    '''
    tests to check that name_first is valid (between 1-50 characters)
    '''
    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    assert user_profile_setname(user_dict['token'], "A", "hardy") == {}

    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    assert user_profile_setname(user_dict['token'], "A" * 50, "hardy") == {}

def test_user_profile_setname_invalid_name_first():
    '''
    raises InputError if name_first is invalid (not between 1-50
    characters)
    '''
    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    with pytest.raises(InputError):
        assert user_profile_setname(user_dict['token'], "", "hardy")

    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    with pytest.raises(InputError):
        assert user_profile_setname(user_dict['token'], "A" * 51, "hardy")

def test_user_profile_setname_valid_name_last():
    '''
    tests to check that name_last is valid (between 1-50 characters)
    '''
    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    assert user_profile_setname(user_dict['token'], "tom", "A") == {}

    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    assert user_profile_setname(user_dict['token'], "tom", "A" * 50) == {}

def test_user_profile_setname_invalid_name_last():
    '''
    raises InputError if name_last is invalid (not between 1-50
    characters)
    '''
    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    with pytest.raises(InputError):
        assert user_profile_setname(user_dict['token'], "tom", "")

    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    with pytest.raises(InputError):
        assert user_profile_setname(user_dict['token'], "tom", "A" * 51)

def test_user_profile_setname_valid_token():
    '''
    test to check that given token is valid
    '''
    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    assert user_profile_setname(user_dict['token'], "tom", "hardy") == {}

def test_user_profile_setname_invalid_token():
    '''
    raises AccessError if given token is invalid
    '''
    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    invalid_token = user_dict['token'] + "abc"
    with pytest.raises(AccessError):
        assert user_profile_setname(invalid_token, "tom", "hardy")

def test_user_profile_setname_updated_name():
    '''
    checks if user's name_first and name_last has been updated
    '''
    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    assert user_profile_setname(user_dict['token'], "dark", "knight") == {}
    profile = user_profile(user_dict['token'], user_dict['u_id'])
    assert profile['user'] == {'u_id': user_dict['u_id'],
                               'email': 'ankitrai326@gmail.com',
                               'name_first': 'dark',
                               'name_last': 'knight',
                               'handle_str': 'tomhardy'
                              }

# Tests for user_profile_setemail:
def test_user_profile_setemail_valid_email():
    '''
    test to check that given email is valid
    '''
    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    assert user_profile_setemail(user_dict['token'], "ankitrai001@gmail.com") == {}

    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    assert user_profile_setemail(user_dict['token'], "my.ownsite@ourearth.org") == {}

def test_user_profile_setemail_invalid_email():
    '''
    raises InputError if given email is invalid
    '''
    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    with pytest.raises(InputError):
        assert user_profile_setemail(user_dict['token'], "ankitrai326.com")

def test_user_profile_setemail_email_in_use():
    '''
    raises InputError if given email is already in use by another
    user
    '''
    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    with pytest.raises(InputError):
        assert user_profile_setemail(user_dict['token'], "ankitrai326@gmail.com")

    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    auth_register("ankitrai001@gmail.com", "12345678", "tom", "hardy")
    with pytest.raises(InputError):
        assert user_profile_setemail(user_dict['token'], "ankitrai001@gmail.com")

def test_user_profile_setemail_valid_token():
    '''
    test to check that given token is valid
    '''
    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    assert user_profile_setemail(user_dict['token'], "ankitrai001@gmail.com") == {}

def test_user_profile_setemail_invalid_token():
    '''
    raises AccessError if given token is invalid
    '''
    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    invalid_token = user_dict['token'] + "abc"
    with pytest.raises(AccessError):
        assert user_profile_setemail(invalid_token, "ankitrai001@gmail.com")

def test_user_profile_setemail_updated_email():
    '''
    checks if user's email has been updated
    '''
    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    assert user_profile_setemail(user_dict['token'], "ankitrai001@gmail.com") == {}
    profile = user_profile(user_dict['token'], user_dict['u_id'])
    assert profile['user'] == {'u_id': user_dict['u_id'],
                               'email': 'ankitrai001@gmail.com',
                               'name_first': 'tom',
                               'name_last': 'hardy',
                               'handle_str': 'tomhardy'
                              }

# Tests for user_profile_sethandle:
def test_user_profile_sethandle_valid_handle():
    '''
    test to check that handle_str is valid (between 3-20 characters)
    '''
    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    assert user_profile_sethandle(user_dict['token'], "A" * 3) == {}

    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    assert user_profile_sethandle(user_dict['token'], "A" * 20) == {}

def test_user_profile_sethandle_invalid_handle():
    '''
    raises InputError if handle_str is invalid (not between 3-20
    characters)
    '''
    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    with pytest.raises(InputError):
        assert user_profile_sethandle(user_dict['token'], "A" * 2)

    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    with pytest.raises(InputError):
        assert user_profile_sethandle(user_dict['token'], "A" * 21)

def test_user_profile_sethandle_handle_in_use():
    '''
    raises InputError if handle_str entered is already in use
    '''
    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    with pytest.raises(InputError):
        assert user_profile_sethandle(user_dict['token'], "tomhardy")

    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    auth_register("ankitrai001@gmail.com", "12345678", "christian", "bale")
    with pytest.raises(InputError):
        assert user_profile_sethandle(user_dict['token'], "christianbale")

def test_user_profile_sethandle_valid_token():
    '''
    test to check that given token is valid
    '''
    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    assert user_profile_sethandle(user_dict['token'], "christianbale") == {}

def test_user_profile_sethandle_invalid_token():
    '''
    raises AccessError if given token is invalid
    '''
    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    invalid_token = user_dict['token'] + "abc"
    with pytest.raises(AccessError):
        assert user_profile_sethandle(invalid_token, "christianbale")

def test_user_profile_sethandle_updated_handle():
    '''
    checks if user's handle has been updated
    '''
    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    assert user_profile_sethandle(user_dict['token'], "ChristianBale") == {}
    profile = user_profile(user_dict['token'], user_dict['u_id'])
    assert profile['user'] == {'u_id': user_dict['u_id'],
                               'email': 'ankitrai326@gmail.com',
                               'name_first': 'tom',
                               'name_last': 'hardy',
                               'handle_str': 'ChristianBale'
                              }

# Tests for user_profile_uploadphoto:
def test_user_profile_uploadphoto_invalid_http_status():
    '''
    checks if InputError is raised when invalid http status (not 200) is entered
    '''
    clear()
    user_info = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    input_url = "https://www.aiwdhaohdahdwo.awdjoadj"
    with pytest.raises(InputError):
        assert user_profile_uploadphoto(user_info['token'], input_url, 280, 200, 450, 400, 'url')

def test_user_profile_uploadphoto_invalid_x_dimensions():
    '''
    checks if InputError is raised when invalid x dimensions are entered
    '''
    clear()
    user_info = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    input_url = "https://pbs.twimg.com/profile_images/976522723445936128/RDTP0iCK_400x400.jpg"
    with pytest.raises(InputError):
        assert user_profile_uploadphoto(user_info['token'], input_url, -1, 200, 400, 400, 'url')

    clear()
    user_info = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    input_url = "https://pbs.twimg.com/profile_images/976522723445936128/RDTP0iCK_400x400.jpg"
    with pytest.raises(InputError):
        assert user_profile_uploadphoto(user_info['token'], input_url, 0, 200, 401, 400, 'url')

def test_user_profile_uploadphoto_invalid_y_dimensions():
    '''
    checks if InputError is raised when invalid y dimensions are entered
    '''
    clear()
    user_info = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    input_url = "https://pbs.twimg.com/profile_images/976522723445936128/RDTP0iCK_400x400.jpg"
    with pytest.raises(InputError):
        assert user_profile_uploadphoto(user_info['token'], input_url, 0, -1, 400, 400, 'url')

    clear()
    user_info = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    input_url = "https://pbs.twimg.com/profile_images/976522723445936128/RDTP0iCK_400x400.jpg"
    with pytest.raises(InputError):
        assert user_profile_uploadphoto(user_info['token'], input_url, 0, 0, 400, 401, 'url')

def test_user_profile_uploadphoto_invalid_token():
    '''
    checks if AccessError is raised when invalid token is entered
    '''
    clear()
    user_info = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    input_url = "https://pbs.twimg.com/profile_images/976522723445936128/RDTP0iCK_400x400.jpg"
    invalid_token = user_info['token'] + 'abc'
    with pytest.raises(AccessError):
        assert user_profile_uploadphoto(invalid_token, input_url, 0, 0, 400, 400, 'url')

def test_user_profile_uploadphoto_img_not_jpg():
    '''
    checks if InputError is raised when image uploaded is not a JPG (e.g. gif)
    '''
    clear()
    user_info = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    input_url = "https://compote.slate.com/images/697b023b-64a5-49a0-8059-27b963453fb1.gif"
    with pytest.raises(InputError):
        assert user_profile_uploadphoto(user_info['token'], input_url, 0, 0, 400, 400, 'url')
