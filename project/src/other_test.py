'''
time is used for delay with sleep()
'''
import time
import pytest
from auth import auth_register
from channels import channels_create
from channel import channel_join, channel_messages
from error import InputError, AccessError
from other import admin_userpermission_change, users_all, clear, search
from other import standup_start, standup_active, standup_send
from message import message_send
from user import user_profile

# Tests for admin_userpermission_change:
def test_admin_userpermission_change_invalid_uid():
    '''
    given an invalid u_id, raise InputError
    '''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    user2 = auth_register("ankitrai36@gmail.com", "12345678", "tom", "hardy")
    with pytest.raises(InputError):
        assert admin_userpermission_change(user1['token'], user2['u_id'] + 100, 1)

def test_admin_userpermission_change_invalid_token():
    '''
    given an invalid token, raise InputError
    '''
    clear()
    auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    user2 = auth_register("ankitrai36@gmail.com", "12345678", "tom", "hardy")
    with pytest.raises(AccessError):
        assert admin_userpermission_change("invalid", user2['u_id'], 1)

def test_admin_userpermission_change_invalid_permission_id():
    '''
    given an invalid permission_id, raise InputError
    '''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    user2 = auth_register("ankitrai36@gmail.com", "12345678", "tom", "hardy")
    with pytest.raises(InputError):
        assert admin_userpermission_change(user1['token'], user2['u_id'], 100)

def test_admin_userpermission_change_not_admin():
    '''
    given a token that is not a global member, raise AccessError
    '''
    clear()
    auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    user2 = auth_register("ankitrai36@gmail.com", "12345678", "tom", "hardy")
    with pytest.raises(AccessError):
        assert admin_userpermission_change(user2['token'], user2['u_id'], 1)

def test_admin_userpermission_change_already_admin():
    '''
    given a u_id that is already a global member, raise InputError
    '''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    user2 = auth_register("ankitrai36@gmail.com", "12345678", "tom", "hardy")
    admin_userpermission_change(user1['token'], user2['u_id'], 1)
    with pytest.raises(InputError):
        assert admin_userpermission_change(user1['token'], user2['u_id'], 1)

def test_admin_userpermission_change_already_member():
    '''
    given a u_id that is already a member, raise InputError
    '''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    user2 = auth_register("ankitrai36@gmail.com", "12345678", "tom", "hardy")
    with pytest.raises(InputError):
        assert admin_userpermission_change(user1['token'], user2['u_id'], 2)

def test_admin_userpermission_change_valid():
    '''
    when function works as intended, new owner should be able to join a
    private channel with no errors
    '''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user1['token'], 'channel', False)
    user2 = auth_register("ankitrai36@gmail.com", "12345678", "tom", "hardy")
    admin_userpermission_change(user1['token'], user2['u_id'], 1)
    assert channel_join(user2['token'], channel['channel_id']) == {}

# Tests for users_all:
def test_users_all_invalid_token():
    '''
    test to check that given token is valid
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    invalid_token = user['token'] + 'abc'
    with pytest.raises(InputError):
        assert users_all(invalid_token)
def test_users_all_valid():
    '''
    test to check that user with valid token returns correct information
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    users_l = [
        {
            'u_id': user['u_id'],
            'email': 'ankitrai326@gmail.com',
            'name_first': 'tom',
            'name_last': 'hardy',
            'handle_str': 'tomhardy'
        }
    ]
    assert users_all(user['token'])['users'] == users_l
def test_users_all_multiple():
    '''
    test to check that multiple users with valid tokens return correct
    information
    '''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    user2 = auth_register("ankitrai26@gmail.com", "12345678", "christian", "bale")
    user3 = auth_register("ankitrai36@gmail.com", "12345678", "annie", "leonhart")
    users_l = [
        {
            'u_id': user1['u_id'],
            'email': 'ankitrai326@gmail.com',
            'name_first': 'tom',
            'name_last': 'hardy',
            'handle_str': 'tomhardy'
        },
        {
            'u_id': user2['u_id'],
            'email': 'ankitrai26@gmail.com',
            'name_first': 'christian',
            'name_last': 'bale',
            'handle_str': 'christianbale'
        },
        {
            'u_id': user3['u_id'],
            'email': 'ankitrai36@gmail.com',
            'name_first': 'annie',
            'name_last': 'leonhart',
            'handle_str': 'annieleonhart'
        }
    ]
    assert users_all(user1['token'])['users'] == users_l

# Tests for search
def test_search_single():
    '''
    Sends a sample messages, then calls search
    Function works as intended
    '''
    clear()
    user = auth_register("examplenoodle@gmail.com", "easypass", "Michelle", "Seeto")
    channel_id1 = channels_create(user['token'], 'channel_one', True)
    message_send(user['token'], channel_id1['channel_id'], "Testing")
    matched_message = search(user['token'], "Testing")

    assert matched_message['messages'][0]['message'] == "Testing"

def test_search_multiple():
    '''
    Function works as intended, several messages sent
    '''
    clear()
    user = auth_register("examplenoodle@gmail.com", "easypass", "Michelle", "Seeto")
    channel_id1 = channels_create(user['token'], 'channel_one', True)
    message_send(user['token'], channel_id1['channel_id'], "Testing")
    message_send(user['token'], channel_id1['channel_id'], "Testing")
    messages = channel_messages(user['token'], channel_id1['channel_id'], 0)
    message_send(user['token'], channel_id1['channel_id'], "Not to be returned")

    matched_list = search(user['token'], "Testing")
    assert matched_list['messages'] == messages['messages']

def test_search_multiple_channels():
    '''
    Function works as intended, several messages sent across several
    channels
    '''
    clear()
    user = auth_register("examplenoodle@gmail.com", "easypass", "Michelle", "Seeto")
    correct_list = []
    for i in range(1, 4):
        channel = channels_create(user['token'], str(i), True)
        message_send(user['token'], channel['channel_id'], "Testing")
        messages = channel_messages(user['token'], channel['channel_id'], 0)
        message_send(user['token'], channel['channel_id'], "Not to be returned")
        correct_list += messages['messages']

    matched_list = search(user['token'], "Testing")
    assert matched_list['messages'] == correct_list

# Tests for standup_start
def test_standup_start_invalid_channel_id():
    '''
    Returns InputError if given an invalid channel_id
    '''
    clear()
    user = auth_register("examplenoodle@gmail.com", "easypass", "Michelle", "Seeto")
    channels_create(user['token'], "channel", True)
    with pytest.raises(InputError):
        assert standup_start(user['token'], 123123, 5)

def test_standup_start_invalid_token():
    '''
    Returns AccessError if given invalid token
    '''
    clear()
    user = auth_register("examplenoodle@gmail.com", "easypass", "Michelle", "Seeto")
    channel = channels_create(user['token'], "channel", True)
    with pytest.raises(AccessError):
        standup_start('invalid', channel['channel_id'], 5)

def test_standup_start_not_member():
    '''
    Returns AccessError if token is not a member of the channel
    '''
    clear()
    user1 = auth_register("examplenoodle@gmail.com", "easypass", "Michelle", "Seeto")
    user2 = auth_register("examplenoodle2@gmail.com", "easypass", "Michelle", "Seeto")
    channel = channels_create(user1['token'], "channel", True)
    with pytest.raises(AccessError):
        standup_start(user2['token'], channel['channel_id'], 5)

def test_standup_start_invalid_length():
    '''
    Returns InputError if given a length that does not correspond to the unit seconds
    '''
    clear()
    user = auth_register("examplenoodle@gmail.com", "easypass", "Michelle", "Seeto")
    channel = channels_create(user['token'], "channel", True)
    with pytest.raises(InputError):
        standup_start(user['token'], channel['channel_id'], -1)

def test_standup_start_already_active():
    '''
    Returns InputError if a standup is already active in given channel
    '''
    clear()
    user = auth_register("examplenoodle@gmail.com", "easypass", "Michelle", "Seeto")
    channel = channels_create(user['token'], "channel", True)
    standup_start(user['token'], channel['channel_id'], 2)
    with pytest.raises(InputError):
        standup_start(user['token'], channel['channel_id'], 2)

def test_standup_start_valid():
    '''
    Function works as intended
    '''
    time.sleep(2.1)
    clear()
    user = auth_register("examplenoodle@gmail.com", "easypass", "Michelle", "Seeto")
    channel = channels_create(user['token'], "channel", True)
    standup_start(user['token'], channel['channel_id'], 2)
    standup_send(user['token'], channel['channel_id'], "Hi")

    message_l = channel_messages(user['token'], channel['channel_id'], 0)
    assert message_l['messages'] == []

    time.sleep(2.1)
    message_l = channel_messages(user['token'], channel['channel_id'], 0)
    user = user_profile(user['token'], user['u_id'])
    in_list = False
    for message in message_l['messages']:
        if message['message'] == f"{user['user']['handle_str']}: Hi":
            in_list = True
    assert in_list

# Tests for standup_active
def test_standup_active_invalid_token():
    '''
    Returns AccessError if given invalid token
    '''
    time.sleep(2.1)
    clear()
    user = auth_register("examplenoodle@gmail.com", "easypass", "Michelle", "Seeto")
    channel = channels_create(user['token'], "channel", True)
    standup_start(user['token'], channel['channel_id'], 2)
    with pytest.raises(AccessError):
        standup_active('invalid', channel['channel_id'])

def test_standup_active_invalid_channel_id():
    '''
    Returns InputError if given invalid channel_id
    '''
    time.sleep(2.1)
    clear()
    user = auth_register("examplenoodle@gmail.com", "easypass", "Michelle", "Seeto")
    channel = channels_create(user['token'], "channel", True)
    standup_start(user['token'], channel['channel_id'], 2)
    with pytest.raises(InputError):
        standup_active(user['token'], 123123)

def test_standup_active_not_member():
    '''
    Returns AccessError if token is not a member of the channel
    '''
    time.sleep(2.1)
    clear()
    user1 = auth_register("examplenoodle@gmail.com", "easypass", "Michelle", "Seeto")
    user2 = auth_register("examplenoodle1@gmail.com", "easypass", "Michelle", "Seeto")
    channel = channels_create(user1['token'], "channel", True)
    standup_start(user1['token'], channel['channel_id'], 2)
    with pytest.raises(AccessError):
        standup_active(user2['token'], channel['channel_id'])

def test_standup_active_valid_not_active():
    '''
    Function works as intended and standup is not active
    '''
    time.sleep(2.1)
    clear()
    user = auth_register("examplenoodle@gmail.com", "easypass", "Michelle", "Seeto")
    channel = channels_create(user['token'], "channel", True)
    result = standup_active(user['token'], channel['channel_id'])
    assert result == {
        'is_active': False,
        'time_finish': None
    }

def test_standup_active_valid_active():
    '''
    Function works as intended and standup is active
    '''
    time.sleep(2.1)
    clear()
    user = auth_register("examplenoodle@gmail.com", "easypass", "Michelle", "Seeto")
    channel = channels_create(user['token'], "channel", True)
    standup = standup_start(user['token'], channel['channel_id'], 2)
    result = standup_active(user['token'], channel['channel_id'])
    assert result == {
        'is_active': True,
        'time_finish': standup['time_finish']
    }

# Tests for standup_send
def test_standup_send_invalid_channel_id():
    '''
    Returns InputError if given invalid channel_id
    '''
    time.sleep(2.1)
    clear()
    user = auth_register("examplenoodle@gmail.com", "easypass", "Michelle", "Seeto")
    channel = channels_create(user['token'], "channel", True)
    standup_start(user['token'], channel['channel_id'], 2)
    with pytest.raises(InputError):
        standup_send(user['token'], 123123, "Hi")

def test_standup_send_invalid_token():
    '''
    Returns AccessError if given invalid token
    '''
    time.sleep(2.1)
    clear()
    user = auth_register("examplenoodle@gmail.com", "easypass", "Michelle", "Seeto")
    channel = channels_create(user['token'], "channel", True)
    standup_start(user['token'], channel['channel_id'], 2)
    with pytest.raises(AccessError):
        standup_send("invalid", channel['channel_id'], "Hi")

def test_standup_send_long_message():
    '''
    Returns InputError if given a message that is longer than 1000 characters
    '''
    time.sleep(2.1)
    clear()
    user = auth_register("examplenoodle@gmail.com", "easypass", "Michelle", "Seeto")
    channel = channels_create(user['token'], "channel", True)
    long_message = ""
    for i in range(1001):
        long_message += str(i)
    standup_start(user['token'], channel['channel_id'], 2)
    with pytest.raises(InputError):
        standup_send(user['token'], channel['channel_id'], long_message)

def test_standup_send_not_active():
    '''
    Returns InputError if given channel does not have an active standup
    '''
    time.sleep(2.1)
    clear()
    user = auth_register("examplenoodle@gmail.com", "easypass", "Michelle", "Seeto")
    channel = channels_create(user['token'], "channel", True)
    with pytest.raises(InputError):
        standup_send(user['token'], channel['channel_id'], "Hi")

def test_standup_send_not_member():
    '''
    Returns AccessError if token is not a member of channel
    '''
    time.sleep(2.1)
    clear()
    user1 = auth_register("examplenoodle@gmail.com", "easypass", "Michelle", "Seeto")
    user2 = auth_register("examplenoodle1@gmail.com", "easypass", "Michelle", "Seeto")
    channel = channels_create(user1['token'], "channel", True)
    standup_start(user1['token'], channel['channel_id'], 2)
    with pytest.raises(AccessError):
        standup_send(user2['token'], channel['channel_id'], "Hi")

def test_standup_send_valid_multiple():
    '''
    Function works as intended, with multiple messages
    '''
    time.sleep(2.1)
    clear()
    user = auth_register("examplenoodle@gmail.com", "easypass", "Michelle", "Seeto")
    channel = channels_create(user['token'], "channel", True)
    standup_start(user['token'], channel['channel_id'], 2)
    standup_send(user['token'], channel['channel_id'], "Hi")
    standup_send(user['token'], channel['channel_id'], "Hello")
    standup_send(user['token'], channel['channel_id'], "How are you?")

    message_l = channel_messages(user['token'], channel['channel_id'], 0)
    assert message_l['messages'] == []

    time.sleep(2.1)
    message_l = channel_messages(user['token'], channel['channel_id'], 0)
    user = user_profile(user['token'], user['u_id'])
    in_list = False
    for message in message_l['messages']:
        result = f"{user['user']['handle_str']}: Hi\n"
        result += f"{user['user']['handle_str']}: Hello\n"
        result += f"{user['user']['handle_str']}: How are you?"
        if message['message'] == result:
            in_list = True
    assert in_list

def test_standup_send_valid_multiple_users():
    '''
    Function works as intended, with multiple users
    '''
    time.sleep(2.1)
    clear()
    user1 = auth_register("examplenoodle@gmail.com", "easypass", "Michelle", "Seeto")
    channel = channels_create(user1['token'], "channel", True)
    user2 = auth_register("examplenoodle1@gmail.com", "easypass", "Tom", "Hardy")
    channel_join(user2['token'], channel['channel_id'])
    user3 = auth_register("examplenoodle2@gmail.com", "easypass", "Hi", "Man")
    channel_join(user3['token'], channel['channel_id'])

    standup_start(user1['token'], channel['channel_id'], 2)
    standup_send(user1['token'], channel['channel_id'], "Hi")
    standup_send(user2['token'], channel['channel_id'], "Hello")
    standup_send(user3['token'], channel['channel_id'], "How are you?")

    message_l = channel_messages(user1['token'], channel['channel_id'], 0)
    assert message_l['messages'] == []

    time.sleep(2.1)
    message_l = channel_messages(user1['token'], channel['channel_id'], 0)
    user1 = user_profile(user1['token'], user1['u_id'])
    user2 = user_profile(user2['token'], user2['u_id'])
    user3 = user_profile(user3['token'], user3['u_id'])
    in_list = False
    for message in message_l['messages']:
        result = f"{user1['user']['handle_str']}: Hi\n"
        result += f"{user2['user']['handle_str']}: Hello\n"
        result += f"{user3['user']['handle_str']}: How are you?"
        if message['message'] == result:
            in_list = True
    assert in_list
