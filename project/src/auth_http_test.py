'''requests is imported to obtain data from flask server'''
import requests
import pytest

@pytest.mark.usefixtures("url")
def test_url(url):
    '''
    A simple sanity test to check that your server is set up properly
    '''
    assert url.startswith("http")

# Tests for auth_register:
def test_auth_register_http_valid_email(url):
    '''
    test to check registered email is valid and return value is same as
    registered email
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

    assert user_details_payload['user']['email'] == 'ankitrai326@gmail.com'

def test_auth_register_http_invalid_email(url):
    '''
    raises InputError if email entered is invalid
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()

    assert register_payload['code'] == 400
    assert register_payload['message'] == '<p>Invalid email address entered</p>'

def test_auth_register_http_email_in_use(url):
    '''
    raises InputError if same email is registered the second time (in use)
    '''
    requests.delete(f'{url}/clear')
    requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()

    error_message = '<p>Email address is already being used by another user</p>'
    assert register_payload['code'] == 400
    assert register_payload['message'] == error_message

def test_auth_register_http_valid_password(url):
    '''
    checks if the email of the user is the registered email, this indicates
    that the user has entered a valid password and the user has been registered
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '123456',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()

    in_url = f"{url}/user/profile?token={register_payload['token']}&u_id={register_payload['u_id']}"
    response = requests.get(in_url)
    user_details_payload = response.json()

    assert user_details_payload['user']['email'] == 'ankitrai326@gmail.com'

    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678joeeeee',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()

    in_url = f"{url}/user/profile?token={register_payload['token']}&u_id={register_payload['u_id']}"
    response = requests.get(in_url)
    user_details_payload = response.json()

    assert user_details_payload['user']['email'] == 'ankitrai326@gmail.com'

def test_auth_register_http_invalid_password(url):
    '''
    raises InputError if user registers with invalid password
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    assert register_payload['code'] == 400
    assert register_payload['message'] == '<p>Password cannot be less than 6 characters long</p>'

    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': 'a',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()

    assert register_payload['code'] == 400
    assert register_payload['message'] == '<p>Password cannot be less than 6 characters long</p>'

def test_auth_register_http_valid_name_first(url):
    '''
    test to check valid name_first has been entered
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'A',
        'name_last': 'hardy'
    })
    register_payload = response.json()

    in_url = f"{url}/user/profile?token={register_payload['token']}&u_id={register_payload['u_id']}"
    response = requests.get(in_url)
    user_details_payload = response.json()

    assert user_details_payload['user']['name_first'] == 'A'

    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'A' * 50,
        'name_last': 'hardy'
    })
    register_payload = response.json()

    in_url = f"{url}/user/profile?token={register_payload['token']}&u_id={register_payload['u_id']}"
    response = requests.get(in_url)
    user_details_payload = response.json()

    assert user_details_payload['user']['name_first'] == 'A' * 50

def test_auth_register_http_invalid_name_first(url):
    '''
    raises InputError if user registers with invalid name_first
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': '',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    assert register_payload['code'] == 400
    assert register_payload['message'] == '<p>Invalid first name</p>'

    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'A' * 51,
        'name_last': 'hardy'
    })
    register_payload = response.json()

    assert register_payload['code'] == 400
    assert register_payload['message'] == '<p>Invalid first name</p>'

def test_auth_register_http_valid_name_last(url):
    '''
    test to check valid name_last
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'A'
    })
    register_payload = response.json()

    in_url = f"{url}/user/profile?token={register_payload['token']}&u_id={register_payload['u_id']}"
    response = requests.get(in_url)
    user_details_payload = response.json()

    assert user_details_payload['user']['name_last'] == 'A'

    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'A' * 50
    })
    register_payload = response.json()

    in_url = f"{url}/user/profile?token={register_payload['token']}&u_id={register_payload['u_id']}"
    response = requests.get(in_url)
    user_details_payload = response.json()

    assert user_details_payload['user']['name_last'] == 'A' * 50

def test_auth_register_http_invalid_name_last(url):
    '''
    raises InputError if user registers with invalid name_last
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': ''
    })
    register_payload = response.json()
    assert register_payload['code'] == 400
    assert register_payload['message'] == '<p>Invalid last name</p>'

    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'A' * 51
    })
    register_payload = response.json()

    assert register_payload['code'] == 400
    assert register_payload['message'] == '<p>Invalid last name</p>'

def test_auth_register_http_return_u_id(url):
    '''
    test to check registered u_id has been returned
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

    assert register_payload['u_id'] == user_details_payload['user']['u_id']

def test_auth_register_http_return_token(url):
    '''
    test to check if valid token has been generated which can be used to
    logout in auth_logout
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()

    response = requests.post(f'{url}/auth/logout', json={
        'token': register_payload['token']
    })
    logout_payload = response.json()

    assert logout_payload['is_success']

def test_auth_register_http_return_handle(url):
    '''
    test to check if valid and proper handle has been returned
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

    assert user_details_payload['user']['handle_str'] == 'tomhardy'

def test_auth_register_http_handle_concatenates(url):
    '''
    test to check if the handle concatenates at 20 characters max
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardydeathofabachelorrrrrr'
    })
    register_payload = response.json()

    in_url = f"{url}/user/profile?token={register_payload['token']}&u_id={register_payload['u_id']}"
    response = requests.get(in_url)
    user_details_payload = response.json()

    assert user_details_payload['user']['handle_str'] == 'tomhardydeathofabach'

def test_auth_register_http_handle_lowercase_only(url):
    '''
    test to check if handle converts everything to lowercase only
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'toM',
        'name_last': 'HaRdY'
    })
    register_payload = response.json()

    in_url = f"{url}/user/profile?token={register_payload['token']}&u_id={register_payload['u_id']}"
    response = requests.get(in_url)
    user_details_payload = response.json()

    assert user_details_payload['user']['handle_str'] == 'tomhardy'

# Tests for auth_login:
def test_auth_login_http_unregistered_email(url):
    '''
    raises InputError if unregistered email is used to login
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/login', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
    })
    login_payload = response.json()
    assert login_payload['code'] == 400
    assert login_payload['message'] == '<p>Email entered does not belong to a user</p>'

def test_auth_login_http_wrong_password(url):
    '''
    raises InputError if wrong password is used to login
    '''
    requests.delete(f'{url}/clear')
    requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    response = requests.post(f'{url}/auth/login', json={
        'email': 'ankitrai326@gmail.com',
        'password': 'wrong123',
    })
    login_payload = response.json()
    assert login_payload['code'] == 400
    assert login_payload['message'] == '<p>Password entered is incorrect</p>'

def test_auth_login_http_return(url):
    '''
    test to check if auth_login returns the appriopriate return values (u_id)
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()

    requests.post(f'{url}/auth/logout', json={
        'token': register_payload['token']
    })

    response = requests.post(f'{url}/auth/login', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
    })
    login_payload = response.json()

    in_url = f"{url}/user/profile?token={login_payload['token']}&u_id={login_payload['u_id']}"
    response = requests.get(in_url)
    user_details_payload = response.json()

    assert user_details_payload['user']['u_id'] == register_payload['u_id']

# Tests for auth_logout:
def test_auth_logout_http_invalid_token(url):
    '''
    return value is False if token is invalid
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/logout', json={
        'token': '12345'
    })
    logout_payload = response.json()
    assert not logout_payload['is_success']

    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/logout', json={
        'token': '50000'
    })
    logout_payload = response.json()
    assert not logout_payload['is_success']

def test_auth_logout_http_valid_token(url):
    '''
    return value is True when token is valid
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()

    response = requests.post(f'{url}/auth/logout', json={
        'token': register_payload['token']
    })
    logout_payload = response.json()
    assert logout_payload['is_success']

    response = requests.post(f'{url}/auth/login', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
    })
    login_payload = response.json()
    response = requests.post(f'{url}/auth/logout', json={
        'token': login_payload['token']
    })
    logout_payload = response.json()
    assert logout_payload['is_success']

def test_auth_logout_http_token_invalidated(url):
    '''
    tests and confirms token has been invalidated after logging out by
    logging out twice with the same token will result in the first one
    returning True, and the second one returning False
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()

    response = requests.post(f'{url}/auth/logout', json={
        'token': register_payload['token']
    })
    logout_payload_first = response.json()

    response = requests.post(f'{url}/auth/logout', json={
        'token': register_payload['token']
    })
    logout_payload_second = response.json()

    assert logout_payload_first['is_success']
    assert not logout_payload_second['is_success']

# Tests for auth_passwordreset_request:
def test_auth_passwordreset_request_http_unregistered_email(url):
    '''
    test to check if InputError is raised when unregistered email is used
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/passwordreset/request', json={
        'email': 'ankitrai326@gmail.com'
    })
    payload = response.json()

    assert payload['code'] == 400
    assert payload['message'] == '<p>User is not registered</p>'

# Tests for auth_passwordreset_reset:
def test_auth_passwordreset_reset_http_invalid_password(url):
    '''
    test to check if InputError is raised when invalid password is used
    (less than 6 characters long)
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/passwordreset/reset', json={
        'reset_code': '123456',
        'new_password': 'A'
    })
    payload = response.json()

    assert payload['code'] == 400
    assert payload['message'] == '<p>Password cannot be less than 6 characters long</p>'

    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/passwordreset/reset', json={
        'reset_code': '123456',
        'new_password': 'A'*5
    })
    payload = response.json()

    assert payload['code'] == 400
    assert payload['message'] == '<p>Password cannot be less than 6 characters long</p>'

def test_auth_passwordreset_reset_http_invalid_secret_code(url):
    '''
    test to check if valid password is given and invalid reset code is given,
    InputError will be raised
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/passwordreset/reset', json={
        'reset_code': 'A' * 1000,
        'new_password': '12345678'
    })
    payload = response.json()

    assert payload['code'] == 400
    assert payload['message'] == '<p>Invalid reset code entered</p>'
