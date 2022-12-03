'''
Helper functions for all functions
string module provides alphabet list for handle management
random module provides support for generating random number as token
re, signal, time and subprocess is used for url function
'''

from datetime import datetime, timezone
import string
import random
import re
import signal
from time import sleep
from subprocess import Popen, PIPE
import pytest
from error import AccessError, InputError

def generate_handle(name_first, name_last, data):
    '''
    This function generates a handle based on a user's first name and
    last name and ensures the handle is unique by checking it with data. The
    handle will be altered if the handle generated is already in use, making
    each handle unique to their respective users.
    '''
    handle = name_first + name_last
    handle = handle.lower()
    handle = handle[:20]

    alphabet = 0
    replace_position = -1
    alphabet_string = string.ascii_lowercase
    alphabet_list = list(alphabet_string)
    restart_loop = True
    while restart_loop:
        restart_loop = False
        for user in data['users']:
            if data['users'][user]['handle_str'] == handle:
                restart_loop = True
                if len(handle) < 20:
                    handle = handle + '_'
                elif len(handle) == 20:
                    handle = handle[:replace_position] + alphabet_list[alphabet]
                    alphabet += 1
                    if alphabet == 26:
                        alphabet = 0
                        replace_position += -1
    return handle

def generate_token(data):
    '''
    This function generates a token, which is a random number that is
    converted to a string. The token is then checked with data to ensure that
    the token is unique.
    '''
    token = random.randrange(10000, 99000)
    restart_loop = True
    while restart_loop:
        restart_loop = False
        for user in data['users']:
            if 'token' in data['users'][user]:
                if data['users'][user]['token'] == str(token):
                    token += 1
                    restart_loop = True

    return token

def channel_is_member(channel_id, u_id, data):
    '''
    helper function used to check whether a given u_id is a member of a given
    channel
    '''
    is_member = False
    for channel in data['users'][u_id]['channel_membership']:
        if channel['channel_id'] == channel_id:
            is_member = True
    return is_member

def channel_has_owner_permissions(channel_id, u_id, data):
    '''
    helper function used to check whether a given u_id has owner permissions of
    a given channel
    '''
    has_owner = False
    # checking for global owner
    if data['users'][u_id]['permission_id'] == 1:
        has_owner = True

    # checking for creator of the channel
    token = data['users'][u_id]['token']
    if data['channels'][channel_id]['creator'] == token:
        has_owner = True

    for member in data['channels'][channel_id]['owner_members']:
        # checking for local owner
        if member['u_id'] == u_id:
            has_owner = True
    return has_owner

def is_channel_owner(token, channel_id, data):
    '''Helper function for AccessError condition in message_remove function'''

    for owner_member in data['channels'][channel_id]['owner_members']:
        u_id = owner_member['u_id']
        if data['users'][u_id]['token'] == token:
            return True
    return False

def u_id_finder(token, data):
    '''Given a token, search through the data variable to match validated token to a user_id'''
    u_id = -1
    for user in data['users']:
        if 'token' in data['users'][user]:
            if data['users'][user]['token'] == token:
                u_id = user

    if u_id == -1:
        raise AccessError("Invalid token entered")
    return u_id

def valid_token(token, data):
    '''Given a token, search through users list to ensure that token is valid
    Returns True if token is indeed valid '''
    for user in data['users']:
        if 'token' in data['users'][user]:
            if data['users'][user]['token'] == token:
                return True
    return False

def valid_channel(channel_id, data):
    '''Given a channel_id, check that it is a valid channel and is in channels list'''
    for channels in data['channels']:
        if data['channels'][channels]['channel_id'] == channel_id:
            return True
    return False

def valid_user_id(u_id, data):
    '''Given a u_id, check that it is a valid u_id'''
    for users in data['users']:
        if data['users'][users]['u_id'] == u_id:
            return True
    return False

def message_send_future(u_id, channel_id, message, message_id, data):
    '''Used for sending messages in the future'''
    #Time_created
    curr_time = datetime.now()
    timestamp = curr_time.replace(tzinfo=timezone.utc).timestamp()
    #Populating the new messages dictionary
    message_dict = {
        'message_id': message_id,
        'u_id': u_id,
        'message': message,
        'time_created': timestamp,
        'reacts': [],
        'is_pinned': False
    }

    for messages in data['msg_later_list']:
        if messages['message_id'] == message_id:
            del messages

    #Inserting into the messages data structure within global var data
    msg_list = data['channels'][channel_id]['messages']
    msg_list.insert(0, message_dict)
    data['channels'][channel_id]['messages'] = msg_list

    return {
        'message_id': message_id,
    }

def standup_end(channel_id, token, message_id, data):
    '''Function is called when startup ends (in startup_start function)'''
    standup_msg = "\n".join(data['channels'][channel_id]['standup']['messages'])
    del data['channels'][channel_id]['standup']
    u_id = u_id_finder(token, data)
    message_send_future(u_id, channel_id, standup_msg, message_id, data)

def message_id_in_which_channel(message_id, data):
    '''
    Finding the channel_id of a channel in which the message with message_id exists
    '''
    for channel_id in data['channels']:
        for message_dict in data['channels'][channel_id]['messages']:
            if message_dict['message_id'] == message_id:
                return channel_id

    raise InputError("Message cannot be found in any channel")

def is_user_in_channel(channel_id, u_id, data):
    '''
    Check to see whether a user of u_id is in the channel with channel_id
    '''
    user_in_channel = False

    for owner in data['channels'][channel_id]['owner_members']:
        if owner['u_id'] == u_id:
            user_in_channel = True
            break

    if not user_in_channel:
        for member in data['channels'][channel_id]['all_members']:
            if member['u_id'] == u_id:
                user_in_channel = True
                break

    return user_in_channel

# Use this fixture to get the URL of the server.
@pytest.fixture
def url():
    '''
    function to find base url
    '''
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")
