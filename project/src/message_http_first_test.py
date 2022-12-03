'''requests is imported to obtain data from flask server'''
import time
from datetime import datetime, timezone
import requests
import pytest

@pytest.mark.usefixtures("url")
def test_url(url):
    '''
    A simple sanity test to check that your server is set up properly
    '''
    assert url.startswith("http")

# for message_send

def test_message_send_http(url):
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

    requests.post(f'{url}/channel/join', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id']
    })

    requests.post(f'{url}/message/send', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': 'Example message'
    })

    in_url = f"{url}/channel/messages?token={register_payload['token']}&"
    in_url2 = f"channel_id={channel_payload['channel_id']}&start=0"
    message_list = requests.get(in_url + in_url2)
    channel_messages = message_list.json()

    assert channel_messages['messages'][0]['message'] == 'Example message'

def test_message_send_http_invalid_message(url):
    '''
    Should riase InputError due to the message breaching the maximum character limit
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

    requests.post(f'{url}/channel/join', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id']
    })

    channel_payload = response2.json()
    response3 = requests.post(f'{url}/message/send', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': """This message is going to be too long
        This message is going to be too long 
        This message is going to be too long 
        This message is going to be too long
        This message is going to be too long 
        This message is going to be too long 
        This message is going to be too long 
        This message is going to be too long 
        This message is going to be too long 
        This message is going to be too long 
        This message is going to be too long 
        This message is going to be too long 
        This message is going to be too long 
        This message is going to be too long 
        This message is going to be too long 
        This message is going to be too long 
        This message is going to be too long 
        This message is going to be too long 
        This message is going to be too long 
        This message is going to be too long 
        This message is going to be too long 
        This message is going to be too long 
        This message is going to be too long 
        This message is going to be too long 
        This message is going to be too long 
        This message is going to be too long 
        This message is going to be too long 
        This message is going to be too long 
        This message is going to be too long 
        This message is going to be too long 
        This message is going to be too long 
        This message is going to be too long 
        This message is going to be too long"""
    })
    message_payload = response3.json()
    assert message_payload['code'] == 400
    assert message_payload['message'] == '<p>Message is too long</p>'

def test_message_send_http_invalid_user(url):
    '''
    Raise AccessError since the token in message send is invalidated
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

    requests.post(f'{url}/channel/join', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id']
    })

    response3 = requests.post(f'{url}/message/send', json={
        'token': 'unauthorised user',
        'channel_id': channel_payload['channel_id'],
        'message': 'Blah blah blah'
    })
    message_payload = response3.json()

    assert message_payload['code'] == 400
    assert message_payload['message'] == '<p>Invalid token entered</p>'

# for message_remove

def test_message_remove_http(url):
    '''
    Function used as intended
    '''
    requests.delete(f'{url}/clear')

    response1 = requests.post(f'{url}/auth/register', json={
        'email': 'example@gmail.com',
        'password':'12345678',
        'name_first': 'Pooh',
        'name_last':'bear'
    })
    register_payload = response1.json()

    response2 = requests.post(f'{url}/channels/create', json={
        'token': register_payload['token'],
        'name': 'channel1',
        'is_public': True
    })
    channel_payload = response2.json()

    requests.post(f'{url}/channel/join', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id']
    })

    response3 = requests.post(f'{url}/message/send', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': 'Testing message remove'
    })
    message_payload = response3.json()

    requests.delete(f'{url}/message/remove', json={
        'token': register_payload['token'],
        'message_id': message_payload['message_id']
    })

    in_url = f"{url}/channel/messages?token={register_payload['token']}&"
    in_url2 = f"channel_id={channel_payload['channel_id']}&start=0"
    response5 = requests.get(in_url + in_url2)
    message_list = response5.json()

    assert message_list['messages'] == []

def test_message_remove_http_message_nonexistent(url):
    '''
    Raise Input Error since the message does not exist
    '''
    requests.delete(f'{url}/clear')

    response1 = requests.post(f'{url}/auth/register', json={
        'email': 'example@gmail.com',
        'password':'12345678',
        'name_first': 'John',
        'name_last':'Wick'
    })
    register_payload = response1.json()

    response4 = requests.delete(f'{url}/message/remove', json={
        'token': register_payload['token'],
        'message_id': -10
    })
    result = response4.json()

    assert result['code'] == 400
    assert result['message'] == '<p>Message no longer exists</p>'

def test_messsage_remove_http_message_unauthorised(url):
    '''
    Token from user removing message does not match message sent nor has
    owner permissions
    '''
    requests.delete(f'{url}/clear')

    user1 = requests.post(f'{url}/auth/register', json={
        'email': 'example@gmail.com',
        'password':'12345678',
        'name_first': 'Mike',
        'name_last':'Hunt'
    })
    user2 = requests.post(f'{url}/auth/register', json={
        'email': 'example2@gmail.com',
        'password':'8642135',
        'name_first': 'Richard',
        'name_last':'Stroker'
    })

    register_payload = user1.json()
    register2 = user2.json()

    response2 = requests.post(f'{url}/channels/create', json={
        'token': register_payload['token'],
        'name': 'channel1',
        'is_public': True
    })
    channel_payload = response2.json()

    requests.post(f'{url}/channel/join', json={
        'token': register2['token'],
        'channel_id': channel_payload['channel_id']
    })

    response3 = requests.post(f'{url}/message/send', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': 'Testing message remove'
    })
    message_payload = response3.json()

    response4 = requests.delete(f'{url}/message/remove', json={
        'token': register2['token'],
        'message_id': message_payload['message_id']
    })

    result = response4.json()
    error_message = '<p>You do not have permissions to delete this message</p>'
    assert result['code'] == 400
    assert result['message'] == error_message

def test_message_remove_http_multiple(url):
    '''
    Function used as intended, several messages sent
    '''
    requests.delete(f'{url}/clear')

    user1 = requests.post(f'{url}/auth/register', json={
        'email': 'example@gmail.com',
        'password':'12345678',
        'name_first': 'Lebron',
        'name_last':'James'
    })
    register_payload = user1.json()

    response = requests.post(f'{url}/channels/create', json={
        'token': register_payload['token'],
        'name': 'channel1',
        'is_public': True
    })
    channel_payload = response.json()

    requests.post(f'{url}/channel/join', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id']
    })

    requests.post(f'{url}/message/send', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': 'Testing message remove'
    })

    requests.post(f'{url}/message/send', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': 'This should stay'
    })

    message3 = requests.post(f'{url}/message/send', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': 'This should be deleted'
    })
    message_payload = message3.json()

    requests.delete(f'{url}/message/remove', json={
        'token': register_payload['token'],
        'message_id': message_payload['message_id']
    })

    in_url = f"{url}/channel/messages?token={register_payload['token']}&"
    in_url2 = f"channel_id={channel_payload['channel_id']}&start=0"
    messages_list = requests.get(in_url + in_url2)

    channel_messages = messages_list.json()
    assert channel_messages['messages'][0]['message'] == 'This should stay'
    assert channel_messages['messages'][1]['message'] == 'Testing message remove'
    assert len(channel_messages['messages']) == 2


def test_message_edit_access_error(url):
    '''
    Throw access error since the user does not have permissions
    '''
    requests.delete(f'{url}/clear')

    response1 = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user1_payload = response1.json()

    response2 = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai327@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user2_payload = response2.json()

    response3 = requests.post(f'{url}/channels/create', json={
        'token': user1_payload['token'],
        'name': 'channel1',
        'is_public': True
    })
    channel = response3.json()

    requests.post(f'{url}/channel/join', json={
        'token': user2_payload['token'],
        'channel_id': channel['channel_id']
    })

    response5 = requests.post(f'{url}/message/send', json={
        'token': user1_payload['token'],
        'channel_id': channel['channel_id'],
        'message': 'just one message'
    })
    message_send_payload = response5.json()

    response6 = requests.put(f'{url}/message/edit', json={
        'token': user2_payload['token'],
        'message_id': message_send_payload['message_id'],
        'message': 'change the message'
    })
    message_edit_payload = response6.json()

    error_message = '<p>You do not have permissions to delete this message</p>'
    assert message_edit_payload['code'] == 400
    assert message_edit_payload['message'] == error_message

def test_message_edit_http_by_channel_owner_who_is_not_sender(url):
    '''
    Function as intended since owner has permissions
    '''
    requests.delete(f'{url}/clear')

    response1 = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user1_payload = response1.json()

    response2 = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai327@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user2_payload = response2.json()

    # user2 is an owner of the channel
    response3 = requests.post(f'{url}/channels/create', json={
        'token': user2_payload['token'],
        'name': 'channel1',
        'is_public': True
    })
    channel_payload = response3.json()

    # user1 is only a user of the channel
    requests.post(f'{url}/channel/join', json={
        'token': user1_payload['token'],
        'channel_id': channel_payload['channel_id']
    })

    # user1 sends a message
    response5 = requests.post(f'{url}/message/send', json={
        'token': user1_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': 'just one message'
    })
    message_send_payload = response5.json()

    # user2 edits the message
    requests.put(f'{url}/message/edit', json={
        'token': user2_payload['token'],
        'message_id': message_send_payload['message_id'],
        'message': 'change the message'
    })

    in_url = f"{url}/channel/messages?token={user1_payload['token']}&"
    in_url2 = f"channel_id={channel_payload['channel_id']}&start=0"
    response5 = requests.get(in_url + in_url2)
    message_list_payload = response5.json()

    assert message_list_payload['messages'][0]['message'] == 'change the message'

def test_message_edit_http_by_user_who_is_sender(url):
    '''
    Function as intended since user has authority to edit messages
    '''
    requests.delete(f'{url}/clear')

    response1 = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user1_payload = response1.json()

    response2 = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai327@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user2_payload = response2.json()

    # user1 is an owner of the channel
    response3 = requests.post(f'{url}/channels/create', json={
        'token': user1_payload['token'],
        'name': 'channel1',
        'is_public': True
    })
    channel_payload = response3.json()

    # user2 is only a user of the channel
    requests.post(f'{url}/channel/join', json={
        'token': user2_payload['token'],
        'channel_id': channel_payload['channel_id']
    })

    # user2 sends a message
    response5 = requests.post(f'{url}/message/send', json={
        'token': user2_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': 'just one message'
    })
    message_send_payload = response5.json()

    # user2 edits the message
    requests.put(f'{url}/message/edit', json={
        'token': user2_payload['token'],
        'message_id': message_send_payload['message_id'],
        'message': 'change the message'
    })

    in_url = f"{url}/channel/messages?token={user2_payload['token']}&"
    in_url2 = f"channel_id={channel_payload['channel_id']}&start=0"
    response5 = requests.get(in_url + in_url2)
    message_list_payload = response5.json()

    assert message_list_payload['messages'][0]['message'] == 'change the message'

def test_message_edit_http_to_empty_message(url):
    '''
    As specified, the message is deleted if the message is an empty string
    '''
    requests.delete(f'{url}/clear')

    response1 = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user1_payload = response1.json()

    # user1 is an owner of the channel
    response2 = requests.post(f'{url}/channels/create', json={
        'token': user1_payload['token'],
        'name': 'channel1',
        'is_public': True
    })
    channel_payload = response2.json()

    # user1 sends a message
    response3 = requests.post(f'{url}/message/send', json={
        'token': user1_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': 'just one message'
    })
    message_send_payload = response3.json()

    # user1 edits the message to become empty
    requests.put(f'{url}/message/edit', json={
        'token': user1_payload['token'],
        'message_id': message_send_payload['message_id'],
        'message': ''
    })

    in_url = f"{url}/channel/messages?token={user1_payload['token']}&"
    in_url2 = f"channel_id={channel_payload['channel_id']}&start=0"
    response5 = requests.get(in_url + in_url2)
    message_list_payload = response5.json()

    assert message_list_payload['messages'][0]['message'] == ''

def test_message_edit_http_by_owner_who_is_sender(url):
    '''
    Function as inteded, since both permission requirements are fulfilled
    '''
    requests.delete(f'{url}/clear')

    response1 = requests.post(f'{url}/auth/register', json={
        'email': 'ankitrai326@gmail.com',
        'password': '12345678',
        'name_first': 'tom',
        'name_last': 'hardy'
    })
    user1_payload = response1.json()

    # user1 is an owner of the channel
    response2 = requests.post(f'{url}/channels/create', json={
        'token': user1_payload['token'],
        'name': 'channel1',
        'is_public': True
    })
    channel_payload = response2.json()

    # user1 sends a message
    response3 = requests.post(f'{url}/message/send', json={
        'token': user1_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': 'just one message'
    })
    message_send_payload = response3.json()

    # user1 edits the message
    requests.put(f'{url}/message/edit', json={
        'token': user1_payload['token'],
        'message_id': message_send_payload['message_id'],
        'message': 'change the message'
    })

    in_url = f"{url}/channel/messages?token={user1_payload['token']}&"
    in_url2 = f"channel_id={channel_payload['channel_id']}&start=0"
    response5 = requests.get(in_url + in_url2)
    message_list_payload = response5.json()

    assert message_list_payload['messages'][0]['message'] == 'change the message'

def test_message_sendlater_http_input_error(url):
    '''Test to check for input error since time_sent is in the past
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

    past_time = datetime.now(timezone.utc).timestamp() - 5*60
    sendlater_response = requests.post(f'{url}/message/sendlater', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': 'Example message',
        'time_sent': past_time
    })
    payload = sendlater_response.json()
    error_message = "<p>Time sent is in the past</p>"
    assert payload['code'] == 400
    assert payload['message'] == error_message

def test_message_sendlater_http_access_error(url):
    '''Test to check for access error user is not a member of the channel
    they are trying to post to
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

    response3 = requests.post(f'{url}/auth/register', json={
        'email': 'noodles@gmail.com',
        'password':'87654321',
        'name_first': 'James',
        'name_last':'Bond'
    })
    register2_payload = response3.json()

    future_time = datetime.now(timezone.utc).timestamp() + 5*60
    sendlater_response = requests.post(f'{url}/message/sendlater', json={
        'token': register2_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': 'Example message',
        'time_sent': future_time #time is ok now
    })

    payload = sendlater_response.json()
    error_message = "<p>User is not a member of given channel</p>"
    assert payload['code'] == 400
    assert payload['message'] == error_message

def test_message_sendlater_http_success(url):
    '''Function works as intended
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

    future_time = datetime.now(timezone.utc).timestamp() + 7
    requests.post(f'{url}/message/sendlater', json={
        'token': register_payload['token'],
        'channel_id': channel_payload['channel_id'],
        'message': 'Future message',
        'time_sent': future_time #5 Seconds in the future
    })

    in_url = f"{url}/channel/messages?token={register_payload['token']}&"
    in_url2 = f"channel_id={channel_payload['channel_id']}&start=0"
    message_list = requests.get(in_url + in_url2)
    channel_messages = message_list.json()
    #channel messages list should be empty at first
    assert channel_messages['messages'] == []

    time.sleep(10)
    message_list = requests.get(in_url + in_url2)
    channel_messages = message_list.json()
    #The message should appear now
    assert channel_messages['messages'][0]['message'] == "Future message"
