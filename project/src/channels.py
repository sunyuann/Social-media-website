'''no other external modules were used'''
from data import data
from error import InputError, AccessError
from helper_functions import u_id_finder

def channels_list(token):
    '''
    Provide a list of all channels (and their associated details) that the
    authorised user is part of
    Returns a list of channels
    '''
    is_part_of = []
    for user in data['users']:
        if 'token' in data['users'][user]:
            if data['users'][user]['token'] == token:
                u_id = user
                is_part_of = data['users'][user]['channel_membership']
    try:
        data['users'][u_id]
    except:
        raise AccessError("Invalid token entered")

    return {
        'channels': is_part_of
    }

def channels_listall(token):
    '''
    Provide a list of all channels (and their associated details)
    Returns a list of channels
    '''
    # using helper function to raise InputError if token is invalid
    u_id_finder(token, data)

    all_channels = []
    for channels in data['channels']:
        channel_data = {}
        #extract name and channel id for each channels_list
        channel_data['channel_id'] = data['channels'][channels]['channel_id']
        channel_data['name'] = data['channels'][channels]['name']
        all_channels.append(channel_data)

    return {
        'channels': all_channels
    }

def channels_create(token, name, is_public):
    '''
    Creates a new channel with that name that is either a public or private
    channel
    returns a channel_id (integer)
    '''
    channel_id = len(data["channels"]) + 1
    # raising InputError
    if len(name) == 0:
        raise InputError("Channel name cannot be empty")
    if len(name) > 20:
        raise InputError("Channel name is too long")

    # using helper function to find u_id from token, raises InputError if token is invalid
    u_id = u_id_finder(token, data)

    # creating channel dict for data
    data["channels"][channel_id] = {
        "name": name,
        "creator": token,
        "is_public": is_public,
        "channel_id": channel_id,
        "owner_members": [],
        "all_members": [],
        "messages": [],
    }

    owner_detail = {
        'u_id': u_id,
        'name_first': data['users'][u_id]['name_first'],
        'name_last': data['users'][u_id]['name_last']
    }
    if 'profile_img_url' in data['users'][u_id]:
        owner_detail['profile_img_url'] = data['users'][u_id]['profile_img_url']
    # adds channel creator as a member
    data['channels'][channel_id]['all_members'].append(owner_detail)
    channel_detail = {
        'channel_id': channel_id,
        'name': data['channels'][channel_id]['name']
    }
    data['users'][u_id]['channel_membership'].append(channel_detail)
    # adds channel creator as an owner
    data['channels'][channel_id]['owner_members'].append(owner_detail)

    return {
        "channel_id": channel_id
    }
