'''pytest is imported to check for errors and to run the tests'''
import pytest
from auth import auth_register
from channel import channel_details
from channels import channels_create, channels_list, channels_listall
from error import InputError, AccessError
from other import clear



# tests for channels_list

def test_channels_list_invalid_token():
    '''
    given invalid token should raise AccessError
    '''
    clear()
    with pytest.raises(AccessError):
        assert channels_list("invalid_token")

def test_channels_list():
    '''
    function used as intended
    '''
    clear()
    user1 = auth_register("examplemail@gmail.com", "password1234", "bruce", "lee")
    user2 = auth_register("example2mail@gmail.com", "pa55word", 'bugs', 'bunny')
    channel_id1 = channels_create(user1['token'], 'channel_one', True)
    channel_id2 = channels_create(user1['token'], 'channel_two', True)
    channels_create(user2['token'], 'channel_three', True)

    user_channels = channels_list(user1["token"])
    common_list = [
        {'channel_id' : channel_id1['channel_id'], 'name': 'channel_one'},
        {'channel_id' : channel_id2['channel_id'], 'name': 'channel_two'}
    ]

    assert user_channels['channels'] == common_list

# tests for channels_listall

def test_channels_listall():
    '''
    function used as intended
    '''
    clear()
    user = auth_register("noodles@gmail.com", "easy_password", "Jackie", "Chan")
    channel_id = channels_create(user["token"], "first_chan", True)
    all_chans = channels_listall(user["token"])
    channel = [{'channel_id': channel_id['channel_id'], 'name': 'first_chan'}]
    assert all_chans['channels'] == channel

def test_channels_listall_multiple():
    '''
    function used with multiple channels
    '''
    clear()
    user1 = auth_register("definitelyarealemail@yahoo.com", "notguessable", "Mickey", "Mouse")
    channel_id = channels_create(user1["token"], "first_chan", True)
    channel_id2 = channels_create(user1["token"], "second_chan", True)
    channel_id3 = channels_create(user1["token"], "third_chan", False)
    list_chans = [{'channel_id': channel_id['channel_id'], 'name': 'first_chan'},
                  {'channel_id': channel_id2['channel_id'], 'name': 'second_chan'},
                  {'channel_id': channel_id3['channel_id'], 'name': 'third_chan'}]
    all_channels = channels_listall(user1["token"])
    assert all_channels['channels'] == list_chans

def test_channels_listall_invalid_token():
    '''
    given invalid token should raise AccessError
    '''
    clear()
    with pytest.raises(AccessError):
        assert channels_listall("invalid_token")

# tests for channels_create

def test_channels_create_valid():
    '''
    function is used as intended
    '''
    clear()
    user = auth_register("nessylee@gmail.com", "password", "nelson", "lee")
    value = channels_create(user["token"], "first_chan", True)
    list_of_channels = channels_listall(user["token"])
    #We want to see if list_of_channels now contains a new channel with the above specifications
    valid = False
    for chans in list_of_channels['channels']:
        if chans['channel_id'] == value['channel_id']:
            valid = True

    assert valid

def test_channels_create_invalid_name():
    '''
    given an invalid name should raise InputError
    '''
    clear()
    user = auth_register("nelsonylee@gmail.com", "password", "nelson", "lee")
    with pytest.raises(InputError):
        assert channels_create(user["token"], "invalidChannelNameTooLong", False)

def test_channels_create_invalid_token():
    '''
    given an invalid token should raise AccessError
    '''
    clear()
    user = auth_register("nelsonylee@gmail.com", "password", "nelson", "lee")
    invalid_token = user['token'] + 'abc'
    with pytest.raises(AccessError):
        assert channels_create(invalid_token, "Channel", False)

def test_channels_create_isowner():
    '''
    when function is used as intended, user should now be an owner of the
    channel
    '''
    clear()
    user = auth_register("nelsonylee@gmail.com", "password", "nelson", "lee")
    channel = channels_create(user['token'], "Channel", True)
    channel_detail = channel_details(user['token'], channel['channel_id'])

    is_pass = False
    for member in channel_detail['owner_members']:
        if member['u_id'] == user['u_id']:
            is_pass = True
    assert is_pass
