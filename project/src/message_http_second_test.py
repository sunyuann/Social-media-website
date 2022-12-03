'''requests is imported to obtain data from flask server'''
import requests
import pytest

@pytest.mark.usefixtures("url")
def test_url(url):
    '''
    A simple sanity test to check that your server is set up properly
    '''
    assert url.startswith("http")

# message_react tests
def test_message_react_http_invalid_token(url):
    '''
    Should raise InputError when an invalid token is passed
    '''
    requests.delete(f'{url}/clear')

    response1 = requests.post(f'{url}/auth/register', json={
        'email': 'example@gmail.com',
        'password':'12345678',
        'name_first': 'john',
        'name_last':'smith'
    })
    register_payload = response1.json()

    response2 = requests.post(f'{url}/channels/create', json={
        'token': register_payload['token'],
        'name': 'channel1',
        'is_public': True
    })
    channel_payload = response2.json()

    response3 = requests.post(f'{url}/message/send', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': 'blah blah'
    })
    message_payload = response3.json()

    invalid_token = register_payload['token'] + "rhjwkrw"
    response4 = requests.post(f'{url}/message/react', json={
        'token': invalid_token,
        'message_id': message_payload['message_id'],
        'react_id': 1
    })
    react_payload = response4.json()

    assert react_payload['code'] == 400
    assert react_payload['message'] == '<p>Invalid token entered</p>'

def test_message_react_http_invalid_message_id(url):
    '''
    Should raise InputError when an invalid message id is passed
    '''
    requests.delete(f'{url}/clear')

    response1 = requests.post(f'{url}/auth/register', json={
        'email': 'example@gmail.com',
        'password':'12345678',
        'name_first': 'john',
        'name_last':'smith'
    })
    register_payload = response1.json()

    response2 = requests.post(f'{url}/channels/create', json={
        'token': register_payload['token'],
        'name': 'channel1',
        'is_public': True
    })
    channel_payload = response2.json()

    requests.post(f'{url}/message/send', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': 'blah blah'
    })

    invalid_message_id = 35467
    response4 = requests.post(f'{url}/message/react', json={
        'token': register_payload['token'],
        'message_id': invalid_message_id,
        'react_id': 1
    })
    react_payload = response4.json()

    assert react_payload['code'] == 400
    assert react_payload['message'] == '<p>Message cannot be found in any channel</p>'

def test_message_react_http_invalid_react_id(url):
    '''
    Should raise InputError when an invalid react id is passed
    '''
    requests.delete(f'{url}/clear')

    response1 = requests.post(f'{url}/auth/register', json={
        'email': 'example@gmail.com',
        'password':'12345678',
        'name_first': 'john',
        'name_last':'smith'
    })
    register_payload = response1.json()

    response2 = requests.post(f'{url}/channels/create', json={
        'token': register_payload['token'],
        'name': 'channel1',
        'is_public': True
    })
    channel_payload = response2.json()

    response3 = requests.post(f'{url}/message/send', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': 'blah blah'
    })
    message_payload = response3.json()

    invalid_react_id = 354
    response4 = requests.post(f'{url}/message/react', json={
        'token': register_payload['token'],
        'message_id': message_payload['message_id'],
        'react_id': invalid_react_id
    })
    react_payload = response4.json()

    assert react_payload['code'] == 400
    assert react_payload['message'] == '<p>Invalid react id</p>'

def test_message_react_http_message_already_contain_active_react_id_from_the_user(url):
    '''
    Should raise InputError in the case where the message with
    message_id already has an active react from the user
    '''
    requests.delete(f'{url}/clear')

    response1 = requests.post(f'{url}/auth/register', json={
        'email': 'example@gmail.com',
        'password':'12345678',
        'name_first': 'john',
        'name_last':'smith'
    })
    register_payload = response1.json()

    response2 = requests.post(f'{url}/channels/create', json={
        'token': register_payload['token'],
        'name': 'channel1',
        'is_public': True
    })
    channel_payload = response2.json()

    response3 = requests.post(f'{url}/message/send', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': 'blah blah'
    })
    message_payload = response3.json()

    requests.post(f'{url}/message/react', json={
        'token': register_payload['token'],
        'message_id': message_payload['message_id'],
        'react_id': 1
    })

    response5 = requests.post(f'{url}/message/react', json={
        'token': register_payload['token'],
        'message_id': message_payload['message_id'],
        'react_id': 1
    })
    react2_payload = response5.json()

    error_message = "<p>Message already contains an active react from the user</p>"
    assert react2_payload['code'] == 400
    assert react2_payload['message'] == error_message

def test_message_react_http_all_valid(url):
    '''
    Function used as intended
    '''
    requests.delete(f'{url}/clear')

    response1 = requests.post(f'{url}/auth/register', json={
        'email': 'example@gmail.com',
        'password':'12345678',
        'name_first': 'john',
        'name_last':'smith'
    })
    register_payload = response1.json()

    response2 = requests.post(f'{url}/channels/create', json={
        'token': register_payload['token'],
        'name': 'channel1',
        'is_public': True
    })
    channel_payload = response2.json()

    response3 = requests.post(f'{url}/message/send', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': 'blah blah'
    })
    message_payload = response3.json()

    requests.post(f'{url}/message/react', json={
        'token': register_payload['token'],
        'message_id': message_payload['message_id'],
        'react_id': 1
    })

    in_url = f"{url}/channel/messages?token={register_payload['token']}&"
    in_url2 = f"channel_id={channel_payload['channel_id']}&start=0"
    message_list = requests.get(in_url + in_url2)
    channel_messages = message_list.json()

    assert register_payload['u_id'] in channel_messages['messages'][0]['reacts'][0]['u_ids']

# message_unreact tests
def test_message_unreact_http_invalid_token(url):
    '''
    Should raise InputError when an invalid token is passed
    '''
    requests.delete(f'{url}/clear')

    response1 = requests.post(f'{url}/auth/register', json={
        'email': 'example@gmail.com',
        'password':'12345678',
        'name_first': 'john',
        'name_last':'smith'
    })
    register_payload = response1.json()

    response2 = requests.post(f'{url}/channels/create', json={
        'token': register_payload['token'],
        'name': 'channel1',
        'is_public': True
    })
    channel_payload = response2.json()

    response3 = requests.post(f'{url}/message/send', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': 'blah blah'
    })
    message_payload = response3.json()

    requests.post(f'{url}/message/react', json={
        'token': register_payload['token'],
        'message_id': message_payload['message_id'],
        'react_id': 1
    })

    invalid_token = register_payload['token'] + "rhjwkrw"
    response5 = requests.post(f'{url}/message/unreact', json={
        'token': invalid_token,
        'message_id': message_payload['message_id'],
        'react_id': 1
    })
    unreact_payload = response5.json()

    assert unreact_payload['code'] == 400
    assert unreact_payload['message'] == '<p>Invalid token entered</p>'

def test_message_unreact_http_invalid_message_id(url):
    '''
    Should raise InputError when an invalid message id is passed
    '''
    requests.delete(f'{url}/clear')

    response1 = requests.post(f'{url}/auth/register', json={
        'email': 'example@gmail.com',
        'password':'12345678',
        'name_first': 'john',
        'name_last':'smith'
    })
    register_payload = response1.json()

    response2 = requests.post(f'{url}/channels/create', json={
        'token': register_payload['token'],
        'name': 'channel1',
        'is_public': True
    })
    channel_payload = response2.json()

    response3 = requests.post(f'{url}/message/send', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': 'blah blah'
    })
    message_payload = response3.json()

    requests.post(f'{url}/message/react', json={
        'token': register_payload['token'],
        'message_id': message_payload['message_id'],
        'react_id': 1
    })

    invalid_message_id = 35467
    response5 = requests.post(f'{url}/message/unreact', json={
        'token': register_payload['token'],
        'message_id': invalid_message_id,
        'react_id': 1
    })
    unreact_payload = response5.json()

    assert unreact_payload['code'] == 400
    assert unreact_payload['message'] == '<p>Message cannot be found in any channel</p>'

def test_message_unreact_http_invalid_react_id(url):
    '''
    Should raise InputError when an invalid react id is passed
    '''
    requests.delete(f'{url}/clear')

    response1 = requests.post(f'{url}/auth/register', json={
        'email': 'example@gmail.com',
        'password':'12345678',
        'name_first': 'john',
        'name_last':'smith'
    })
    register_payload = response1.json()

    response2 = requests.post(f'{url}/channels/create', json={
        'token': register_payload['token'],
        'name': 'channel1',
        'is_public': True
    })
    channel_payload = response2.json()

    response3 = requests.post(f'{url}/message/send', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': 'blah blah'
    })
    message_payload = response3.json()

    requests.post(f'{url}/message/react', json={
        'token': register_payload['token'],
        'message_id': message_payload['message_id'],
        'react_id': 1
    })

    invalid_react_id = 354
    response5 = requests.post(f'{url}/message/unreact', json={
        'token': register_payload['token'],
        'message_id': message_payload['message_id'],
        'react_id': invalid_react_id
    })
    unreact_payload = response5.json()

    assert unreact_payload['code'] == 400
    assert unreact_payload['message'] == '<p>Invalid react id</p>'

def test_message_unreact_http_message_does_not_contain_active_react_id_from_the_user(url):
    '''
    Should raise InputError when the message with message_id
    does not contain an active react from the user
    '''
    requests.delete(f'{url}/clear')

    response1 = requests.post(f'{url}/auth/register', json={
        'email': 'example@gmail.com',
        'password':'12345678',
        'name_first': 'john',
        'name_last':'smith'
    })
    register_payload = response1.json()

    response2 = requests.post(f'{url}/channels/create', json={
        'token': register_payload['token'],
        'name': 'channel1',
        'is_public': True
    })
    channel_payload = response2.json()

    response3 = requests.post(f'{url}/message/send', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': 'blah blah'
    })
    message_payload = response3.json()

    requests.post(f'{url}/message/react', json={
        'token': register_payload['token'],
        'message_id': message_payload['message_id'],
        'react_id': 1
    })

    requests.post(f'{url}/message/unreact', json={
        'token': register_payload['token'],
        'message_id': message_payload['message_id'],
        'react_id': 1
    })

    response6 = requests.post(f'{url}/message/unreact', json={
        'token': register_payload['token'],
        'message_id': message_payload['message_id'],
        'react_id': 1
    })
    unreact2_payload = response6.json()

    error_message = "<p>Message does not contain an active react from the user</p>"
    assert unreact2_payload['code'] == 400
    assert unreact2_payload['message'] == error_message

def test_message_unreact_http_all_valid(url):
    '''
    Function used as intended
    '''
    requests.delete(f'{url}/clear')

    response1 = requests.post(f'{url}/auth/register', json={
        'email': 'example@gmail.com',
        'password':'12345678',
        'name_first': 'john',
        'name_last':'smith'
    })
    register_payload = response1.json()

    response2 = requests.post(f'{url}/channels/create', json={
        'token': register_payload['token'],
        'name': 'channel1',
        'is_public': True
    })
    channel_payload = response2.json()

    response3 = requests.post(f'{url}/message/send', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': 'blah blah'
    })
    message_payload = response3.json()

    requests.post(f'{url}/message/react', json={
        'token': register_payload['token'],
        'message_id': message_payload['message_id'],
        'react_id': 1
    })

    requests.post(f'{url}/message/unreact', json={
        'token': register_payload['token'],
        'message_id': message_payload['message_id'],
        'react_id': 1
    })

    in_url = f"{url}/channel/messages?token={register_payload['token']}&"
    in_url2 = f"channel_id={channel_payload['channel_id']}&start=0"
    message_list = requests.get(in_url + in_url2)
    channel_messages = message_list.json()

    assert channel_messages['messages'][0]['reacts'][0]['u_ids'] == []

# message_pin tests
def test_message_pin_http_invalid_token(url):
    '''
    Should raise InputError when an invalid token is passed
    '''
    requests.delete(f'{url}/clear')

    response1 = requests.post(f'{url}/auth/register', json={
        'email': 'example@gmail.com',
        'password':'12345678',
        'name_first': 'john',
        'name_last':'smith'
    })
    register_payload = response1.json()

    response2 = requests.post(f'{url}/channels/create', json={
        'token': register_payload['token'],
        'name': 'channel1',
        'is_public': True
    })
    channel_payload = response2.json()

    response3 = requests.post(f'{url}/message/send', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': 'blah blah'
    })
    message_payload = response3.json()

    invalid_token = register_payload['token'] + "rhjwkrw"
    response4 = requests.post(f'{url}/message/pin', json={
        'token': invalid_token,
        'message_id': message_payload['message_id']
    })
    pin_payload = response4.json()

    assert pin_payload['code'] == 400
    assert pin_payload['message'] == '<p>Invalid token entered</p>'

def test_message_pin_http_invalid_message_id(url):
    '''
    Should raise InputError when an invalid message id is passed
    '''
    requests.delete(f'{url}/clear')

    response1 = requests.post(f'{url}/auth/register', json={
        'email': 'example@gmail.com',
        'password':'12345678',
        'name_first': 'john',
        'name_last':'smith'
    })
    register_payload = response1.json()

    response2 = requests.post(f'{url}/channels/create', json={
        'token': register_payload['token'],
        'name': 'channel1',
        'is_public': True
    })
    channel_payload = response2.json()

    requests.post(f'{url}/message/send', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': 'blah blah'
    })

    invalid_message_id = 35467
    response4 = requests.post(f'{url}/message/pin', json={
        'token': register_payload['token'],
        'message_id': invalid_message_id
    })
    pin_payload = response4.json()

    assert pin_payload['code'] == 400
    assert pin_payload['message'] == '<p>Message cannot be found in any channel</p>'

def test_message_pin_http_message_already_pinned(url):
    '''
    Should raise InputError when attempting to pin a pinned message
    '''
    requests.delete(f'{url}/clear')

    response1 = requests.post(f'{url}/auth/register', json={
        'email': 'example@gmail.com',
        'password':'12345678',
        'name_first': 'john',
        'name_last':'smith'
    })
    register_payload = response1.json()

    response2 = requests.post(f'{url}/channels/create', json={
        'token': register_payload['token'],
        'name': 'channel1',
        'is_public': True
    })
    channel_payload = response2.json()

    response3 = requests.post(f'{url}/message/send', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': 'blah blah'
    })
    message_payload = response3.json()

    requests.post(f'{url}/message/pin', json={
        'token': register_payload['token'],
        'message_id': message_payload['message_id']
    })

    response5 = requests.post(f'{url}/message/pin', json={
        'token': register_payload['token'],
        'message_id': message_payload['message_id']
    })
    pin_payload = response5.json()

    assert pin_payload['code'] == 400
    assert pin_payload['message'] == "<p>Message is already pinned</p>"

def test_message_pin_http_user_is_not_member_of_channel(url):
    '''
    Should raise AccessError when the user is not a member of the channel
    '''
    requests.delete(f'{url}/clear')

    response1 = requests.post(f'{url}/auth/register', json={
        'email': 'example@gmail.com',
        'password':'12345678',
        'name_first': 'john',
        'name_last':'smith'
    })
    register_payload = response1.json()

    response2 = requests.post(f'{url}/channels/create', json={
        'token': register_payload['token'],
        'name': 'channel1',
        'is_public': True
    })
    channel_payload = response2.json()

    response3 = requests.post(f'{url}/message/send', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': 'blah blah'
    })
    message_payload = response3.json()

    response4 = requests.post(f'{url}/auth/register', json={
        'email': 'example234@gmail.com',
        'password':'12345678',
        'name_first': 'john',
        'name_last':'smith'
    })
    register2_payload = response4.json()

    response5 = requests.post(f'{url}/message/pin', json={
        'token': register2_payload['token'],
        'message_id': message_payload['message_id']
    })
    pin_payload = response5.json()

    assert pin_payload['code'] == 400
    assert pin_payload['message'] == "<p>User has no permissions to pin message</p>"

def test_message_pin_http_user_is_member_but_not_owner_of_channel(url):
    '''
    Should raise AccessError when the user is a member but not an owner of the channel
    '''
    requests.delete(f'{url}/clear')

    response1 = requests.post(f'{url}/auth/register', json={
        'email': 'example@gmail.com',
        'password':'12345678',
        'name_first': 'john',
        'name_last':'smith'
    })
    register_payload = response1.json()

    response2 = requests.post(f'{url}/channels/create', json={
        'token': register_payload['token'],
        'name': 'channel1',
        'is_public': True
    })
    channel_payload = response2.json()

    response3 = requests.post(f'{url}/message/send', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': 'blah blah'
    })
    message_payload = response3.json()

    response4 = requests.post(f'{url}/auth/register', json={
        'email': 'example234@gmail.com',
        'password':'12345678',
        'name_first': 'john',
        'name_last':'smith'
    })
    register2_payload = response4.json()

    requests.post(f'{url}/channel/join', json={
        'token': register2_payload['token'],
        'channel_id': channel_payload['channel_id']
    })

    response6 = requests.post(f'{url}/message/pin', json={
        'token': register2_payload['token'],
        'message_id': message_payload['message_id']
    })
    pin_payload = response6.json()

    assert pin_payload['code'] == 400
    assert pin_payload['message'] == "<p>User has no permissions to pin message</p>"

def test_message_pin_http_all_valid(url):
    '''
    Function used as intended
    '''
    requests.delete(f'{url}/clear')

    response1 = requests.post(f'{url}/auth/register', json={
        'email': 'example@gmail.com',
        'password':'12345678',
        'name_first': 'john',
        'name_last':'smith'
    })
    register_payload = response1.json()

    response2 = requests.post(f'{url}/channels/create', json={
        'token': register_payload['token'],
        'name': 'channel1',
        'is_public': True
    })
    channel_payload = response2.json()

    response3 = requests.post(f'{url}/message/send', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': 'blah blah'
    })
    message_payload = response3.json()

    requests.post(f'{url}/message/pin', json={
        'token': register_payload['token'],
        'message_id': message_payload['message_id']
    })

    in_url = f"{url}/channel/messages?token={register_payload['token']}&"
    in_url2 = f"channel_id={channel_payload['channel_id']}&start=0"
    message_list = requests.get(in_url + in_url2)
    channel_messages = message_list.json()

    assert channel_messages['messages'][0]['is_pinned']

# message_unpin tests
def test_message_unpin_http_invalid_token(url):
    '''
    Should raise InputError when an invalid token is passed
    '''
    requests.delete(f'{url}/clear')

    response1 = requests.post(f'{url}/auth/register', json={
        'email': 'example@gmail.com',
        'password':'12345678',
        'name_first': 'john',
        'name_last':'smith'
    })
    register_payload = response1.json()

    response2 = requests.post(f'{url}/channels/create', json={
        'token': register_payload['token'],
        'name': 'channel1',
        'is_public': True
    })
    channel_payload = response2.json()

    response3 = requests.post(f'{url}/message/send', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': 'blah blah'
    })
    message_payload = response3.json()

    requests.post(f'{url}/message/pin', json={
        'token': register_payload['token'],
        'message_id': message_payload['message_id']
    })

    invalid_token = register_payload['token'] + "rhjwkrw"
    response5 = requests.post(f'{url}/message/unpin', json={
        'token': invalid_token,
        'message_id': message_payload['message_id']
    })
    unpin_payload = response5.json()

    assert unpin_payload['code'] == 400
    assert unpin_payload['message'] == '<p>Invalid token entered</p>'

def test_message_unpin_http_invalid_message_id(url):
    '''
    Should raise InputError when an invalid message id is passed
    '''
    requests.delete(f'{url}/clear')

    response1 = requests.post(f'{url}/auth/register', json={
        'email': 'example@gmail.com',
        'password':'12345678',
        'name_first': 'john',
        'name_last':'smith'
    })
    register_payload = response1.json()

    response2 = requests.post(f'{url}/channels/create', json={
        'token': register_payload['token'],
        'name': 'channel1',
        'is_public': True
    })
    channel_payload = response2.json()

    response3 = requests.post(f'{url}/message/send', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': 'blah blah'
    })
    message_payload = response3.json()

    requests.post(f'{url}/message/pin', json={
        'token': register_payload['token'],
        'message_id': message_payload['message_id']
    })

    invalid_message_id = 35467
    response5 = requests.post(f'{url}/message/unpin', json={
        'token': register_payload['token'],
        'message_id': invalid_message_id
    })
    unpin_payload = response5.json()

    assert unpin_payload['code'] == 400
    assert unpin_payload['message'] == '<p>Message cannot be found in any channel</p>'

def test_message_unpin_http_message_is_not_pinned(url):
    '''
    Should raise InputError when attempting to unpin a message that is not pinned
    '''
    requests.delete(f'{url}/clear')

    response1 = requests.post(f'{url}/auth/register', json={
        'email': 'example@gmail.com',
        'password':'12345678',
        'name_first': 'john',
        'name_last':'smith'
    })
    register_payload = response1.json()

    response2 = requests.post(f'{url}/channels/create', json={
        'token': register_payload['token'],
        'name': 'channel1',
        'is_public': True
    })
    channel_payload = response2.json()

    response3 = requests.post(f'{url}/message/send', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': 'blah blah'
    })
    message_payload = response3.json()

    response4 = requests.post(f'{url}/message/unpin', json={
        'token': register_payload['token'],
        'message_id': message_payload['message_id']
    })
    unpin_payload = response4.json()

    assert unpin_payload['code'] == 400
    assert unpin_payload['message'] == "<p>Message is already unpinned</p>"

def test_message_unpin_http_user_is_not_member_of_channel(url):
    '''
    Should raise AccessError when the user is not a member of the channel
    '''
    requests.delete(f'{url}/clear')

    response1 = requests.post(f'{url}/auth/register', json={
        'email': 'example@gmail.com',
        'password':'12345678',
        'name_first': 'john',
        'name_last':'smith'
    })
    register_payload = response1.json()

    response2 = requests.post(f'{url}/channels/create', json={
        'token': register_payload['token'],
        'name': 'channel1',
        'is_public': True
    })
    channel_payload = response2.json()

    response3 = requests.post(f'{url}/message/send', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': 'blah blah'
    })
    message_payload = response3.json()

    requests.post(f'{url}/message/pin', json={
        'token': register_payload['token'],
        'message_id': message_payload['message_id']
    })

    response5 = requests.post(f'{url}/auth/register', json={
        'email': 'example424892@gmail.com',
        'password':'12345678',
        'name_first': 'john',
        'name_last':'smith'
    })
    register2_payload = response5.json()

    response6 = requests.post(f'{url}/message/unpin', json={
        'token': register2_payload['token'],
        'message_id': message_payload['message_id']
    })
    unpin_payload = response6.json()

    assert unpin_payload['code'] == 400
    assert unpin_payload['message'] == "<p>User has no permissions to unpin message</p>"

def test_message_unpin_http_user_is_member_but_not_owner_of_channel(url):
    '''
    Should raise AccessError when the user is a member but not an owner of the channel
    '''
    requests.delete(f'{url}/clear')

    response1 = requests.post(f'{url}/auth/register', json={
        'email': 'example@gmail.com',
        'password':'12345678',
        'name_first': 'john',
        'name_last':'smith'
    })
    register_payload = response1.json()

    response2 = requests.post(f'{url}/channels/create', json={
        'token': register_payload['token'],
        'name': 'channel1',
        'is_public': True
    })
    channel_payload = response2.json()

    response3 = requests.post(f'{url}/message/send', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': 'blah blah'
    })
    message_payload = response3.json()

    requests.post(f'{url}/message/pin', json={
        'token': register_payload['token'],
        'message_id': message_payload['message_id']
    })

    response5 = requests.post(f'{url}/auth/register', json={
        'email': 'example424892@gmail.com',
        'password':'12345678',
        'name_first': 'john',
        'name_last':'smith'
    })
    register2_payload = response5.json()

    requests.post(f'{url}/channel/join', json={
        'token': register2_payload['token'],
        'channel_id': channel_payload['channel_id']
    })

    response7 = requests.post(f'{url}/message/unpin', json={
        'token': register2_payload['token'],
        'message_id': message_payload['message_id']
    })
    unpin_payload = response7.json()

    assert unpin_payload['code'] == 400
    assert unpin_payload['message'] == "<p>User has no permissions to unpin message</p>"

def test_message_unpin_http_all_valid(url):
    '''
    Function used as intended
    '''
    requests.delete(f'{url}/clear')

    response1 = requests.post(f'{url}/auth/register', json={
        'email': 'example@gmail.com',
        'password':'12345678',
        'name_first': 'john',
        'name_last':'smith'
    })
    register_payload = response1.json()

    response2 = requests.post(f'{url}/channels/create', json={
        'token': register_payload['token'],
        'name': 'channel1',
        'is_public': True
    })
    channel_payload = response2.json()

    response3 = requests.post(f'{url}/message/send', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': 'blah blah'
    })
    message_payload = response3.json()

    requests.post(f'{url}/message/pin', json={
        'token': register_payload['token'],
        'message_id': message_payload['message_id']
    })

    requests.post(f'{url}/message/unpin', json={
        'token': register_payload['token'],
        'message_id': message_payload['message_id']
    })

    in_url = f"{url}/channel/messages?token={register_payload['token']}&"
    in_url2 = f"channel_id={channel_payload['channel_id']}&start=0"
    message_list = requests.get(in_url + in_url2)
    channel_messages = message_list.json()

    assert not channel_messages['messages'][0]['is_pinned']
