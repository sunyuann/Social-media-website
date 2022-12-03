'''no other external modules were used'''
from data import data
from error import InputError, AccessError
from helper_functions import channel_is_member, channel_has_owner_permissions
from helper_functions import u_id_finder, valid_user_id, valid_channel


def channel_invite(token, channel_id, u_id):
    '''
    Given a valid token, the user with u_id is invited to join channel with
    channel_id
    '''
    # catching InputErrors
    if not valid_channel(channel_id, data):
        raise InputError("Invalid channel ID entered")
    if not valid_user_id(u_id, data):
        raise InputError("Invalid user ID entered")

    # using helper function to find u_id from token, raises InputError if token is invalid
    u_id_inviter = u_id_finder(token, data)

    # checking if u_id_inviter is a member of the channel with helper_function
    is_member = channel_is_member(channel_id, u_id_inviter, data)
    if not is_member:
        raise AccessError("User is not a member of this channel")

    # checking if u_id_invitee is already a member
    is_member = channel_is_member(channel_id, u_id, data)
    if is_member:
        raise AccessError("User is already a member of this channel")

    # adding user_details into channel 'all_members' data
    user_detail = {
        'u_id': u_id,
        'name_first': data['users'][u_id]['name_first'],
        'name_last': data['users'][u_id]['name_last']
    }
    if 'profile_img_url' in data['users'][u_id]:
        user_detail['profile_img_url'] = data['users'][u_id]['profile_img_url']
    data['channels'][channel_id]['all_members'].append(user_detail)
    # if u_id is a global owner, becomes a local owner as well
    if data['users'][u_id]['permission_id'] == 1:
        if user_detail not in data['channels'][channel_id]['owner_members']:
            data['channels'][channel_id]['owner_members'].append(user_detail)

    # adding channel_details into user 'channel_membership' data
    channel_detail = {
        'channel_id': channel_id,
        'name': data['channels'][channel_id]['name']
    }
    data['users'][u_id]['channel_membership'].append(channel_detail)

    return {
    }

def channel_details(token, channel_id):
    '''
    Given a channel with the channel_id that a user with the token is a part
    of, provide basic details about the channel
    '''
    # catching InputError
    if not valid_channel(channel_id, data):
        raise InputError("Invalid channel ID entered")

    # using helper function to find u_id from token, raises InputError if token is invalid
    u_id = u_id_finder(token, data)

    # checking if u_id is a member of the channel with helper_function
    is_member = channel_is_member(channel_id, u_id, data)
    if not is_member:
        raise AccessError("User is not a member of this channel")

    # creating returned dictionary
    channel_name = data['channels'][channel_id]['name']
    owner_members = data['channels'][channel_id]['owner_members']
    all_members = data['channels'][channel_id]['all_members']
    return {
        'name': channel_name,
        'owner_members': owner_members,
        'all_members': all_members,
    }

def channel_messages(token, channel_id, start):
    '''
    Given a channel with the channel_id that the user with the token is a part
    of, return up to 50 messages bewtween index start and start + 50. Message
    with index 0 is the most recent message in the channel. This function
    returns a new index "end" which is the value of "start + 50", or, if this
    function has returned the least recent messages in the channel, returns -1
    in "end" to indicate there are no more messages to load after this return.
    '''
    # catching InputError
    if not valid_channel(channel_id, data):
        raise InputError("Invalid channel ID entered")

    # using helper function to find u_id from token, raises InputError if token is invalid
    u_id = u_id_finder(token, data)

    # checking if u_id is a member of the channel with helper_function
    is_member = channel_is_member(channel_id, u_id, data)
    if not is_member:
        raise AccessError("User is not a member of this channel")

    # accessing message from channel data
    for message in data['channels'][channel_id]['messages']:
        for react in message['reacts']:
            if u_id in react['u_ids']:
                react['is_this_user_reacted'] = True
            else:
                react['is_this_user_reacted'] = False
    message_list = data['channels'][channel_id]['messages']

    oldest_message = len(message_list) - 1

    if len(message_list) == 0:
        oldest_message = 0

    # catching InputError
    if start > oldest_message:
        raise InputError("Start is greater than the total number of messages in this channel")

    # creating message list and returned dictionary
    end_point = start + 49
    end_value = start + 50
    if end_point >= oldest_message:
        end_point = oldest_message + 1
        end_value = -1
    return_val = {
        'messages': message_list[start:end_point],
        'start': start,
        'end': end_value,
    }
    return return_val

def channel_leave(token, channel_id):
    '''
    Given a channel with the channel_id, user with the token is removed as a
    member of this channel
    '''
    # catching InputError
    if not valid_channel(channel_id, data):
        raise InputError("Invalid channel ID entered")

    # using helper function to find u_id from token, raises InputError if token is invalid
    u_id = u_id_finder(token, data)

    # checking if u_id is a member of the channel with helper_function
    is_member = channel_is_member(channel_id, u_id, data)
    if not is_member:
        raise AccessError("User is not a member of this channel")

    # removing channel_detail from user 'channel_membership' data
    channel_detail = {
        'channel_id': channel_id,
        'name': data['channels'][channel_id]['name']
    }
    data['users'][u_id]['channel_membership'].remove(channel_detail)

    # removing user_detail from channel 'all_members' data
    user_detail = user_detail = {
        'u_id': u_id,
        'name_first': data['users'][u_id]['name_first'],
        'name_last': data['users'][u_id]['name_last']
    }
    if 'profile_img_url' in data['users'][u_id]:
        user_detail['profile_img_url'] = data['users'][u_id]['profile_img_url']
    data['channels'][channel_id]['all_members'].remove(user_detail)

    # by the assumption we made, owners who leave the channel have their
    # 'owner' status taken away
    if user_detail in data['channels'][channel_id]['owner_members']:
        data['channels'][channel_id]['owner_members'].remove(user_detail)
    return {
    }

def channel_join(token, channel_id):
    '''
    Given a channel with the channel_id that the user with the token can join,
    the user is added to the channel
    '''
    # catching InputError
    if not valid_channel(channel_id, data):
        raise InputError("Invalid channel ID entered")

    # using helper function to find u_id from token, raises InputError if token is invalid
    u_id = u_id_finder(token, data)

    # raises AccessError if user is already a member of said channel
    is_member = channel_is_member(channel_id, u_id, data)
    if is_member:
        raise AccessError("User is already a member of this channel")

    is_owner = False
    # if user has a permisssion_id of an owner, user can join private channels
    if data['users'][u_id]['permission_id'] == 1:
        is_owner = True

    # catching AccessError
    if not data['channels'][channel_id]['is_public'] and not is_owner:
        raise AccessError("Channel is not public")

    # creating user_detail dict and adding it into channel 'all_members' data
    user_detail = {
        'u_id': u_id,
        'name_first': data['users'][u_id]['name_first'],
        'name_last': data['users'][u_id]['name_last']
    }
    if 'profile_img_url' in data['users'][u_id]:
        user_detail['profile_img_url'] = data['users'][u_id]['profile_img_url']
    data['channels'][channel_id]['all_members'].append(user_detail)
    # if u_id is a global owner, becomes a local owner as well
    if data['users'][u_id]['permission_id'] == 1:
        if user_detail not in data['channels'][channel_id]['owner_members']:
            data['channels'][channel_id]['owner_members'].append(user_detail)

    # creating channel_detail dict and adding it into user 'channel_membership' data
    channel_detail = {
        'channel_id': channel_id,
        'name': data['channels'][channel_id]['name']
    }
    data['users'][u_id]['channel_membership'].append(channel_detail)

    return {
    }

def channel_addowner(token, channel_id, u_id):
    '''
    Makes the user with the user_id an owner of the channel with channel_id
    '''
    # catching invalid channel_id
    if not valid_channel(channel_id, data):
        raise InputError("Invalid channel ID entered")

    # using helper function to find u_id from token, raises InputError if token is invalid
    u_id_inviter = u_id_finder(token, data)

    # catching errors to do with ownership
    # checking for owner permissions of inviter
    is_owner = channel_has_owner_permissions(channel_id, u_id_inviter, data)
    if not is_owner:
        raise AccessError("Given token is not an owner of the channel")

    # checking whether u_id is already an owner
    for member in data['channels'][channel_id]['owner_members']:
        if member['u_id'] == u_id:
            raise InputError('User is already an owner of this channel')

    # catching invalid u_id
    if not valid_user_id(u_id, data):
        raise InputError("Invalid user ID entered")

    # checking if u_id is a member of the channel with helper_function
    is_member = channel_is_member(channel_id, u_id, data)
    if not is_member:
        raise InputError("User is not a member of this channel")

    # creating owner_detail dict and adding it into channel "owner_members" data
    owner_detail = {
        'u_id': u_id,
        'name_first': data['users'][u_id]['name_first'],
        'name_last': data['users'][u_id]['name_last']
    }
    if 'profile_img_url' in data['users'][u_id]:
        owner_detail['profile_img_url'] = data['users'][u_id]['profile_img_url']
    data['channels'][channel_id]['owner_members'].append(owner_detail)

    return {
    }

def channel_removeowner(token, channel_id, u_id):
    '''
    Removes the user with the user_id as an owner of the channel with
    channel_id
    '''
    # catching InputError
    if not valid_channel(channel_id, data):
        raise InputError("Invalid channel ID entered")

    # using helper function to find u_id from token, raises InputError if token is invalid
    u_id_inviter = u_id_finder(token, data)

    # checking if user has owner permissions on this channel
    is_owner = channel_has_owner_permissions(channel_id, u_id_inviter, data)
    if not is_owner:
        raise AccessError("Given token is not an owner of the channel")

    # catching invalid u_id
    if not valid_user_id(u_id, data):
        raise InputError("Invalid user ID entered")

    # catching InputError
    is_owner = False
    for member in data['channels'][channel_id]['owner_members']:
        if member['u_id'] == u_id:
            is_owner = True
    if not is_owner:
        raise InputError('User is not an owner of this channel')

    # creating owner_detail dict and removing it from channel 'owner_members' data
    owner_detail = {
        'u_id': u_id,
        'name_first': data['users'][u_id]['name_first'],
        'name_last': data['users'][u_id]['name_last']
    }
    if 'profile_img_url' in data['users'][u_id]:
        owner_detail['profile_img_url'] = data['users'][u_id]['profile_img_url']
    data['channels'][channel_id]['owner_members'].remove(owner_detail)

    return {

    }
