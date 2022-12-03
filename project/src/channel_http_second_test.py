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
# channel_http_test2.py
# tests for channel_removeowner

def test_channel_removeowner_http_invalid_channel_id(url):
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

    response = requests.post(f'{url}/channel/removeowner', json={
        'token': user['token'],
        'channel_id':  channel['channel_id'] + 100,
        'u_id': user['u_id']
    })
    result = response.json()
    assert result['code'] == 400
    assert result['message'] == '<p>Invalid channel ID entered</p>'

def test_channel_removeowner_http_invalid_u_id(url):
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
    user = response.json()

    response = requests.post(f'{url}/channels/create', json={
        'token': user['token'],
        'name': 'channel',
        'is_public': True
    })
    channel = response.json()

    response = requests.post(f'{url}/channel/removeowner', json={
        'token': user['token'],
        'channel_id':  channel['channel_id'],
        'u_id': user['u_id'] + 100
    })
    result = response.json()
    assert result['code'] == 400
    assert result['message'] == '<p>Invalid user ID entered</p>'

def test_channel_removeowner_http_user_not_owner_of_channel(url):
    '''
    given a u_id that is not an owner of channel_id should raise InputError
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

    response = requests.post(f'{url}/channel/removeowner', json={
        'token': user1['token'],
        'channel_id':  channel['channel_id'],
        'u_id': user2['u_id']
    })
    result = response.json()
    assert result['code'] == 400
    assert result['message'] == '<p>User is not an owner of this channel</p>'

def test_channel_removeowner_http_unauthorized_user(url):
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
        'token': user1['token'],
        'channel_id':  channel['channel_id'],
        'u_id': user2['u_id']
    })

    response = requests.post(f'{url}/channel/removeowner', json={
        'token': 'invalid',
        'channel_id':  channel['channel_id'],
        'u_id': user2['u_id']
    })
    result = response.json()
    assert result['code'] == 400
    assert result['message'] == '<p>Invalid token entered</p>'

def test_channel_removeowner_http_token_notowner(url):
    '''
    given a token that is not an owner of channel_id should raise AccessError
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
        'token': user1['token'],
        'channel_id':  channel['channel_id'],
        'u_id': user3['u_id']
    })

    response = requests.post(f'{url}/channel/removeowner', json={
        'token': user2['token'],
        'channel_id':  channel['channel_id'],
        'u_id': user3['u_id']
    })
    result = response.json()
    assert result['code'] == 400
    assert result['message'] == '<p>Given token is not an owner of the channel</p>'

def test_channel_removeowner_http_global_owner(url):
    '''
    given a token that is an owner of flockr, should work
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
        'token': user1['token'],
        'channel_id':  channel['channel_id'],
        'u_id': user2['u_id']
    })

    in_url = f"{url}/channel/details?token={user2['token']}&channel_id={channel['channel_id']}"
    response = requests.get(in_url)
    channel_detail = response.json()

    is_pass = True
    for member in channel_detail['owner_members']:
        if member['u_id'] == user2['u_id']:
            is_pass = False
    assert is_pass

def test_channel_removeowner_http_allvalid(url):
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

    response = requests.post(f'{url}/channel/removeowner', json={
        'token': user['token'],
        'channel_id':  channel['channel_id'],
        'u_id': user['u_id']
    })

    in_url = f"{url}/channel/details?token={user['token']}&channel_id={channel['channel_id']}"
    response = requests.get(in_url)
    channel_detail = response.json()

    is_pass = True
    for member in channel_detail['owner_members']:
        if member['u_id'] == user['u_id']:
            is_pass = False
    assert is_pass

# Tests for channel_join:

def test_channel_join_http_invalid_channel(url):
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
        'channel_id':  channel['channel_id'] + 100
    })
    result = response.json()
    assert result['code'] == 400
    assert result['message'] == '<p>Invalid channel ID entered</p>'

def test_channel_join_http_invalid_token(url):
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

    response = requests.post(f'{url}/channel/join', json={
        'token': "invalid",
        'channel_id':  channel['channel_id']
    })
    result = response.json()
    assert result['code'] == 400
    assert result['message'] == '<p>Invalid token entered</p>'

def test_channel_join_http_already_member(url):
    '''
    given a token that is already a member of channel_id should raise AccessError
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

    response = requests.post(f'{url}/channel/join', json={
        'token': user['token'],
        'channel_id': channel['channel_id']
    })
    result = response.json()
    assert result['code'] == 400
    assert result['message'] == '<p>User is already a member of this channel</p>'

def test_channel_join_http_private_channel(url):
    '''
    given a channel_id with is_public set to False should raise AccessError
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

    response = requests.post(f'{url}/channel/join', json={
        'token': user2['token'],
        'channel_id':  channel['channel_id']
    })
    result = response.json()
    assert result['code'] == 400
    assert result['message'] == '<p>Channel is not public</p>'

def test_channel_join_http_private_channel_owner(url):
    '''
    given a u_id who is a global owner, function should allow them to join
    private channels
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
        'is_public': False
    })
    channel = response.json()

    response = requests.post(f'{url}/channel/join', json={
        'token': user1['token'],
        'channel_id':  channel['channel_id']
    })

    response = requests.get(f"{url}/channels/list?token={user1['token']}")
    user_channels = response.json()

    is_pass = False
    for chan in user_channels['channels']:
        if chan['channel_id'] == channel['channel_id']:
            is_pass = True
    assert is_pass

def test_channel_join_http_function(url):
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
        'channel_id':  channel['channel_id']
    })

    response = requests.get(f"{url}/channels/list?token={user2['token']}")
    user_channels = response.json()

    is_pass = False
    for chan in user_channels['channels']:
        if chan['channel_id'] == channel['channel_id']:
            is_pass = True
    assert is_pass

# Tests for channel_leave:

def test_channel_leave_http_invalid_channel(url):
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

    response = requests.post(f'{url}/channel/leave', json={
        'token': user['token'],
        'channel_id':  channel['channel_id'] + 100
    })
    result = response.json()
    assert result['code'] == 400
    assert result['message'] == '<p>Invalid channel ID entered</p>'

def test_channel_leave_http_invalid_token(url):
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

    response = requests.post(f'{url}/channel/leave', json={
        'token': "invalid",
        'channel_id':  channel['channel_id']
    })
    result = response.json()
    assert result['code'] == 400
    assert result['message'] == '<p>Invalid token entered</p>'

def test_channel_leave_http_not_member(url):
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

    response = requests.post(f'{url}/channel/leave', json={
        'token': user2['token'],
        'channel_id':  channel['channel_id']
    })
    result = response.json()
    assert result['code'] == 400
    assert result['message'] == '<p>User is not a member of this channel</p>'

def test_channel_leave_http_function(url):
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

    response = requests.post(f'{url}/channel/leave', json={
        'token': user['token'],
        'channel_id':  channel['channel_id']
    })

    response = requests.get(f"{url}/channels/list?token={user['token']}")
    channel_list = response.json()

    assert channel_list == {'channels': []}

def test_channel_leave_http_multiple(url):
    '''
    function is used with multiple users in channel
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

    response = requests.post(f'{url}/channel/leave', json={
        'token': user3['token'],
        'channel_id':  channel['channel_id']
    })

    response = requests.get(f"{url}/channels/list?token={user1['token']}")
    channel_list1 = response.json()

    response = requests.get(f"{url}/channels/list?token={user2['token']}")
    channel_list2 = response.json()

    response = requests.get(f"{url}/channels/list?token={user3['token']}")
    channel_list3 = response.json()

    assert channel_list3 == {
        'channels': []
    }
    assert channel_list2 == {
        'channels': [{
            'channel_id' : channel['channel_id'],
            'name' : 'channel'
        }]
    }
    assert channel_list1 == {
        'channels': [{
            'channel_id' : channel['channel_id'],
            'name' : 'channel'
        }]
    }
def test_channel_leave_http_owner(url):
    '''
    given a u_id that is an owner of channel_id, owner rights are stripped as
    well
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
        'channel_id':  channel['channel_id']
    })

    response = requests.post(f'{url}/channel/addowner', json={
        'token': user1['token'],
        'channel_id':  channel['channel_id'],
        'u_id': user2['u_id']
    })

    response = requests.post(f'{url}/channel/leave', json={
        'token': user2['token'],
        'channel_id':  channel['channel_id']
    })

    in_url = f"{url}/channel/details?token={user1['token']}&channel_id={channel['channel_id']}"
    response = requests.get(in_url)
    channel_d = response.json()
    assert channel_d['owner_members'] == [{
        'u_id': user1['u_id'],
        'name_first': 'tom',
        'name_last': 'hardy'
    }]
