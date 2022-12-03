'''requests is imported to obtain data from flask server'''
import requests
import pytest

@pytest.mark.usefixtures("url")
def test_url(url):
    '''
    A simple sanity test to check that your server is set up properly
    '''
    assert url.startswith("http")

# Tests for channel functions are split into two files, to satisfy pylint
# channel_http_test1.py
# Tests for channel_invite:
def test_channel_invite_http_invalid_channel(url):
    '''
    given an invalid channel_id should raise InputError
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
        'is_public': True
    })
    channel = response.json()

    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai36@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user2 = response.json()

    response = requests.post(f'{url}/channel/invite', json={
        'token': user1['token'],
        'channel_id':  channel['channel_id'] + 100,
        'u_id': user2['u_id']
    })
    result = response.json()
    assert result['code'] == 400
    assert result['message'] == '<p>Invalid channel ID entered</p>'

def test_channel_invite_http_invalid_invitee(url):
    '''
    given an invalid u_id should raise InputError
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
        'is_public': True
    })
    channel = response.json()

    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai36@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user2 = response.json()

    response = requests.post(f'{url}/channel/invite', json={
        'token': user1['token'],
        'channel_id': channel['channel_id'],
        'u_id': user2['u_id'] + 100
    })
    result = response.json()
    assert result['code'] == 400
    assert result['message'] == '<p>Invalid user ID entered</p>'

def test_channel_invite_http_invalid_inviter(url):
    '''
    given an invalid token should raise InputError
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
        'is_public': True
    })
    channel = response.json()

    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai36@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user2 = response.json()

    response = requests.post(f'{url}/channel/invite', json={
        'token': "invalid",
        'channel_id': channel['channel_id'],
        'u_id': user2['u_id']
    })
    result = response.json()
    assert result['code'] == 400
    assert result['message'] == '<p>Invalid token entered</p>'

def test_channel_invite_http_inviter_not_member(url):
    '''
    given a token that is not a member of channel_id should raise AccessError
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
        'is_public': True
    })
    channel = response.json()

    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai36@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user2 = response.json()

    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai6@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user3 = response.json()

    response = requests.post(f'{url}/channel/invite', json={
        'token': user2['token'],
        'channel_id': channel['channel_id'],
        'u_id': user3['u_id']
    })
    result = response.json()
    assert result['code'] == 400
    assert result['message'] == '<p>User is not a member of this channel</p>'

def test_channel_invite_http_invitee_already_member(url):
    '''
    given a u_id that is already a member of channel_id should raise AccessError
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
        'is_public': True
    })
    channel = response.json()

    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai36@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user2 = response.json()

    requests.post(f'{url}/channel/join', json={
        'token': user2['token'],
        'channel_id': channel['channel_id']
    })

    response = requests.post(f'{url}/channel/invite', json={
        'token': user1['token'],
        'channel_id': channel['channel_id'],
        'u_id': user2['u_id']
    })
    result = response.json()
    assert result['code'] == 400
    assert result['message'] == '<p>User is already a member of this channel</p>'

def test_channel_invite_http_valid(url):
    '''
    function is used as intended
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
        'is_public': True
    })
    channel = response.json()

    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai36@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user2 = response.json()

    response = requests.post(f'{url}/channel/invite', json={
        'token': user1['token'],
        'channel_id': channel['channel_id'],
        'u_id': user2['u_id']
    })

    response = requests.get(f"{url}/channels/list?token={user2['token']}")
    channel_l = response.json()
    is_pass = False
    for chan in channel_l['channels']:
        if channel['channel_id'] == chan['channel_id']:
            is_pass = True
    assert is_pass

# tests for channel_details

def test_channel_details_http_invalid_channel(url):
    '''
    given an invalid channel_id should raise InputError
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

    in_url = f"{url}/channel/details?token={user['token']}&channel_id={channel['channel_id'] + 100}"
    response = requests.get(in_url)
    result = response.json()
    assert result['code'] == 400
    assert result['message'] == '<p>Invalid channel ID entered</p>'

def test_channel_details_http_invalid_token(url):
    '''
    given an invalid token should raise InputError
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

    in_url = f"{url}/channel/details?token=invalid&channel_id={channel['channel_id']}"
    response = requests.get(in_url)
    result = response.json()
    assert result['code'] == 400
    assert result['message'] == '<p>Invalid token entered</p>'

def test_channel_details_http_not_member(url):
    '''
    given a u_id that is not a member of channel_id should raise AccessError
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
        'is_public': True
    })
    channel = response.json()

    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai36@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user2 = response.json()

    in_url = f"{url}/channel/details?token={user2['token']}&channel_id={channel['channel_id']}"
    response = requests.get(in_url)
    result = response.json()
    assert result['code'] == 400
    assert result['message'] == '<p>User is not a member of this channel</p>'

def test_channel_details_http_valid(url):
    '''
    function is used as intended
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

    in_url = f"{url}/channel/details?token={user['token']}&channel_id={channel['channel_id']}"
    response = requests.get(in_url)
    result = response.json()
    assert result == {
        'name': 'channel',
        'owner_members': [{
            'u_id': user['u_id'],
            'name_first': "tom",
            'name_last': "hardy"
        }],
        'all_members': [{
            'u_id': user['u_id'],
            'name_first': "tom",
            'name_last': "hardy"
        }]
    }

# tests for channel_messages

def test_channel_messages_http_invalid_channel(url):
    '''
    given an invalid channel_id should raise InputError
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

    in_url = f"{url}/channel/messages?token={user['token']}&"
    in_url2 = f"channel_id={channel['channel_id'] + 100}&start=0"
    response = requests.get(in_url + in_url2)
    result = response.json()
    assert result['code'] == 400
    assert result['message'] == '<p>Invalid channel ID entered</p>'

def test_channel_messages_http_invalid_start(url):
    '''
    given an invalid start should raise InputError
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

    in_url = f"{url}/channel/messages?token={user['token']}&"
    in_url2 = f"channel_id={channel['channel_id']}&start=100000"
    response = requests.get(in_url + in_url2)
    result = response.json()
    error_message = '<p>Start is greater than the total number of messages in this channel</p>'
    assert result['code'] == 400
    assert result['message'] == error_message

def test_channel_messages_http_invalid_token(url):
    '''
    given an invalid token should raise InputError
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

    in_url = f"{url}/channel/messages?token=invalid&"
    in_url2 = f"channel_id={channel['channel_id']}&start=0"
    response = requests.get(in_url + in_url2)
    result = response.json()
    assert result['code'] == 400
    assert result['message'] == '<p>Invalid token entered</p>'

def test_channel_messages_http_not_member(url):
    '''
    given a token of a user that is not a member of channel_id should raise
    AccessError
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
        'is_public': True
    })
    channel = response.json()

    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai36@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user2 = response.json()

    in_url = f"{url}/channel/messages?token={user2['token']}&"
    in_url2 = f"channel_id={channel['channel_id']}&start=0"
    response = requests.get(in_url + in_url2)
    result = response.json()
    assert result['code'] == 400
    assert result['message'] == '<p>User is not a member of this channel</p>'

def test_channel_messages_http_less_50(url):
    '''
    function is used as intended and message list is below 50
    this test requires implementation of message_send function
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

    for i in range(0, 10):
        response = requests.post(f'{url}/message/send', json={
            'token': user['token'],
            'channel_id': channel['channel_id'],
            'message': str(i)
        })

    in_url = f"{url}/channel/messages?token={user['token']}&"
    in_url2 = f"channel_id={channel['channel_id']}&start=0"
    response = requests.get(in_url + in_url2)
    messages = response.json()

    assert messages['start'] == 0
    assert messages['end'] == -1

    expected_id = 10
    for message_dict in messages['messages']:
        # checks whether the messages are in the right order
        assert message_dict['message_id'] == expected_id
        expected_id -= 1

def test_channel_messages_http_more_50(url):
    '''
    function is used as intended and message list is above 50
    this test requires implementation of message_send function
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

    for i in range(0, 60):
        # sends 60 messages
        response = requests.post(f'{url}/message/send', json={
            'token': user['token'],
            'channel_id': channel['channel_id'],
            'message': str(i)
        })

    in_url = f"{url}/channel/messages?token={user['token']}&"
    in_url2 = f"channel_id={channel['channel_id']}&start=0"
    response = requests.get(in_url + in_url2)
    messages = response.json()

    assert messages['start'] == 0
    assert messages['end'] == 50

    expected_id = 60
    for message_dict in messages['messages']:
        # check whether the correct messages are on the list in the right order
        assert message_dict['message_id'] == expected_id
        expected_id -= 1

# tests for channel_addowner

def test_channel_addowner_http_invalid_channel_id(url):
    '''
    given an invalid channel_id should raise InputError
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
        'is_public': True
    })
    channel = response.json()

    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai36@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user2 = response.json()

    response = requests.post(f'{url}/channel/join', json={
        'token': user2['token'],
        'channel_id': channel['channel_id']
    })

    response = requests.post(f'{url}/channel/addowner', json={
        'token': user1['token'],
        'channel_id':  channel['channel_id'] + 100,
        'u_id': user2['u_id']
    })
    result = response.json()
    assert result['code'] == 400
    assert result['message'] == '<p>Invalid channel ID entered</p>'

def test_channel_addowner_http_invalid_u_id(url):
    '''
    given an invalid u_id should raise InputError
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
        'is_public': True
    })
    channel = response.json()

    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai36@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user2 = response.json()

    response = requests.post(f'{url}/channel/join', json={
        'token': user2['token'],
        'channel_id': channel['channel_id']
    })

    response = requests.post(f'{url}/channel/addowner', json={
        'token': user1['token'],
        'channel_id':  channel['channel_id'],
        'u_id': user2['u_id'] + 100
    })
    result = response.json()
    assert result['code'] == 400
    assert result['message'] == '<p>Invalid user ID entered</p>'

def test_channel_addowner_http_u_id_notmember(url):
    '''
    given a u_id that is not a member of channel_id should raise InputError
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
        'is_public': True
    })
    channel = response.json()

    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai36@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user2 = response.json()

    response = requests.post(f'{url}/channel/addowner', json={
        'token': user1['token'],
        'channel_id':  channel['channel_id'],
        'u_id': user2['u_id']
    })
    result = response.json()
    assert result['code'] == 400
    assert result['message'] == '<p>User is not a member of this channel</p>'

def test_channel_addowner_http_user_already_owner_of_channel(url):
    '''
    given a u_id who is already an owner of channel_id should raise InputError
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

    response = requests.post(f'{url}/channel/addowner', json={
        'token': user['token'],
        'channel_id':  channel['channel_id'],
        'u_id': user['u_id']
    })
    result = response.json()
    assert result['code'] == 400
    assert result['message'] == '<p>User is already an owner of this channel</p>'

def test_channel_addowner_http_unauthorized_user(url):
    '''
    given an invalid token should raise InputError
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
        'is_public': True
    })
    channel = response.json()

    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai36@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user2 = response.json()

    response = requests.post(f'{url}/channel/join', json={
        'token': user2['token'],
        'channel_id': channel['channel_id']
    })

    response = requests.post(f'{url}/channel/addowner', json={
        'token': 'invalid',
        'channel_id':  channel['channel_id'],
        'u_id': user2['u_id']
    })
    result = response.json()
    assert result['code'] == 400
    assert result['message'] == '<p>Invalid token entered</p>'

def test_channel_addowner_http_token_notowner(url):
    '''
    given a token that does not have owner permissions, raised AccessError
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
        'is_public': True
    })
    channel = response.json()

    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai36@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user2 = response.json()

    response = requests.post(f'{url}/channel/join', json={
        'token': user2['token'],
        'channel_id': channel['channel_id']
    })

    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai6@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user3 = response.json()

    response = requests.post(f'{url}/channel/join', json={
        'token': user3['token'],
        'channel_id': channel['channel_id']
    })

    response = requests.post(f'{url}/channel/addowner', json={
        'token': user2['u_id'],
        'channel_id':  channel['channel_id'],
        'u_id': user3['u_id']
    })
    result = response.json()
    assert result['code'] == 400
    assert result['message'] == '<p>Invalid token entered</p>'

def test_channel_addowner_http_token_global_owner(url):
    '''
    given a token that is an owner of flockr but not local owner, should work
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

    response = requests.post(f'{url}/channels/create', json={
        'token': user2['token'],
        'name': 'channel',
        'is_public': True
    })
    channel = response.json()

    response = requests.post(f'{url}/channel/removeowner', json={
        'token': user2['token'],
        'channel_id':  channel['channel_id'],
        'u_id': user2['u_id']
    })

    response = requests.post(f'{url}/channel/addowner', json={
        'token': user1['token'],
        'channel_id':  channel['channel_id'],
        'u_id': user2['u_id']
    })

    in_url = f"{url}/channel/details?token={user2['token']}&channel_id={channel['channel_id']}"
    response = requests.get(in_url)
    channel_detail = response.json()

    is_pass = False
    for member in channel_detail['owner_members']:
        if member['u_id'] == user2['u_id']:
            is_pass = True
    assert is_pass

def test_channel_addowner_http_allvalid(url):
    '''
    function is used as intended
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
        'is_public': True
    })
    channel = response.json()

    response = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai36@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user2 = response.json()

    response = requests.post(f'{url}/channel/join', json={
        'token': user2['token'],
        'channel_id': channel['channel_id']
    })

    response = requests.post(f'{url}/channel/addowner', json={
        'token': user1['token'],
        'channel_id':  channel['channel_id'],
        'u_id': user2['u_id']
    })

    in_url = f"{url}/channel/details?token={user1['token']}&channel_id={channel['channel_id']}"
    response = requests.get(in_url)
    channel_detail = response.json()

    is_pass = False
    for member in channel_detail['owner_members']:
        if member['u_id'] == user2['u_id']:
            is_pass = True
    assert is_pass
