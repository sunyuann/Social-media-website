'''pytest is imported to check for errors and to run the tests'''
import pytest
from auth import auth_register
from channels import channels_create, channels_list
from channel import channel_join, channel_leave, channel_details
from channel import channel_addowner, channel_removeowner, channel_invite, channel_messages
from message import message_send
from error import InputError, AccessError
from other import clear

# tests for channel_invite

def test_channel_invite_invalid_channel():
    '''
    given an invalid channel_id should raise InputError
    '''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channels_create(user1['token'], 'channel', True)
    user2 = auth_register("ankitrai36@gmail.com", "12345678", "tom", "hardy")
    with pytest.raises(InputError):
        assert channel_invite(user1['token'], 7898789, user2['u_id'])

def test_channel_invite_invalid_invitee():
    '''
    given an invalid u_id should raise InputError
    '''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user1['token'], 'channel', True)
    auth_register("ankitrai36@gmail.com", "12345678", "tom", "hardy")
    with pytest.raises(InputError):
        assert channel_invite(user1['token'], channel['channel_id'], 213123)

def test_channel_invite_invalid_inviter():
    '''
    given an invalid token should raise AccessError
    '''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user1['token'], 'channel', True)
    user2 = auth_register("ankitrai36@gmail.com", "12345678", "tom", "hardy")
    with pytest.raises(AccessError):
        assert channel_invite("invalid", channel['channel_id'], user2['u_id'])

def test_channel_invite_inviter_not_member():
    '''
    given a token that is not a member of channel_id should raise AccessError
    '''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user1['token'], 'channel', True)
    user2 = auth_register("ankitrai3@gmail.com", "12345678", "tom", "hardy")
    user3 = auth_register("ankitrai36@gmail.com", "12345678", "tom", "hardy")
    with pytest.raises(AccessError):
        assert channel_invite(user2['token'], channel['channel_id'], user3['u_id'])

def test_channel_invite_invitee_already_member():
    '''
    given a u_id that is already a member of channel_id should raise AccessError
    '''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user1['token'], 'channel', True)
    user2 = auth_register("ankitrai3@gmail.com", "12345678", "tom", "hardy")
    channel_join(user2['token'], channel['channel_id'])
    with pytest.raises(AccessError):
        assert channel_invite(user1['token'], channel['channel_id'], user2['u_id'])

def test_channel_invite_valid():
    '''
    function is used as intended
    '''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user1['token'], 'channel', True)
    user2 = auth_register("ankitrai36@gmail.com", "12345678", "tom", "hardy")
    channel_invite(user1['token'], channel['channel_id'], user2['u_id'])
    channel_l = channels_list(user2['token'])
    is_pass = False
    for chan in channel_l['channels']:
        if channel['channel_id'] == chan['channel_id']:
            is_pass = True
    assert is_pass

def test_channel_invite_private():
    '''
    u_id invited to a private channel should be allowed
    '''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user1['token'], 'channel', False)
    user2 = auth_register("ankitrai36@gmail.com", "12345678", "tom", "hardy")
    channel_invite(user1['token'], channel['channel_id'], user2['u_id'])
    channel_l = channels_list(user2['token'])
    is_pass = False
    for chan in channel_l['channels']:
        if channel['channel_id'] == chan['channel_id']:
            is_pass = True
    assert is_pass

# tests for channel_details

def test_channel_details_invalid_channel():
    '''
    given an invalid channel_id should raise InputError
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channels_create(user['token'], 'channel', True)
    with pytest.raises(InputError):
        assert channel_details(user['token'], 7898789)

def test_channel_details_invalid_token():
    '''
    given an invalid token should raise AccessError
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user['token'], 'channel', True)
    with pytest.raises(AccessError):
        assert channel_details('invalid', channel['channel_id'])

def test_channel_details_not_member():
    '''
    given a u_id that is not a member of channel_id should raise AccessError
    '''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user1['token'], 'channel', True)
    user2 = auth_register("ankitrai26@gmail.com", "12345678", "tom", "hardy")
    with pytest.raises(AccessError):
        assert channel_details(user2['token'], channel['channel_id'])

def test_channel_details_valid():
    '''
    function is used as intended
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user['token'], 'channel', True)
    detail = channel_details(user['token'], channel['channel_id'])
    assert detail == {
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

def test_channel_messages_invalid_channel():
    '''
    given an invalid channel_id should raise InputError
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channels_create(user['token'], 'channel', True)
    with pytest.raises(InputError):
        assert channel_messages(user['token'], 7898789, 0)

def test_channel_messages_invalid_start():
    '''
    given an invalid start should raise InputError
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user['token'], 'channel', True)
    with pytest.raises(InputError):
        assert channel_messages(user['token'], channel['channel_id'], 12321)

def test_channel_messages_invalid_token():
    '''
    given an invalid token should raise AccessError
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user['token'], 'channel', True)
    with pytest.raises(AccessError):
        assert channel_messages("invalid", channel['channel_id'], 0)

def test_channel_messages_not_member():
    '''
    given a token that is not a member of channel_id should raise AccessError
    '''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user1['token'], 'channel', True)
    user2 = auth_register("ankitrai36@gmail.com", "12345678", "tom", "hardy")
    with pytest.raises(AccessError):
        assert channel_messages(user2['token'], channel['channel_id'], 0)

def test_channel_messages_less_50():
    '''
    function is used as intended and message list is below 50
    this test requires implementation of message_send function
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user['token'], 'channel', True)

    for i in range(0, 10):
        message_send(user['token'], channel['channel_id'], str(i))

    messages = channel_messages(user['token'], channel['channel_id'], 0)
    assert messages['start'] == 0
    assert messages['end'] == -1

    expected_id = 10
    for message_dict in messages['messages']:
        # checks whether the messages are in the right order
        assert message_dict['message_id'] == expected_id
        expected_id -= 1


def test_channel_messages_more_50():
    '''
    function is used as intended and message list is above 50
    this test requires implementation of message_send function
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user['token'], 'channel', True)

    for i in range(0, 60):
        # sends 60 messages
        message_send(user['token'], channel['channel_id'], str(i))

    messages = channel_messages(user['token'], channel['channel_id'], 0)
    assert messages['start'] == 0
    assert messages['end'] == 50

    expected_id = 60
    for message_dict in messages['messages']:
        # check whether the correct messages are on the list in the right order
        assert message_dict['message_id'] == expected_id
        expected_id -= 1

# tests for channel_addowner

def test_channel_addowner_invalid_channel_id():
    '''
    given an invalid channel_id should raise InputError
    '''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user1['token'], 'channel', True)
    user2 = auth_register("ankitrai26@gmail.com", "12345678", "tom", "hardy")
    channel_join(user2['token'], channel['channel_id'])
    with pytest.raises(InputError):
        assert channel_addowner(user1['token'], 7898789, user2['u_id'])

def test_channel_addowner_invalid_u_id():
    '''
    given an invalid u_id should raise InputError
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user['token'], 'channel', True)
    with pytest.raises(InputError):
        assert channel_addowner(user['token'], channel['channel_id'], 2312312)

def test_channel_addowner_u_id_notmember():
    '''
    given a u_id that is not a member of channel_id should raise InputError
    '''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user1['token'], 'channel', True)
    user2 = auth_register("ankitrai26@gmail.com", "12345678", "tom", "hardy")
    with pytest.raises(InputError):
        assert channel_addowner(user1['token'], channel['channel_id'], user2['u_id'])

def test_channel_addowner_user_already_owner_of_channel():
    '''
    given a u_id who is already an owner of channel_id should raise InputError
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user['token'], 'channel', True)
    with pytest.raises(InputError):
        assert channel_addowner(user['token'], channel['channel_id'], user['u_id'])

def test_channel_addowner_unauthorized_user():
    '''
    given an invalid token should raise AccessError
    '''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user1['token'], 'channel', True)
    user2 = auth_register("ankitrai36@gmail.com", "12345678", "tom", "hardy")
    channel_join(user2['token'], channel['channel_id'])
    with pytest.raises(AccessError):
        assert channel_addowner('invalid', channel['channel_id'], user2['u_id'])
def test_channel_addowner_token_notowner():
    '''
    given a token that does not have owner permissions, raised AccessError
    '''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user1['token'], 'channel', True)
    user2 = auth_register("ankitrai36@gmail.com", "12345678", "tom", "hardy")
    channel_join(user2['token'], channel['channel_id'])
    user3 = auth_register("ankitrai6@gmail.com", "12345678", "tom", "hardy")
    channel_join(user3['token'], channel['channel_id'])
    with pytest.raises(AccessError):
        channel_addowner(user2['token'], channel['channel_id'], user3['u_id'])

def test_channel_addowner_token_global_owner():
    '''
    given a token that is an owner of flockr but not local owner, should work
    '''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    user2 = auth_register("ankitrai36@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user2['token'], 'channel', True)
    channel_removeowner(user2['token'], channel['channel_id'], user2['u_id'])
    channel_addowner(user1['token'], channel['channel_id'], user2['u_id'])
    channel_detail = channel_details(user2['token'], channel['channel_id'])

    is_pass = False
    for member in channel_detail['owner_members']:
        if member['u_id'] == user2['u_id']:
            is_pass = True
    assert is_pass

def test_channel_addowner_allvalid():
    '''
    function is used as intended
    '''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user1['token'], 'channel', True)
    user2 = auth_register("ankitrai36@gmail.com", "12345678", "tom", "hardy")
    channel_join(user2['token'], channel['channel_id'])
    channel_addowner(user1['token'], channel['channel_id'], user2['u_id'])
    channel_detail = channel_details(user1['token'], channel['channel_id'])

    is_pass = False
    for member in channel_detail['owner_members']:
        if member['u_id'] == user2['u_id']:
            is_pass = True
    assert is_pass

# tests for channel_removeowner

def test_channel_removeowner_invalid_channel_id():
    '''
    given an invalid channel_id should raise InputError
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channels_create(user['token'], 'channel', True)
    with pytest.raises(InputError):
        assert channel_removeowner(user['token'], 4783949, user['u_id'])

def test_channel_removeowner_invalid_u_id():
    '''
    given an invalid u_id should raise InputError
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user['token'], 'channel', True)
    with pytest.raises(InputError):
        assert channel_removeowner(user['token'], channel['channel_id'], 3213122)

def test_channel_removeowner_u_id_not_owner_of_channel():
    '''
    given a u_id that is not an owner of channel_id should raise InputError
    '''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user1['token'], 'channel', True)
    user2 = auth_register("ankitrai32@gmail.com", "12345678", "tom", "hardy")
    channel_join(user2['token'], channel['channel_id'])
    with pytest.raises(InputError):
        assert channel_removeowner(user1['token'], channel['channel_id'], user2['u_id'])

def test_channel_removeowner_unauthorized_user():
    '''
    given an invalid token should raise AccessError
    '''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user1['token'], 'channel', True)
    user2 = auth_register("ankitrai32@gmail.com", "12345678", "tom", "hardy")
    channel_join(user2['token'], channel['channel_id'])
    channel_addowner(user1['token'], channel['channel_id'], user2['u_id'])
    with pytest.raises(AccessError):
        assert channel_removeowner('invalid', channel['channel_id'], user2['u_id'])

def test_channel_removeowner_token_notowner():
    '''
    given a token that is not an owner of channel_id should raise AccessError
    '''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user1['token'], 'channel', True)
    user2 = auth_register("ankitrai32@gmail.com", "12345678", "tom", "hardy")
    channel_join(user2['token'], channel['channel_id'])
    user3 = auth_register("ankitrai3@gmail.com", "12345678", "tom", "hardy")
    channel_join(user3['token'], channel['channel_id'])
    channel_addowner(user1['token'], channel['channel_id'], user3['u_id'])
    with pytest.raises(AccessError):
        assert channel_removeowner(user2['token'], channel['channel_id'], user3['u_id'])

def test_channel_removeowner_global_owner():
    '''
    given a token that is an owner of flockr, should work
    '''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    user2 = auth_register("ankitrai32@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user2['token'], 'channel', True)
    channel_removeowner(user1['token'], channel['channel_id'], user2['u_id'])
    channel_detail = channel_details(user2['token'], channel['channel_id'])

    is_pass = True
    for member in channel_detail['owner_members']:
        if member['u_id'] == user2['u_id']:
            is_pass = False
    assert is_pass

def test_channel_removeowner_allvalid():
    '''
    function is used as intended
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user['token'], 'channel', True)
    channel_removeowner(user['token'], channel['channel_id'], user['u_id'])
    channel_detail = channel_details(user['token'], channel['channel_id'])

    is_pass = True
    for member in channel_detail['owner_members']:
        if member['u_id'] == user['u_id']:
            is_pass = False
    assert is_pass

# Tests for channel_join:

def test_channel_join_invalid_channel():
    '''
    given an invalid channel_id should raise InputError
    '''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "1234567", "tom", "hardy")
    channels_create(user1['token'], 'Channel', True)
    user2 = auth_register("ankitrai32@gmail.com", "1234567", "tom", "hardy")
    with pytest.raises(InputError):
        assert channel_join(user2['token'], 123445)

def test_channel_join_invalid_token():
    '''
    given an invalid token should raise AccessError
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "1234567", "tom", "hardy")
    channel = channels_create(user['token'], 'Channel', True)
    auth_register("ankitrai32@gmail.com", "1234567", "tom", "hardy")
    with pytest.raises(AccessError):
        assert channel_join('invalid', channel['channel_id'])

def test_channel_join_already_member():
    '''
    given a token that is already a member of channel_id should raise AccessError
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user['token'], 'channel', True)
    with pytest.raises(AccessError):
        assert channel_join(user['token'], channel['channel_id'])

def test_channel_join_private_channel():
    '''
    given a channel_id with is_public set to False should raise AccessError
    '''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "1234567", "tom", "hardy")
    channel = channels_create(user1['token'], 'Channel', False)
    user2 = auth_register("ankitrai32@gmail.com", "1234567", "tom", "hardy")
    with pytest.raises(AccessError):
        assert channel_join(user2['token'], channel['channel_id'])

def test_channel_join_private_channel_owner():
    '''
    given a u_id who is a global owner, function should allow them to join
    private channels
    '''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "1234567", "tom", "hardy")
    user2 = auth_register("ankitrai32@gmail.com", "1234567", "tom", "hardy")
    channel = channels_create(user2['token'], 'Channel', False)
    channel_join(user1['token'], channel['channel_id'])
    user_channels = channels_list(user1['token'])
    is_pass = False
    for chan in user_channels['channels']:
        if chan['channel_id'] == channel['channel_id']:
            is_pass = True
    assert is_pass

def test_channel_join_function():
    '''
    function is used as intended
    '''
    clear()
    user1 = auth_register("ankitrai3@gmail.com", "1234567", "tom", "hardy")
    channel = channels_create(user1['token'], 'Channel', True)
    user2 = auth_register("ankitrai32@gmail.com", "1234567", "tom", "hardy")
    channel_join(user2['token'], channel['channel_id'])
    user_channels = channels_list(user2['token'])
    is_pass = False
    for chan in user_channels['channels']:
        if chan['channel_id'] == channel['channel_id']:
            is_pass = True
    assert is_pass

# Tests for channel_leave:

def test_channel_leave_invalid_channel():
    '''
    given an invalid channel_id should raise InputError
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "1234567", "tom", "hardy")
    channels_create(user['token'], 'Channel', True)
    with pytest.raises(InputError):
        assert channel_leave(user['token'], 123445)

def test_channel_leave_invalid_token():
    '''
    given an invalid token should raise AccessError
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "1234567", "tom", "hardy")
    channel = channels_create(user['token'], 'Channel', True)
    with pytest.raises(AccessError):
        assert channel_leave('invalid', channel['channel_id'])

def test_channel_leave_not_member():
    '''
    given a token that is not a member of channel_id should raise AccessError
    '''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "1234567", "tom", "hardy")
    channel = channels_create(user1['token'], 'Channel', True)
    user2 = auth_register("ankitrai32@gmail.com", "1234567", "tom", "hardy")
    with pytest.raises(AccessError):
        assert channel_leave(user2['token'], channel['channel_id'])

def test_channel_leave_function():
    '''
    function is used as intended
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "1234567", "tom", "hardy")
    channel = channels_create(user['token'], 'Channel', True)
    channel_leave(user['token'], channel['channel_id'])
    assert channels_list(user['token']) == {'channels': []}

def test_channel_leave_multiple():
    '''
    function is used with multiple users in channel
    '''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "1234567", "tom", "hardy")
    channel = channels_create(user1['token'], 'Channel', True)
    user2 = auth_register("ankitrai26@gmail.com", "1234567", "tom", "hardy")
    channel_join(user2['token'], channel['channel_id'])
    user3 = auth_register("ankitrai6@gmail.com", "1234567", "tom", "hardy")
    channel_join(user3['token'], channel['channel_id'])
    channel_leave(user3['token'], channel['channel_id'])

    assert channels_list(user3['token']) == {
        'channels': []
    }
    assert channels_list(user2['token']) == {
        'channels': [{
            'channel_id' : channel['channel_id'],
            'name' : 'Channel'
        }]
    }
    assert channels_list(user1['token']) == {
        'channels': [{
            'channel_id' : channel['channel_id'],
            'name' : 'Channel'
        }]
    }
def test_channel_leave_owner():
    '''
    given a u_id that is an owner of channel_id, owner rights are stripped as
    well
    '''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "1234567", "tom", "hardy")
    channel = channels_create(user1['token'], 'Channel', True)
    user2 = auth_register("ankitrai32@gmail.com", "1234567", "tom", "hardy")
    channel_join(user2['token'], channel['channel_id'])
    channel_addowner(user1['token'], channel['channel_id'], user2['u_id'])
    channel_leave(user2['token'], channel['channel_id'])

    channel_d = channel_details(user1['token'], channel['channel_id'])
    assert channel_d['owner_members'] == [{
        'u_id': user1['u_id'],
        'name_first': 'tom',
        'name_last': 'hardy'
    }]
