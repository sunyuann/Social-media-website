'''
error imported to check for InputErrors and AccessErrors
data imported for clear function
datetime is used for finding the unix timestamps and finding the current time in standups
threading is used for the buffering of standups
'''
from datetime import datetime, timezone
import threading
from error import InputError, AccessError
from data import data
from helper_functions import u_id_finder, valid_channel, channel_is_member
from helper_functions import valid_user_id, standup_end
from user import user_profile

def clear():
    '''
    Clears all data from data.py (global variables)
    Used for tests
    Resets the internal data of the application to its initial state
    '''
    data['users'].clear()
    data['channels'].clear()
    data['msg_later_list'].clear()
    return {}

def users_all(token):
    '''
    The users_all function takes in the parameter token. An InputError is
    raised when there is an invalid token. Returns a dictionary containing the
    key 'users' which leads to a list of all users and their associated
    details. This includes the user's user_id, email, first name, last name
    and handle
    '''
    users_l = []
    valid_token = False
    # looping through users and adding details to users list
    for user in data['users']:
        user_detail = {
            'u_id': data['users'][user]['u_id'],
            'email': data['users'][user]['email'],
            'name_first': data['users'][user]['name_first'],
            'name_last': data['users'][user]['name_last'],
            'handle_str': data['users'][user]['handle_str']
        }
        if 'profile_img_url' in data['users'][user]:
            user_detail['profile_img_url'] = data['users'][user]['profile_img_url']
        users_l.append(user_detail)

        # checking for valid input token
        if 'token' in data['users'][user]:
            if data['users'][user]['token'] == token:
                valid_token = True

    if not valid_token:
        raise InputError('Invalid token entered')

    return {
        'users' : users_l
    }

def admin_userpermission_change(token, u_id, permission_id):
    '''
    This function takes in a token, who is a global owner, and sets the permission_id
    of the user with the u_id given
    '''
    # function to check for valid u_id
    if not valid_user_id(u_id, data):
        raise InputError("Invalid user ID entered")

    # using helper function to find u_id from token, raises InputError if token is invalid
    admin = u_id_finder(token, data)

    # checking for owner permissions
    if data['users'][admin]['permission_id'] == 2:
        raise AccessError("Unauthorized user cannot change other's permissions")
    if permission_id == 1 and data['users'][u_id]['permission_id'] == 1:
        raise InputError("User is already an owner of flockr")
    if permission_id == 2 and data['users'][u_id]['permission_id'] == 2:
        raise InputError("User is already a member of flockr")

    # checking for valid permission_id
    if permission_id not in (2, 1):
        raise InputError("Permission_id does not refer to a valid permission")

    data['users'][u_id]['permission_id'] = permission_id
    return {}

def search(token, query_str):
    '''
    Search function takes in 2 parameters, token and query_str, which then
    returns a collection of messages in all of the channels that the user
    has joined that match the query
    '''
    # using helper function to find u_id from token, raises InputError if token is invalid
    u_id = u_id_finder(token, data)

    matching_messages = []
    #Find the channels that user is a part of
    for channels in data['users'][u_id]['channel_membership']:
        channel_id = channels['channel_id']
    #Loop through the messages of every channel and see if we have a match
        for messages in data['channels'][channel_id]['messages']:
            if query_str == messages['message']:
                matching_messages.append(messages)
    return {'messages' : matching_messages}

def standup_start(token, channel_id, length):
    '''
    Standup start function takes in 3 parameters,token, channel_id and length
    In a channel this will start standup stage for length seconds if someone
    call this function. It is buffered during the X second window then at the
    end of the X second window a message will be added to the message queue
    in the channel from the user who started the standup. X is an integer that
    denotes the number of seconds that the standup occurs for.
    '''
    #using helper_function, find u_id from token
    uid = u_id_finder(token, data)

    #check channel id
    if not valid_channel(channel_id, data):
        raise InputError("This is not a valid channel.")

    #check whether user is a member of the channel that the message is within
    if not channel_is_member(channel_id, uid, data):
        raise AccessError("User is not a member of the channel that the message is within.")

    if length < 0:
        raise InputError("Standup cannot be started with invalid length")

    #check it is active
    if standup_active(token, channel_id)['is_active']:
        raise InputError("A standup is running in this channel.")

    time_finish = datetime.now(timezone.utc).timestamp() + length
    data['channels'][channel_id]['standup'] = {
        'messages': [],
        'time_finish': time_finish
    }

    total_messages = 0
    for channels in data['channels']:
        total_messages += len(data['msg_later_list']) + len(data['channels'][channels]['messages'])
        if channels == channel_id:
            msg_id = total_messages + 1

    time = threading.Timer(length, standup_end, [channel_id, token, msg_id, data])
    time.start()
    return {
        'time_finish': time_finish
    }

def standup_active(token, channel_id):
    '''
    Standup active function takes in 2 parameters,token, channel_id.
    In a channel this will check whether there is a standup running in this channel.
    '''
    #check for valid token with u_id finder
    u_id = u_id_finder(token, data)

    #check channel id
    if not valid_channel(channel_id, data):
        raise InputError("This is not a valid channel")

    #check if token is a member of channel
    if not channel_is_member(channel_id, u_id, data):
        raise AccessError("User is not a member of channel")

    #check if there is an active standup
    if 'standup' in data['channels'][channel_id]:
        is_active = True
        time_finish = data['channels'][channel_id]['standup']['time_finish']
    else:
        is_active = False
        time_finish = None
    return {
        'is_active': is_active,
        'time_finish': time_finish
    }

def standup_send(token, channel_id, message):
    '''
    Standup send function takes in 3 parameters,token, channel_id and message.
    Sending a message to get buffered in the standup queue.
    '''
    u_id = u_id_finder(token, data)
    #check channel id
    if not valid_channel(channel_id, data):
        raise InputError("This is not a valid channel.")

    #check whether user is a member of the channel that the message is within
    if not channel_is_member(channel_id, u_id, data):
        raise AccessError("User is not a member of the channel that the message is within.")

    #check message length
    if len(message) > 1000:
        raise InputError("The message can not be more than 1000 characters.")

    #check standup is active
    if not standup_active(token, channel_id)['is_active']:
        raise InputError("This channel is not running a standup now.")

    user = user_profile(token, u_id)
    standup_msg = f"{user['user']['handle_str']}: " + message
    data['channels'][channel_id]['standup']['messages'].append(standup_msg)

    return {

    }
