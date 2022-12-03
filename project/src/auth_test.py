'''pytest is imported to check for errors and to run the tests'''
import pytest
from auth import auth_register, auth_login, auth_logout
from auth import auth_passwordreset_request, auth_passwordreset_reset
from error import InputError
from other import clear
from user import user_profile

# Tests for auth_register:
def test_auth_register_valid_email():
    '''
    test to check registered email is valid and return value is same as
    registered email
    '''
    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    profile = user_profile(user_dict['token'], user_dict['u_id'])
    assert profile['user']['email'] == "ankitrai326@gmail.com"

    clear()
    user_dict = auth_register("my.ownsite@ourearth.org", "12345678", "tom", "hardy")
    profile = user_profile(user_dict['token'], user_dict['u_id'])
    assert profile['user']['email'] == "my.ownsite@ourearth.org"

def test_auth_register_invalid_email():
    '''
    raises InputError if email entered is invalid
    '''
    clear()
    with pytest.raises(InputError):
        assert auth_register("ankitrai326.com", "12345678", "tom", "hardy")

def test_auth_register_email_in_use():
    '''
    raises InputError if same email is registered the second time (in use)
    '''
    clear()
    assert auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    with pytest.raises(InputError):
        assert auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")

def test_auth_register_valid_password():
    '''
    checks if the email of the user is the registered email, this indicates
    that the user has entered a valid password and the user has been registered
    '''
    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "123456", "tom", "hardy")
    profile = user_profile(user_dict['token'], user_dict['u_id'])
    assert profile['user']['email'] == "ankitrai326@gmail.com"

    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "1234567812joeeee", "tom", "hardy")
    profile = user_profile(user_dict['token'], user_dict['u_id'])
    assert profile['user']['email'] == "ankitrai326@gmail.com"

def test_auth_register_invalid_password():
    '''
    raises InputError if user registers with invalid password
    '''
    clear()
    with pytest.raises(InputError):
        assert auth_register("ankitrai326@gmail.com", "12345", "tom", "hardy")
    clear()
    with pytest.raises(InputError):
        assert auth_register("ankitrai326@gmail.com", "a", "tom", "hardy")

def test_auth_register_valid_name_first():
    '''
    test to check valid name_first has been entered
    '''
    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "A" * 50, "hardy")
    profile = user_profile(user_dict['token'], user_dict['u_id'])
    assert profile['user']['name_first'] == "A" * 50

    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "A", "hardy")
    profile = user_profile(user_dict['token'], user_dict['u_id'])
    assert profile['user']['name_first'] == "A"

def test_auth_register_invalid_name_first():
    '''
    raises InputError if user registers with invalid name_first
    '''
    clear()
    with pytest.raises(InputError):
        assert auth_register("ankitrai326@gmail.com", "12345678", "", "hardy")
    clear()
    with pytest.raises(InputError):
        assert auth_register("ankitrai326@gmail.com", "12345678", "A"*51, "hardy")

def test_auth_register_valid_name_last():
    '''
    test to check valid name_last
    '''
    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "A" * 50)
    profile = user_profile(user_dict['token'], user_dict['u_id'])
    assert profile['user']['name_last'] == "A" * 50

    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "A")
    profile = user_profile(user_dict['token'], user_dict['u_id'])
    assert profile['user']['name_last'] == "A"

def test_auth_register_invalid_name_last():
    '''
    raises InputError if user registers with invalid name_last
    '''
    clear()
    with pytest.raises(InputError):
        assert auth_register("ankitrai326@gmail.com", "12345678", "tom", "")

    clear()
    with pytest.raises(InputError):
        assert auth_register("ankitrai326@gmail.com", "12345678", "tom", "A" * 51)

def test_auth_register_return_u_id():
    '''
    test to check registered u_id has been returned
    '''
    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    profile = user_profile(user_dict['token'], user_dict['u_id'])
    assert profile['user']['u_id'] == user_dict['u_id']

def test_auth_register_return_token():
    '''
    test to check if valid token has been generated which can be used to
    logout in auth_logout
    '''
    clear()
    user_info = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    user_dict = auth_logout(user_info['token'])
    assert user_dict['is_success']

def test_auth_register_unique_token():
    '''
    test to check if tokens generated are unique by registering many users and
    checking if their tokens are valid
    '''
    clear()
    token_list = []
    for i in range(1000):
        user_info = auth_register(str(i) + "ankitrai@gmail.com", "12345678", "tom", "hardy")
        token_list.append(user_info['token'])

    # if size of list and set is equal, then no duplicate tokens
    assert len(token_list) == len(set(token_list))

def test_auth_register_return_handle():
    '''
    test to check if valid and proper handle has been returned
    '''
    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    profile = user_profile(user_dict['token'], user_dict['u_id'])
    assert profile['user']['handle_str'] == "tomhardy"

def test_auth_register_handle_concatenates():
    '''
    test to check if the handle concatenates at 20 characters max
    '''
    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardydeathofabachelorrr")
    profile = user_profile(user_dict['token'], user_dict['u_id'])
    assert profile['user']['handle_str'] == "tomhardydeathofabach"

def test_auth_register_handle_lowercase_only():
    '''
    test to check if handle converts everything to lowercase only
    '''
    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "toM", "HaRdY")
    profile = user_profile(user_dict['token'], user_dict['u_id'])
    assert profile['user']['handle_str'] == "tomhardy"

# Tests for auth_login:
def test_auth_login_unregistered_email():
    '''
    raises InputError if unregistered email is used to login
    '''
    clear()
    with pytest.raises(InputError):
        assert auth_login("ankitrai326@gmail.com", "12345678")

def test_auth_login_wrong_password():
    '''
    raises InputError if wrong password is used to login
    '''
    clear()
    auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    with pytest.raises(InputError):
        assert auth_login("ankitrai326@gmail.com", "wrong123")

def test_auth_login_invalid_email():
    '''
    raises InputError if email is invalid
    '''
    clear()
    with pytest.raises(InputError):
        assert auth_login("ankitrai326.com", "12345678")

def test_auth_login_return():
    '''
    test to check if auth_login returns the appriopriate return values (u_id)
    '''
    clear()
    auth_register("ankitrai001@gmail.com", "12345678", "tom", "hardy")
    auth_register("ankitrai002@gmail.com", "12345678", "tom", "hardy")
    user_dict1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    auth_logout(user_dict1['token'])
    user_dict2 = auth_login("ankitrai326@gmail.com", "12345678")
    profile = user_profile(user_dict2['token'], user_dict2['u_id'])
    assert profile['user']['u_id'] == user_dict2['u_id']

# Tests for auth_logout:
def test_auth_logout_invalid_token():
    '''
    return value is False if token is invalid
    '''
    clear()
    value = auth_logout(12345)
    assert not value['is_success']

    clear()
    value = auth_logout(50000)
    assert not value['is_success']

    clear()
    user_dict = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    invalid_token = user_dict['token'] + "abc"
    value = auth_logout(invalid_token)
    assert not value['is_success']

def test_auth_logout_valid_token():
    '''
    return value is True when token is valid
    '''
    clear()
    user_info = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    user_dict = auth_logout(user_info['token'])
    assert user_dict['is_success']

    user_info = auth_login("ankitrai326@gmail.com", "12345678")
    user_dict = auth_logout(user_info['token'])
    assert user_dict['is_success']

def test_auth_logout_token_invalidated():
    '''
    tests and confirms token has been invalidated after logging out by
    logging out twice with the same token will result in the first one
    returning True, and the second one returning False
    '''
    clear()
    user_info = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    user_dict = auth_logout(user_info['token'])
    user_dict1 = auth_logout(user_info['token'])
    assert user_dict['is_success']
    assert not user_dict1['is_success']

# Tests for auth_passwordreset_request:
def test_auth_passwordreset_request_unregistered_email():
    '''
    test to check if InputError is raised when unregistered email is used
    '''
    clear()
    with pytest.raises(InputError):
        assert auth_passwordreset_request("ankitrai326@gmail.com")

# Tests for auth_passwordreset_reset:
def test_auth_passwordreset_reset_invalid_password():
    '''
    test to check if InputError is raised when invalid password is used
    (less than 6 characters long)
    '''
    clear()
    with pytest.raises(InputError):
        assert auth_passwordreset_reset("123456", "A")

    clear()
    with pytest.raises(InputError):
        assert auth_passwordreset_reset("123456", "A"*5)

def test_auth_passwordreset_reset_invalid_reset_code():
    '''
    test to check if valid password is given and invalid reset code is given,
    InputError will be raised
    '''
    clear()
    with pytest.raises(InputError):
        assert auth_passwordreset_reset("A" * 1000, "12345678")
