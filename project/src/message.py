'''Relevant modules that allow us to give timestamps to when mesesages are sent, access global
data variable and throw relevant errors '''
from datetime import datetime, timezone
import threading
from error import InputError, AccessError
from data import data
from helper_functions import is_channel_owner, u_id_finder, channel_is_member
from helper_functions import valid_token, valid_channel, message_send_future
from helper_functions import channel_has_owner_permissions, is_user_in_channel
from helper_functions import message_id_in_which_channel

def message_send(token, channel_id, message, message_id=None):
    '''Send a message from authorised_user to the channel specified by channel_id'''

    #Input Error handling
    if len(message) > 1000:
        raise InputError("Message is too long")

    u_id = u_id_finder(token, data)
    #Access Error handling using helper function
    is_channel_member = channel_is_member(channel_id, u_id, data)
    if not is_channel_member:
        raise AccessError("User is not a member of given channel")
    #Populating messages dictionary
    if message_id is None:
        total_msgs = 0
        for channels in data['channels']:
            total_msgs += len(data['msg_later_list']) + len(data['channels'][channels]['messages'])
            if channels == channel_id:
                msg_id = total_msgs + 1
    else:
        msg_id = message_id

    #Time_created
    curr_time = datetime.now()
    timestamp = curr_time.replace(tzinfo=timezone.utc).timestamp()
    #Populating the new messages dictionary
    message_dict = {
        'message_id': msg_id,
        'u_id': u_id,
        'message': message,
        'time_created': timestamp,
        'reacts': [],
        'is_pinned': False
    }

    #Inserting into the messages data structure within global var data
    msg_list = data['channels'][channel_id]['messages']
    msg_list.insert(0, message_dict)
    data['channels'][channel_id]['messages'] = msg_list

    return {
        'message_id': msg_id,
    }

def message_remove(token, message_id):
    '''
    Given a message_id for a message
    and token to validate user permissions, this message is removed from the channel
    '''

    # InputError Handling
    # Also obtain u_id and channel_id
    u_id_sender = ''
    message_exists = False
    for channel in data['channels']:
        for message in data['channels'][channel]['messages']:
            if message_id == message['message_id']:
                message_exists = True
                u_id_sender = message['u_id']
                channel_id = channel
                break

    if not message_exists:
        raise InputError("Message no longer exists")

    #AccessError handling
    u_id = u_id_finder(token, data)
    if data['users'][u_id]['permission_id'] == 2:
        if (u_id != u_id_sender) and (not is_channel_owner(token, channel_id, data)):
            raise AccessError("You do not have permissions to delete this message")

    #Deletion
    index = 0
    for message in data['channels'][channel_id]['messages']:
        if message_id == message['message_id']:
            message_list = data['channels'][channel_id]['messages']
            message_list.pop(index)
            data['channels'][channel_id]['messages'] = message_list
            break
        index += 1
    return {

    }

def message_edit(token, message_id, message):
    '''
    Takes in token, message_id and message and updates the message's text with new text
    according to message given. If the new message is an empty string, the message is deleted.
    '''
    # catching AccessError
    u_id_sender = ''
    for channel in data['channels']:
        for message_dict in data['channels'][channel]['messages']:
            if message_dict['message_id'] == message_id:
                u_id_sender = message_dict['u_id']
                channel_id = channel
                break

    u_id = u_id_finder(token, data)
    if data['users'][u_id]['permission_id'] == 2:
        if (u_id != u_id_sender) and (not is_channel_owner(token, channel_id, data)):
            raise AccessError("You do not have permissions to delete this message")

    # edit the message in the data structure
    for message_dict in data['channels'][channel_id]['messages']:
        if message_dict['message_id'] == message_id:
            message_dict['message'] = message

    return {}

def message_sendlater(token, channel_id, message, time_sent):
    '''Sends a message after a specified amount of time (Calls message_send)
    '''
    #Validate token
    if not valid_token(token, data):
        raise AccessError("Invalid token")

    #Input Error Handling
    if len(message) > 1000:
        raise InputError("Message is too long")

    if not valid_channel(channel_id, data):
        raise InputError("Not a valid channel")

    if time_sent < datetime.now(timezone.utc).timestamp():
        raise InputError("Time sent is in the past")

    #Access Error
    u_id = u_id_finder(token, data)
    if not channel_is_member(channel_id, u_id, data):
        raise AccessError("User is not a member of given channel")

    #Generating new message_id for future message
    total_messages = 0
    for channels in data['channels']:
        total_messages += len(data['msg_later_list']) + len(data['channels'][channels]['messages'])
        if channels == channel_id:
            msg_id = total_messages + 1

    future_msg = {
        'message_id': msg_id,
        'user_id': u_id,
        'message': message,
        'time_created': time_sent,
        'reacts': [],
        'is_pinned': False
    }
    data['msg_later_list'].append(future_msg)
    time_dif = time_sent - datetime.now(timezone.utc).timestamp()
    time = threading.Timer(time_dif, message_send_future, [u_id, channel_id, message, msg_id, data])
    time.start()
    return {
        'message_id': future_msg['message_id']
    }

def message_react(token, message_id, react_id):
    '''
    Takes in token, message_id, and react_id to give a react to a message
    with message_id from the user given by the token
    '''
    # invalid token
    u_id = u_id_finder(token, data)

    # invalid message_id
    channel_id = message_id_in_which_channel(message_id, data)
    valid_message_id = is_user_in_channel(channel_id, u_id, data)

    if not valid_message_id:
        raise InputError("Message is not in a channel that the user is in.")

    # invalid react_id
    if react_id != 1:
        raise InputError("Invalid react id")

    # check whether message with message_id already contains an active react from the user
    for message in data['channels'][channel_id]['messages']:
        if message['message_id'] == message_id:
            react_exists = False
            for react in message['reacts']:
                if react['react_id'] == react_id:
                    react_exists = True
                    if u_id in react['u_ids']:
                        raise InputError("Message already contains an active react from the user")
                    react['u_ids'].append(u_id)
                    if message['u_id'] == u_id:
                        react['is_this_user_reacted'] = True

            if not react_exists:
                react_dict = {
                    'react_id': react_id,
                    'u_ids': [],
                    'is_this_user_reacted': False
                }
                if message['u_id'] == u_id:
                    react_dict['is_this_user_reacted'] = True
                react_dict['u_ids'].append(u_id)
                message['reacts'].append(react_dict)
    return {}

def message_unreact(token, message_id, react_id):
    '''
    Takes in token, message_id, and react_id to to remove a react to the message
    with message_id from the user given by the token
    '''
    # invalid token
    u_id = u_id_finder(token, data)

    # invalid message_id
    channel_id = message_id_in_which_channel(message_id, data)
    valid_message_id = is_user_in_channel(channel_id, u_id, data)

    if not valid_message_id:
        raise InputError("Message is not in a channel that the user is in.")

    # invalid react_id
    if react_id != 1:
        raise InputError("Invalid react id")

    # message with message_id does not contain an active react from the user
    for message in data['channels'][channel_id]['messages']:
        if message['message_id'] == message_id:
            if message['reacts'] == []:
                raise InputError("Message does not contain an active react from the user")
            for react in message['reacts']:
                if react['react_id'] == react_id:
                    if u_id in react['u_ids']:
                        react['u_ids'].remove(u_id)
                    else:
                        raise InputError("Message does not contain an active react from the user")
                    if message['u_id'] == u_id:
                        react['is_this_user_reacted'] = False
    return {}

def message_pin(token, message_id):
    '''
    Takes in token and message_id to pin a message with message_id by the user given by the token
    '''
    # invalid token
    u_id = u_id_finder(token, data)

    # check whether user is an owner of the channel
    channel_id = message_id_in_which_channel(message_id, data)
    is_user_owner = channel_has_owner_permissions(channel_id, u_id, data)

    # check whether user is a member of the channel
    if not is_user_owner:
        raise AccessError("User has no permissions to pin message")

    # invalid message_id
    valid_message_id = is_user_in_channel(channel_id, u_id, data)

    if not valid_message_id:
        raise InputError("Message is not in a channel that the user is in.")

    # check whether the message with message_id is already pinned or not
    for message in data['channels'][channel_id]['messages']:
        if message['message_id'] == message_id:
            if message['is_pinned']:
                raise InputError("Message is already pinned")
            message['is_pinned'] = True
    return {}

def message_unpin(token, message_id):
    '''
    Takes in token and message_id to unpin a message with message_id by the user given by the token
    '''
    # invalid token
    u_id = u_id_finder(token, data)

    # check whether user is an owner of the channel
    channel_id = message_id_in_which_channel(message_id, data)
    is_user_owner = channel_has_owner_permissions(channel_id, u_id, data)

    # check whether user is a member of the channel IF user is not an owner of the channel
    if not is_user_owner:
        raise AccessError("User has no permissions to unpin message")

    # invalid message_id
    valid_message_id = is_user_in_channel(channel_id, u_id, data)

    if not valid_message_id:
        raise InputError("Message is not in a channel that the user is in.")

    # check whether the message with message_id is already unpinned or not
    for message in data['channels'][channel_id]['messages']:
        if message['message_id'] == message_id:
            if not message['is_pinned']:
                raise InputError("Message is already unpinned")
            message['is_pinned'] = False
    return {}
