'''requests is imported to obtain data from flask server'''
import requests
import pytest

@pytest.mark.usefixtures("url")
def test_url(url):
    '''
    A simple sanity test to check that your server is set up properly
    '''
    assert url.startswith("http")

# tests for channels list:
def test_channels_list_http_invalid_token(url):
    '''
    given invalid token should raise InputError
    '''
    requests.delete(f'{url}/clear')
    response = requests.get(f"{url}/channels/list?token=invalid")

    result = response.json()
    assert result['code'] == 400
    assert result['message'] == '<p>Invalid token entered</p>'

def test_channels_list_http(url):
    '''
    function used as intended
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
        'token': user1['token'],
        'name': 'channel_one',
        'is_public': True
    })
    channel1 = response.json()

    response = requests.post(f'{url}/channels/create', json={
        'token': user1['token'],
        'name': 'channel_two',
        'is_public': True
    })
    channel2 = response.json()

    response = requests.post(f'{url}/channels/create', json={
        'token': user2['token'],
        'name': 'channel_three',
        'is_public': True
    })

    response = requests.get(f"{url}/channels/list?token={user1['token']}")
    result = response.json()

    common_list = [
        {'channel_id' : channel1['channel_id'], 'name': 'channel_one'},
        {'channel_id' : channel2['channel_id'], 'name': 'channel_two'}
    ]
    assert result['channels'] == common_list

# tests for channels_listall:

def test_channels_listall_http(url):
    '''
    function used as intended
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

    response = requests.get(f"{url}/channels/listall?token={user['token']}")
    result = response.json()

    channel_l = [{'channel_id': channel['channel_id'], 'name': 'channel'}]
    assert result['channels'] == channel_l

def test_channels_listall_http_multiple(url):
    '''
    function used with multiple channels
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
        'name': 'first_chan',
        'is_public': True
    })
    channel1 = response.json()

    response = requests.post(f'{url}/channels/create', json={
        'token': user['token'],
        'name': 'second_chan',
        'is_public': True
    })
    channel2 = response.json()

    response = requests.post(f'{url}/channels/create', json={
        'token': user['token'],
        'name': 'third_chan',
        'is_public': False
    })
    channel3 = response.json()

    list_chans = [{'channel_id': channel1['channel_id'], 'name': 'first_chan'},
                  {'channel_id': channel2['channel_id'], 'name': 'second_chan'},
                  {'channel_id': channel3['channel_id'], 'name': 'third_chan'}]

    response = requests.get(f"{url}/channels/listall?token={user['token']}")
    result = response.json()
    assert result['channels'] == list_chans

def test_channels_listall_http_invalid_token(url):
    '''
    given invalid token should raise InputError
    '''
    requests.delete(f'{url}/clear')
    response = requests.get(f"{url}/channels/listall?token=invalid")

    result = response.json()
    assert result['code'] == 400
    assert result['message'] == '<p>Invalid token entered</p>'

# tests for channels create:

def test_channels_create_http_valid(url):
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

    response = requests.get(f"{url}/channels/listall?token={user['token']}")

    channel_l = response.json()

    #We want to see if list_of_channels now contains a new channel with the above specifications
    valid = False
    for chans in channel_l['channels']:
        if chans['channel_id'] == channel['channel_id']:
            valid = True
    assert valid

def test_channels_create_http_invalid_name(url):
    '''
    given an invalid name should raise InputError
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
        'name': 'invalidChannelNameTooLong',
        'is_public': False
    })

    result = response.json()
    assert result['code'] == 400
    assert result['message'] == '<p>Channel name is too long</p>'

def test_channels_create_http_invalid_token(url):
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
        'token': user['token'] + 'abc',
        'name': 'channel',
        'is_public': False
    })

    result = response.json()
    assert result['code'] == 400
    assert result['message'] == '<p>Invalid token entered</p>'

def test_channels_create_http_isowner(url):
    '''
    when function is used as intended, user should now be an owner of the
    channel
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
    channel_detail = response.json()

    is_pass = False
    for member in channel_detail['owner_members']:
        if member['u_id'] == user['u_id']:
            is_pass = True
    assert is_pass
