'''Importing functions to test message.py'''
import time
from datetime import datetime, timezone
import pytest
from auth import auth_register
from channels import channels_create
from channel import channel_messages, channel_join
from other import clear
from error import InputError, AccessError
from message import message_send, message_edit, message_remove, message_sendlater
from message import message_react, message_unreact, message_pin, message_unpin

# tests for message_send
def test_message_send_input_error():
    '''Raises InputError if input message is too long'''
    clear()
    user = auth_register("examplemail@gmail.com", "password1234", "bruce", "lee")
    channel = channels_create(user['token'], 'channel_one', True)
    message = ""
    i = 1
    while i <= 1001:
        message += "t" # message is 1001 characters long
        i += 1
    with pytest.raises(InputError):
        assert message_send(user['token'], channel['channel_id'], message)

def test_message_send_access_error():
    '''Raises AccessError if user is not part of the flockr channel'''
    clear()
    user1 = auth_register("examplemail1@gmail.com", "password1234", "bruce", "lee")
    user2 = auth_register("examplemail2@gmail.com", "password1234", "bruce", "lee")
    channel = channels_create(user1['token'], 'channel_one', True)
    message = "hi"
    with pytest.raises(AccessError):
        assert message_send(user2['token'], channel['channel_id'], message)

def test_message_send_invalid_token():
    '''raises InputError if invalid token is used to send message'''
    clear()
    user1 = auth_register("examplemail1@gmail.com", "password1234", "bruce", "lee")
    channel = channels_create(user1['token'], 'channel_one', True)
    invalid_token = user1['token'] + 'abc'
    message = "hi"
    with pytest.raises(AccessError):
        assert message_send(invalid_token, channel['channel_id'], message)

def test_message_send_a_message():
    '''Creates relevant inputs and sends a sample test message, then check that
    said test message appears in channel_messages'''

    clear()
    #Creating example function inputs
    user1 = auth_register("examplemail@gmail.com", "password1234", "bruce", "lee")
    channel_id1 = channels_create(user1['token'], 'channel_one', True)
    message1 = "This is a test message"

    example_message_id = message_send(user1['token'], channel_id1['channel_id'], message1)
    start = 0
    message_list = channel_messages(user1['token'], channel_id1['channel_id'], start)

    assert example_message_id['message_id'] == 1
    assert message_list['messages'][0]['message'] == message1

def test_message_send_multiple_messages():
    '''Creates relevant inputs and sends a sample test message, then check that
    said test message appears in channel_messages'''

    clear()
    #Creating example function inputs
    user1 = auth_register("examplemail@gmail.com", "password1234", "bruce", "lee")
    channel_id1 = channels_create(user1['token'], 'channel_one', True)
    message1 = "This is a test message"
    message2 = "This is also a test message"
    message3 = "and this is another test message"

    example_message_id1 = message_send(user1['token'], channel_id1['channel_id'], message1)
    example_message_id2 = message_send(user1['token'], channel_id1['channel_id'], message2)
    example_message_id3 = message_send(user1['token'], channel_id1['channel_id'], message3)

    start = 0
    message_list = channel_messages(user1['token'], channel_id1['channel_id'], start)

    assert example_message_id1['message_id'] == 1
    assert message_list['messages'][2]['message'] == message1  # this has to be the last recent
    assert example_message_id2['message_id'] == 2
    assert message_list['messages'][1]['message'] == message2
    assert example_message_id3['message_id'] == 3
    assert message_list['messages'][0]['message'] == message3  # this has to be the most recent

# tests for message_remove
def test_message_remove_invalid_token():
    '''
    Checks if the function raises AccessError when an invalid token
    is passed into the function
    '''
    user = auth_register("ankitrai329@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user['token'], 'channel', True)
    message = message_send(user['token'], channel['channel_id'], "what is up")
    invalid_token = user['token'] + "34h2j4k"

    with pytest.raises(AccessError):
        assert message_edit(invalid_token, message['message_id'], "hello")

def test_message_remove_but_message_do_not_exist():
    '''Raises InputError if message has already been deleted (does not exist)'''
    clear()
    user = auth_register("examplemail@gmail.com", "password1234", "bruce", "lee")
    channel = channels_create(user['token'], 'channel_one', True)
    message = "This needs to be deleted"
    example_message_id = message_send(user['token'], channel['channel_id'], message)
    message_remove(user['token'], example_message_id['message_id'])

    with pytest.raises(InputError):
        assert  message_remove(user['token'], example_message_id['message_id'])

def test_message_remove_access_error():
    '''Raises AccessError if user is not owner of the flockr and
    message with message_id was not sent by current user'''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    user2 = auth_register("ankitrai327@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user1['token'], 'channel', True)
    channel_join(user2['token'], channel['channel_id'])
    message = message_send(user1['token'], channel['channel_id'], "what is up")

    with pytest.raises(AccessError):
        assert message_remove(user2['token'], message['message_id'])

def test_message_remove_by_owner_who_is_not_sender():
    '''function should work if it is used by an owner of flockr'''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    user2 = auth_register("ankitrai327@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user2['token'], 'channel', True)
    channel_join(user1['token'], channel['channel_id'])
    message = message_send(user2['token'], channel['channel_id'], "what is up")
    message_remove(user1['token'], message['message_id'])

    start = 0
    message_list = channel_messages(user2['token'], channel['channel_id'], start)
    assert message_list['messages'] == []

def test_message_remove_by_channel_owner_who_is_not_sender():
    '''function should still work if it is used by channel owner'''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    user2 = auth_register("ankitrai327@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user2['token'], 'channel', True)
    channel_join(user1['token'], channel['channel_id'])
    message = message_send(user1['token'], channel['channel_id'], "what is up")
    message_remove(user2['token'], message['message_id'])

    start = 0
    message_list = channel_messages(user1['token'], channel['channel_id'], start)
    assert message_list['messages'] == []

def test_message_remove_by_user_who_is_sender():
    '''Checks if message is deleted if message is removed by sender'''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    user2 = auth_register("ankitrai327@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user1['token'], 'channel', True)
    channel_join(user2['token'], channel['channel_id'])
    message = message_send(user2['token'], channel['channel_id'], "what is up")
    message_remove(user2['token'], message['message_id'])

    start = 0
    message_list = channel_messages(user2['token'], channel['channel_id'], start)
    assert message_list['messages'] == []

def test_message_remove_by_owner_who_is_sender():
    '''Checks if message is deleted if message is removed by sender who is
    owner of flockr'''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    user2 = auth_register("ankitrai327@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user1['token'], 'channel', True)
    channel_join(user2['token'], channel['channel_id'])
    message = message_send(user1['token'], channel['channel_id'], "what is up")
    message_remove(user1['token'], message['message_id'])

    start = 0
    message_list = channel_messages(user1['token'], channel['channel_id'], start)
    assert message_list['messages'] == []

def test_message_remove_multiple_messages():
    '''Sends a message, then calls message_remove function to delete it '''
    clear()
    user1 = auth_register("examplemail@gmail.com", "password1234", "bruce", "lee")
    user2 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    user3 = auth_register("ankitrai327@gmail.com", "12345678", "tom", "hardy")
    channel_id1 = channels_create(user1['token'], 'channel_one', True)
    message1 = "This needs to be deleted"
    message2 = "i am high"
    message3 = "this guy's toast"
    start = 0

    #Need to add user to channel, otherwise message_send will throw an error
    channel_join(user2['token'], channel_id1['channel_id'])
    channel_join(user3['token'], channel_id1['channel_id'])

    example_message_id1 = message_send(user1['token'], channel_id1['channel_id'], message1)
    example_message_id2 = message_send(user2['token'], channel_id1['channel_id'], message2)
    example_message_id3 = message_send(user3['token'], channel_id1['channel_id'], message3)
    message_remove(user1['token'], example_message_id3['message_id'])

    message_list = channel_messages(user1['token'], channel_id1['channel_id'], start)
    assert message_list['messages'][0]['message'] == message2
    assert message_list['messages'][1]['message'] == message1

    message_remove(user1['token'], example_message_id2['message_id'])
    message_list = channel_messages(user1['token'], channel_id1['channel_id'], start)
    assert message_list['messages'][0]['message'] == message1
    assert message_list['messages'][0]['message_id'] == example_message_id1['message_id']

# tests for message_edit
def test_message_edit_invalid_token():
    '''
    Checks if the function raises AccessError when an invalid token
    is passed into the function
    '''
    user = auth_register("ankitrai328@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user['token'], 'channel', True)
    message = message_send(user['token'], channel['channel_id'], "what is up")
    invalid_token = user['token'] + "34h2j4k"

    with pytest.raises(AccessError):
        assert message_edit(invalid_token, message['message_id'], "hello")

def test_message_edit_access_error():
    '''Checks if function raises AccessError when message was not sent by
    authorised user and the user is not owner of channel'''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    user2 = auth_register("ankitrai327@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user1['token'], 'channel', True)
    channel_join(user2['token'], channel['channel_id'])
    message = message_send(user1['token'], channel['channel_id'], "what is up")

    with pytest.raises(AccessError):
        assert message_edit(user2['token'], message['message_id'], "hello")

def test_message_edit_user_is_owner():
    '''Checks if message can be edited by sender even if user is the
    owner, but not the sender'''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    user2 = auth_register("ankitrai327@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user2['token'], 'channel', True)
    channel_join(user1['token'], channel['channel_id'])
    message = message_send(user2['token'], channel['channel_id'], "what is up")
    message_edit(user1['token'], message['message_id'], "hello")

    start = 0
    message_list = channel_messages(user2['token'], channel['channel_id'], start)
    assert message_list['messages'][0]['message'] == "hello"

def test_message_edit_user_is_channel_owner():
    '''Checks if message can be edited by sender even if user is the
    owner, but not the sender'''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    user2 = auth_register("ankitrai327@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user2['token'], 'channel', True)
    channel_join(user1['token'], channel['channel_id'])
    message = message_send(user1['token'], channel['channel_id'], "what is up")
    message_edit(user2['token'], message['message_id'], "hello")

    start = 0
    message_list = channel_messages(user1['token'], channel['channel_id'], start)
    assert message_list['messages'][0]['message'] == "hello"

def test_message_edit_by_user_who_is_sender():
    '''Checks if message can be edited by user who is the sender'''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    user2 = auth_register("ankitrai327@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user1['token'], 'channel', True)
    channel_join(user2['token'], channel['channel_id'])
    message = message_send(user2['token'], channel['channel_id'], "what is up")
    message_edit(user2['token'], message['message_id'], "hello")

    start = 0
    message_list = channel_messages(user2['token'], channel['channel_id'], start)
    assert message_list['messages'][0]['message'] == "hello"

def test_message_edit_by_owner_who_is_sender():
    '''Checks if message can be edited by user who is both owner and sender'''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user['token'], 'channel', True)
    message1 = message_send(user['token'], channel['channel_id'], "what is up")
    message2 = message_send(user['token'], channel['channel_id'], "waddup") # most recent message
    message_edit(user['token'], message1['message_id'], "i am good")
    message_edit(user['token'], message2['message_id'], "toast") # editing most recent message

    start = 0
    message_list = channel_messages(user['token'], channel['channel_id'], start)
    assert message_list['messages'][0]['message'] == "toast"
    assert message_list['messages'][1]['message'] == "i am good"

def test_message_edit_to_empty_message():
    '''Checks if message can be edited to empty message'''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user['token'], 'channel', True)
    message = message_send(user['token'], channel['channel_id'], "what is up")
    message_edit(user['token'], message['message_id'], "")

    start = 0
    message_list = channel_messages(user['token'], channel['channel_id'], start)
    assert message_list['messages'][0]['message'] == ""

# tests for message_sendlater
def test_message_sendlater_invalid_token():
    '''User holds invalid token, should through AccessError'''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "kobe", "bryant")
    channel = channels_create(user['token'], 'channel', True)
    curr_timestamp = datetime.now(timezone.utc).timestamp()
    future_timestamp = curr_timestamp + (5 * 60)  # 5 min * 60 seconds -> 5 mins into future

    with pytest.raises(AccessError):
        assert message_sendlater("InVaLiD", channel['channel_id'], "Example", future_timestamp)

def test_message_sendlater_overlong_message():
    '''
    Throw Input error, message is over 1000 characters
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "kobe", "bryant")
    channel = channels_create(user['token'], 'channel', True)
    long_message = ""
    for i in range(1001):
        long_message += str(i)
    curr_timestamp = datetime.now(timezone.utc).timestamp()
    future_time = curr_timestamp + (5 * 60)

    with pytest.raises(InputError):
        assert message_sendlater(user['token'], channel['channel_id'], long_message, future_time)

def test_message_sendlater_invalid_channel():
    '''
    Throw InputError, channel_id given is not a valid channel
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "kobe", "bryant")
    curr_timestamp = datetime.now(timezone.utc).timestamp()
    future_timestamp = curr_timestamp + (5 * 60)

    with pytest.raises(InputError):
        assert message_sendlater(user['token'], 43, "Example message", future_timestamp)

def test_message_sendlater_invalid_timesent():
    '''
    Throw InputError, time_sent is in the past
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "kobe", "bryant")
    channel = channels_create(user['token'], 'channel', True)
    curr_timestamp = datetime.now(timezone.utc).timestamp()
    past_time = curr_timestamp - (5 * 60) #5 mins in the past

    with pytest.raises(InputError):
        assert message_sendlater(user['token'], channel['channel_id'], "Example message", past_time)

def test_message_sendlater_access_error():
    '''
    Throw AccessError, user is not a member of channel specified
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "kobe", "bryant")
    user2 = auth_register("examplemail@gmail.com", "87654321", "harland", "sanders")
    channel = channels_create(user['token'], 'channel', True)
    curr_timestamp = datetime.now(timezone.utc).timestamp()
    future_timestamp = curr_timestamp + (5 * 60)

    with pytest.raises(AccessError):
        assert message_sendlater(user2['token'], channel['channel_id'], "a", future_timestamp)

def test_message_sendlater_success():
    '''
    Function works as intended
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "kobe", "bryant")
    channel = channels_create(user['token'], 'channel', True)
    curr_timestamp = datetime.now(timezone.utc).timestamp()
    future_timestamp = curr_timestamp + (5)

    future_message = message_sendlater(user['token'], channel['channel_id'], "a", future_timestamp)
    #First assert that the message doesn't exist now
    msg_list = channel_messages(user['token'], channel['channel_id'], 0)
    assert msg_list['messages'] == []

    #Then assert that the message exists after 10 seconds
    time.sleep(10)
    future_list = channel_messages(user['token'], channel['channel_id'], 0)
    message_exists = False
    for message in future_list['messages']:
        if future_message['message_id'] == message['message_id']:
            message_exists = True
    assert message_exists

def test_message_sendlater_success_multiple():
    '''Function works as intended, sending multiple messages
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "kobe", "bryant")
    channel = channels_create(user['token'], 'channel', True)
    future_time1 = datetime.now(timezone.utc).timestamp() + 5
    future_time2 = datetime.now(timezone.utc).timestamp() + 10
    future_time3 = datetime.now(timezone.utc).timestamp() + 15

    future_message1 = message_sendlater(user['token'], channel['channel_id'], "ex1", future_time1)
    future_message2 = message_sendlater(user['token'], channel['channel_id'], "ex2", future_time2)
    future_message3 = message_sendlater(user['token'], channel['channel_id'], "ex3", future_time3)

    #No messages should appear
    msg_list = channel_messages(user['token'], channel['channel_id'], 0)
    assert msg_list['messages'] == []

    #First message should appear
    time.sleep(7)
    msg_list = channel_messages(user['token'], channel['channel_id'], 0)
    # checking for first message
    in_list = False
    for message in msg_list['messages']:
        if future_message1['message_id'] == message['message_id']:
            in_list = True
    assert in_list

    time.sleep(5)
    msg_list = channel_messages(user['token'], channel['channel_id'], 0)
    # checking for first message
    in_list = False
    for message in msg_list['messages']:
        if future_message1['message_id'] == message['message_id']:
            in_list = True
    assert in_list
    # checking for second message
    in_list = False
    for message in msg_list['messages']:
        if future_message2['message_id'] == message['message_id']:
            in_list = True
    assert in_list

    time.sleep(5)
    msg_list = channel_messages(user['token'], channel['channel_id'], 0)
    # checking for first message
    in_list = False
    for message in msg_list['messages']:
        if future_message1['message_id'] == message['message_id']:
            in_list = True
    assert in_list
    # checking for second message
    in_list = False
    for message in msg_list['messages']:
        if future_message2['message_id'] == message['message_id']:
            in_list = True
    assert in_list
    # checking for third message
    in_list = False
    for message in msg_list['messages']:
        if future_message3['message_id'] == message['message_id']:
            in_list = True
    assert in_list

# tests for message_react
def test_message_react_invalid_token():
    '''
    check if function raises AccessError when an invalid token is passed
    into the function
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user['token'], 'channel', True)
    message1 = message_send(user['token'], channel['channel_id'], "what is up")
    react_id = 1
    invalid_token = user['token'] + "38uhnkwejfbjwbrj"

    with pytest.raises(AccessError):
        assert message_react(invalid_token, message1['message_id'], react_id)

def test_message_react_invalid_message_id():
    '''
    check if function raises InputError when an invalid message_id is passed
    into the function
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user['token'], 'channel', True)
    message_send(user['token'], channel['channel_id'], "what is up")
    react_id = 1
    invalid_message_id = 4567

    with pytest.raises(InputError):
        assert message_react(user['token'], invalid_message_id, react_id)

def test_message_react_invalid_react_id():
    '''
    check if function raises InputError when an invalid react_id is passed
    into the function
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user['token'], 'channel', True)
    message1 = message_send(user['token'], channel['channel_id'], "what is up")
    invalid_react_id = 123

    with pytest.raises(InputError):
        assert message_react(user['token'], message1['message_id'], invalid_react_id)

def test_message_react_message_already_contain_active_react_id():
    '''
    check if function raises InputError in the case where the message with
    message_id already has an active react from the user
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user['token'], 'channel', True)
    message1 = message_send(user['token'], channel['channel_id'], "what is up")
    react_id = 1
    message_react(user['token'], message1['message_id'], react_id)

    with pytest.raises(InputError):
        assert message_react(user['token'], message1['message_id'], react_id)

def test_message_react_all_valid():
    '''
    check if the function successfully appends the user's uid into the
    react list for a given messsage, given the correct parameters
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user['token'], 'channel', True)
    message1 = message_send(user['token'], channel['channel_id'], "what is up")
    react_id = 1
    message_react(user['token'], message1['message_id'], react_id)

    start = 0
    message_list = channel_messages(user['token'], channel['channel_id'], start)
    assert user['u_id'] in message_list['messages'][0]['reacts'][0]['u_ids']

# tests for message_unreact
def test_message_unreact_invalid_token():
    '''
    check if function raises AccessError when an invalid token is passed
    into the function
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user['token'], 'channel', True)
    message1 = message_send(user['token'], channel['channel_id'], "what is up")
    react_id = 1
    message_react(user['token'], message1['message_id'], react_id)
    invalid_token = user['token'] + "38uhnkwejfbjwbrj"

    with pytest.raises(AccessError):
        assert message_unreact(invalid_token, message1['message_id'], react_id)

def test_message_unreact_invalid_message_id():
    '''
    check if function raises InputError when an invalid message_id is passed
    into the function
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user['token'], 'channel', True)
    message1 = message_send(user['token'], channel['channel_id'], "what is up")
    react_id = 1
    message_react(user['token'], message1['message_id'], react_id)
    invalid_message_id = 4567

    with pytest.raises(InputError):
        assert message_unreact(user['token'], invalid_message_id, react_id)

def test_message_unreact_invalid_react_id():
    '''
    check if function raises InputError when an invalid react_id is passed
    into the function
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user['token'], 'channel', True)
    message1 = message_send(user['token'], channel['channel_id'], "what is up")
    valid_react_id = 1
    invalid_react_id = 1223
    message_react(user['token'], message1['message_id'], valid_react_id)

    with pytest.raises(InputError):
        assert message_unreact(user['token'], message1['message_id'], invalid_react_id)

def test_message_unreact_message_does_not_contain_active_react_id():
    '''
    check if function raises InputError in the case where the message with
    message_id does not contain an active react from the user
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user['token'], 'channel', True)
    message1 = message_send(user['token'], channel['channel_id'], "what is up")
    react_id = 1

    with pytest.raises(InputError):
        assert message_unreact(user['token'], message1['message_id'], react_id)

def test_message_unreact_all_valid():
    '''
    check if the function successfully remove the user's uid from the react list
    for a given message, given the correct parameters
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user['token'], 'channel', True)
    message1 = message_send(user['token'], channel['channel_id'], "what is up")
    react_id = 1
    message_react(user['token'], message1['message_id'], react_id)
    message_unreact(user['token'], message1['message_id'], react_id)

    start = 0
    message_list = channel_messages(user['token'], channel['channel_id'], start)
    assert user['u_id'] not in message_list['messages'][0]['reacts'][0]['u_ids']

# tests for message_pin
def test_message_pin_invalid_token():
    '''
    check if function raises AccessError when an invalid token is passed
    into the function
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user['token'], 'channel', True)
    message1 = message_send(user['token'], channel['channel_id'], "what is up")
    invalid_token = user['token'] + "rh3j3k"

    with pytest.raises(AccessError):
        assert message_pin(invalid_token, message1['message_id'])

def test_message_pin_invalid_message_id():
    '''
    check if function raises InputError when an invalid message_id is passed
    into the function
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user['token'], 'channel', True)
    message_send(user['token'], channel['channel_id'], "what is up")
    invalid_message_id = 43278

    with pytest.raises(InputError):
        assert message_pin(user['token'], invalid_message_id)

def test_message_pin_message_already_pinned():
    '''
    check if the function raises InputError when trying to pin a message
    that is already pinned
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user['token'], 'channel', True)
    message1 = message_send(user['token'], channel['channel_id'], "what is up")
    message_pin(user['token'], message1['message_id'])

    with pytest.raises(InputError):
        assert message_pin(user['token'], message1['message_id'])

def test_message_pin_user_is_not_member_of_channel():
    '''
    check if the function raises AccessError when the user is not a member
    nor an owner of the channel where the message with message id is in
    '''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    user2 = auth_register("ankitrai327@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user1['token'], 'channel', True)
    message1 = message_send(user1['token'], channel['channel_id'], "what is up")

    with pytest.raises(AccessError):
        message_pin(user2['token'], message1['message_id'])


def test_message_pin_user_is_member_but_not_owner_of_channel():
    '''
    check if the function raises AccessError when the user is a member but not
    an owner of the channel where the message with message id is in
    '''
    clear()
    user1 = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    user2 = auth_register("ankitrai327@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user1['token'], 'channel', True)
    channel_join(user2['token'], channel['channel_id'])
    message1 = message_send(user2['token'], channel['channel_id'], "what is up")

    with pytest.raises(AccessError):
        message_pin(user2['token'], message1['message_id'])

def test_message_pin_all_valid():
    '''
    check if the function successfully pins the given message,
    given the correct parameters
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user['token'], 'channel', True)
    message1 = message_send(user['token'], channel['channel_id'], "what is up")
    message_pin(user['token'], message1['message_id'])

    start = 0
    message_list = channel_messages(user['token'], channel['channel_id'], start)
    assert message_list['messages'][0]['is_pinned']

# tests for message_unpin
def test_message_unpin_invalid_token():
    '''
    check if function raises AccessError when an invalid token is passed
    into the function
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user['token'], 'channel', True)
    message1 = message_send(user['token'], channel['channel_id'], "what is up")
    message_pin(user['token'], message1['message_id'])
    invalid_token = user['token'] + "34b32j43k"

    with pytest.raises(AccessError):
        message_unpin(invalid_token, message1['message_id'])

def test_message_unpin_invalid_message_id():
    '''
    check if function raises InputError when an invalid message_id is passed
    into the function
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user['token'], 'channel', True)
    message1 = message_send(user['token'], channel['channel_id'], "what is up")
    message_pin(user['token'], message1['message_id'])
    invalid_message_id = 4378

    with pytest.raises(InputError):
        message_unpin(user['token'], invalid_message_id)

def test_message_unpin_message_already_unpinned():
    '''
    check if the function raises InputError when trying to unpin a message
    that is not pinned
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user['token'], 'channel', True)
    message1 = message_send(user['token'], channel['channel_id'], "what is up")
    message_pin(user['token'], message1['message_id'])
    message_unpin(user['token'], message1['message_id'])

    with pytest.raises(InputError):
        message_unpin(user['token'], message1['message_id'])

def test_message_unpin_user_is_not_member_of_channel():
    '''
    check if the function raises AccessError when the user is not a member
    nor an owner of the channel where the message with message id is in
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    user2 = auth_register("ankitrai327@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user['token'], 'channel', True)
    message1 = message_send(user['token'], channel['channel_id'], "what is up")
    message_pin(user['token'], message1['message_id'])

    with pytest.raises(AccessError):
        message_unpin(user2['token'], message1['message_id'])

def test_message_unpin_user_is_member_but_not_owner_of_channel():
    '''
    check if the function raises AccessError when the user is a member but not
    an owner of the channel where the message with message id is in
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    user2 = auth_register("ankitrai327@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user['token'], 'channel', True)
    channel_join(user2['token'], channel['channel_id'])
    message1 = message_send(user['token'], channel['channel_id'], "what is up")
    message_pin(user['token'], message1['message_id'])

    with pytest.raises(AccessError):
        message_unpin(user2['token'], message1['message_id'])

def test_message_unpin_all_valid():
    '''
    check if the function successfully unpins the given message,
    given the correct parameters
    '''
    clear()
    user = auth_register("ankitrai326@gmail.com", "12345678", "tom", "hardy")
    channel = channels_create(user['token'], 'channel', True)
    message1 = message_send(user['token'], channel['channel_id'], "what is up")
    message_pin(user['token'], message1['message_id'])
    message_unpin(user['token'], message1['message_id'])

    start = 0
    message_list = channel_messages(user['token'], channel['channel_id'], start)
    assert not message_list['messages'][0]['is_pinned']
