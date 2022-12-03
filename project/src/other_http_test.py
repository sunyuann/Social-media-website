'''
requests is imported to obtain data from flask server
time is used for delays
'''
import time
import requests
import pytest

@pytest.mark.usefixtures("url")
def test_url(url):
    '''
    A simple sanity test to check that your server is set up properly
    '''
    assert url.startswith("http")

# Tests for admin_userpermission_change:
def test_admin_userpermission_change_http_invalid_uid(url):
    '''
    given an invalid u_id, raise InputError
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user1 = response.json()

    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai36@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user2 = response.json()

    response = requests.post(f'{url}/admin/userpermission/change', json={
        'token': user1['token'],
        'u_id': user2['u_id'] + 100,
        'permission_id': 1
    })
    result = response.json()
    assert result['code'] == 400
    assert result['message'] == '<p>Invalid user ID entered</p>'

def test_admin_userpermission_change_http_invalid_token(url):
    '''
    given an invalid token, raise InputError
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })

    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai36@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user2 = response.json()

    response = requests.post(f'{url}/admin/userpermission/change', json={
        'token': "invalid",
        'u_id': user2['u_id'],
        'permission_id': 1
    })
    result = response.json()
    assert result['code'] == 400
    assert result['message'] == '<p>Invalid token entered</p>'

def test_admin_userpermission_change_http_invalid_permission_id(url):
    '''
    given an invalid permission_id, raise InputError
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user1 = response.json()

    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai36@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user2 = response.json()

    response = requests.post(f'{url}/admin/userpermission/change', json={
        'token': user1['token'],
        'u_id': user2['u_id'],
        'permission_id': 100
    })
    result = response.json()
    assert result['message'] == '<p>Permission_id does not refer to a valid permission</p>'

def test_admin_userpermission_change_http_not_admin(url):
    '''
    given a token that is not a global member, raise AccessError
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })

    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai26@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user2 = response.json()

    response = requests.post(f'{url}/admin/userpermission/change', json={
        'token': user2['token'],
        'u_id': user2['u_id'],
        'permission_id': 1
    })
    result = response.json()
    assert result['code'] == 400
    assert result['message'] == "<p>Unauthorized user cannot change other's permissions</p>"

def test_admin_userpermission_change_http_valid(url):
    '''
    when function works as intended, new owner should be able to join a
    private channel with no errors
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user1 = response.json()

    response = requests.post(f'{url}/channels/create', json={
        'token': user1['token'],
        'name': 'channel',
        'is_public': False
    })
    channel = response.json()

    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai36@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user2 = response.json()

    response = requests.post(f'{url}/admin/userpermission/change', json={
        'token': user1['token'],
        'u_id': user2['u_id'],
        'permission_id': 1
    })

    response = requests.post(f'{url}/channel/join', json={
        'token': user2['token'],
        'channel_id': channel['channel_id']
    })
    result = response.json()
    assert result == {}

# Tests for users_all:
def test_users_all_http_invalid_token(url):
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
    invalid_token = register_payload['token'] + 'abc'
    response = requests.get(f"{url}/users/all?token={invalid_token}")
    user_details_payload = response.json()
    assert user_details_payload['code'] == 400
    assert user_details_payload['message'] == '<p>Invalid token entered</p>'

def test_users_all_http_valid(url):
    '''
    test to check that user with valid token returns correct information
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload = response.json()
    response = requests.get(f"{url}/users/all?token={register_payload['token']}")
    user_details_payload = response.json()
    assert user_details_payload['users'] == [
        {
            'u_id': register_payload['u_id'],
            'email': 'ankitrai326@gmail.com',
            'name_first': 'tom',
            'name_last': 'hardy',
            'handle_str': 'tomhardy'
        }
    ]

def test_users_all_http_multiple(url):
    '''
    test to check that multiple users with valid tokens return correct
    information
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    register_payload1 = response.json()
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai26@gmail.com',
        'password': '12345678',
        'name_first': 'christian',
        'name_last': 'bale'
    })
    register_payload2 = response.json()
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai36@gmail.com',
        'password': '12345678',
        'name_first': 'annie',
        'name_last': 'leonhart'
    })
    register_payload3 = response.json()

    response = requests.get(f"{url}/users/all?token={register_payload1['token']}")
    user_details_payload = response.json()
    assert user_details_payload['users'] == [
        {
            'u_id': register_payload1['u_id'],
            'email': 'ankitrai326@gmail.com',
            'name_first': 'tom',
            'name_last': 'hardy',
            'handle_str': 'tomhardy'
        },
        {
            'u_id': register_payload2['u_id'],
            'email': 'ankitrai26@gmail.com',
            'name_first': 'christian',
            'name_last': 'bale',
            'handle_str': 'christianbale'
        },
        {
            'u_id': register_payload3['u_id'],
            'email': 'ankitrai36@gmail.com',
            'name_first': 'annie',
            'name_last': 'leonhart',
            'handle_str': 'annieleonhart'
        }
    ]

# search tests
def test_search_http_single(url):
    '''
    Sends a sample messages, then calls search
    Function works as intended
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user = response.json()
    response = requests.post(f'{url}/channels/create', json={
        'token': user['token'],
        'name': 'channel',
        'is_public': True
    })
    channel = response.json()
    requests.post(f'{url}/message/send', json={
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': "Testing"
    })
    response = requests.get(f"{url}/search?token={user['token']}&query_str=Testing")
    matched_message = response.json()
    assert matched_message['messages'][0]['message'] == "Testing"

def test_search_http_multiple(url):
    '''
    Function works as intended, several messages sent
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user = response.json()
    response = requests.post(f'{url}/channels/create', json={
        'token': user['token'],
        'name': 'channel',
        'is_public': True
    })
    channel = response.json()
    requests.post(f'{url}/message/send', json={
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': "Testing"
    })
    requests.post(f'{url}/message/send', json={
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': "Testing"
    })
    in_url = f"{url}/channel/messages?token={user['token']}&"
    in_url2 = f"channel_id={channel['channel_id']}&start=0"
    response = requests.get(in_url + in_url2)
    messages = response.json()
    requests.post(f'{url}/message/send', json={
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': "Not to be returned"
    })
    response = requests.get(f"{url}/search?token={user['token']}&query_str=Testing")
    matched_list = response.json()
    assert matched_list['messages'] == messages['messages']

def test_search_http_multiple_channels(url):
    '''
    Function works as intended, several messages sent across several
    channels
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user = response.json()
    correct_list = []
    for i in range(1, 4):
        response = requests.post(f'{url}/channels/create', json={
            'token': user['token'],
            'name': str(i),
            'is_public': True
        })
        channel = response.json()
        requests.post(f'{url}/message/send', json={
            'token': user['token'],
            'channel_id': channel['channel_id'],
            'message': "Testing"
        })
        in_url = f"{url}/channel/messages?token={user['token']}&"
        in_url2 = f"channel_id={channel['channel_id']}&start=0"
        response = requests.get(in_url + in_url2)
        messages = response.json()
        requests.post(f'{url}/message/send', json={
            'token': user['token'],
            'channel_id': channel['channel_id'],
            'message': "Not to be returned"
        })
        correct_list += messages['messages']
    response = requests.get(f"{url}/search?token={user['token']}&query_str=Testing")
    matched_list = response.json()
    assert matched_list['messages'] == correct_list

# standup_start tests
def test_standup_start_invalid_channel_id(url):
    '''
    Returns InputError if given an invalid channel_id
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user = response.json()

    response = requests.post(f'{url}/channels/create', json={
        'token': user['token'],
        'name': "channel",
        'is_public': True
    })

    response = requests.post(f'{url}/standup/start', json={
        'token': user['token'],
        'channel_id': 123123,
        'length': 5
    })
    result = response.json()

    assert result['code'] == 400
    assert result['message'] == "<p>This is not a valid channel.</p>"

def test_standup_start_already_active(url):
    '''
    Returns InputError if a standup is already active in given channel
    '''
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user = response.json()

    response = requests.post(f'{url}/channels/create', json={
        'token': user['token'],
        'name': "channel",
        'is_public': True
    })
    channel = response.json()

    response = requests.post(f'{url}/standup/start', json={
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'length': 2
    })

    response = requests.post(f'{url}/standup/start', json={
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'length': 2
    })
    result = response.json()

    assert result['code'] == 400
    assert result['message'] == "<p>A standup is running in this channel.</p>"

def test_standup_start_valid(url):
    '''
    Function works as intended
    '''
    time.sleep(2)
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user = response.json()

    response = requests.post(f'{url}/channels/create', json={
        'token': user['token'],
        'name': "channel",
        'is_public': True
    })
    channel = response.json()

    response = requests.post(f'{url}/standup/start', json={
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'length': 2
    })

    response = requests.post(f'{url}/standup/send', json={
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': "Hi"
    })

    in_url = f"{url}/channel/messages?token={user['token']}&"
    in_url2 = f"channel_id={channel['channel_id']}&start=0"
    response = requests.get(in_url + in_url2)
    message_l = response.json()

    assert message_l['messages'] == []

    time.sleep(2.1)

    in_url = f"{url}/channel/messages?token={user['token']}&"
    in_url2 = f"channel_id={channel['channel_id']}&start=0"
    response = requests.get(in_url + in_url2)
    message_l = response.json()

    in_url = f"{url}/user/profile?token={user['token']}&u_id={user['u_id']}"
    response = requests.get(in_url)
    user = response.json()

    in_list = False
    for message in message_l['messages']:
        if message['message'] == f"{user['user']['handle_str']}: Hi":
            in_list = True
    assert in_list

# standup_active tests
def test_standup_active_invalid_token(url):
    '''
    Returns AccessError if given invalid token
    '''
    time.sleep(2.1)
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user = response.json()

    response = requests.post(f'{url}/channels/create', json={
        'token': user['token'],
        'name': "channel",
        'is_public': True
    })
    channel = response.json()

    response = requests.post(f'{url}/standup/start', json={
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'length': 2
    })

    in_url = f"{url}/standup/active?token=invalid&channel_id={channel['channel_id']}"
    response = requests.get(in_url)
    result = response.json()

    assert result['code'] == 400
    assert result['message'] == "<p>Invalid token entered</p>"

def test_standup_active_not_member(url):
    '''
    Returns AccessError if token is not a member of the channel
    '''
    time.sleep(2.1)
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user1 = response.json()

    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai36@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user2 = response.json()

    response = requests.post(f'{url}/channels/create', json={
        'token': user1['token'],
        'name': "channel",
        'is_public': True
    })
    channel = response.json()

    response = requests.post(f'{url}/standup/start', json={
        'token': user1['token'],
        'channel_id': channel['channel_id'],
        'length': 2
    })

    in_url = f"{url}/standup/active?token={user2['token']}&channel_id={channel['channel_id']}"
    response = requests.get(in_url)
    result = response.json()

    assert result['code'] == 400
    assert result['message'] == "<p>User is not a member of channel</p>"

def test_standup_active_valid_active(url):
    '''
    Function works as intended and standup is active
    '''
    time.sleep(2.1)
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user = response.json()

    response = requests.post(f'{url}/channels/create', json={
        'token': user['token'],
        'name': "channel",
        'is_public': True
    })
    channel = response.json()

    response = requests.post(f'{url}/standup/start', json={
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'length': 2
    })
    standup = response.json()

    in_url = f"{url}/standup/active?token={user['token']}&channel_id={channel['channel_id']}"
    response = requests.get(in_url)
    result = response.json()

    assert result == {
        'is_active': True,
        'time_finish': standup['time_finish']
    }
# standup_send tests
def test_standup_send_long_message(url):
    '''
    Returns InputError if given a message that is longer than 1000 characters
    '''
    time.sleep(2.1)
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user = response.json()

    response = requests.post(f'{url}/channels/create', json={
        'token': user['token'],
        'name': "channel",
        'is_public': True
    })
    channel = response.json()

    long_message = ""
    for i in range(1001):
        long_message += str(i)

    response = requests.post(f'{url}/standup/start', json={
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'length': 2
    })

    response = requests.post(f'{url}/standup/send', json={
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': long_message
    })
    result = response.json()

    assert result['code'] == 400
    assert result['message'] == "<p>The message can not be more than 1000 characters.</p>"

def test_standup_send_not_active(url):
    '''
    Returns InputError if given channel does not have an active standup
    '''
    time.sleep(2.1)
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user = response.json()

    response = requests.post(f'{url}/channels/create', json={
        'token': user['token'],
        'name': "channel",
        'is_public': True
    })
    channel = response.json()

    response = requests.post(f'{url}/standup/send', json={
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': "Hi"
    })
    result = response.json()

    assert result['code'] == 400
    assert result['message'] == "<p>This channel is not running a standup now.</p>"

def test_standup_send_valid_multiple(url):
    '''
    Function works as intended, with multiple messages
    '''
    time.sleep(2.1)
    requests.delete(f'{url}/clear')
    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user = response.json()

    response = requests.post(f'{url}/channels/create', json={
        'token': user['token'],
        'name': "channel",
        'is_public': True
    })
    channel = response.json()

    response = requests.post(f'{url}/standup/start', json={
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'length': 2
    })

    response = requests.post(f'{url}/standup/send', json={
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': "Hi"
    })

    response = requests.post(f'{url}/standup/send', json={
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': "Hello"
    })

    response = requests.post(f'{url}/standup/send', json={
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': "How are you?"
    })

    in_url = f"{url}/channel/messages?token={user['token']}&"
    in_url2 = f"channel_id={channel['channel_id']}&start=0"
    response = requests.get(in_url + in_url2)
    message_l = response.json()

    assert message_l['messages'] == []

    time.sleep(2.1)

    in_url = f"{url}/channel/messages?token={user['token']}&"
    in_url2 = f"channel_id={channel['channel_id']}&start=0"
    response = requests.get(in_url + in_url2)
    message_l = response.json()

    in_url = f"{url}/user/profile?token={user['token']}&u_id={user['u_id']}"
    response = requests.get(in_url)
    user = response.json()

    in_list = False
    for message in message_l['messages']:
        result = f"{user['user']['handle_str']}: Hi\n"
        result += f"{user['user']['handle_str']}: Hello\n"
        result += f"{user['user']['handle_str']}: How are you?"
        if message['message'] == result:
            in_list = True
    assert in_list
