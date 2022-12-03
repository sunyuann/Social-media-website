'''
file to store global variables (in data variable)
'''

global data
data = {
    'users': {},
    'channels': {},
    'msg_later_list': []
}

'''
Note on usage:

- Format:

data['users'][u_id] = {
        'email': email,
        'password' : password,
        'name_first' : name_first,
        'name_last' : name_last,
        'u_id' : u_id,
        'token' : str(token),
        'handle' : handle,
        'channel_membership': []
    }

e.g data['users'][u_id]['token'] would give access to token value

data['channels'][channel_id] = {
        "name": name,
        "owner": token,
        "is_public": True,
        "channel_id": channel_id,
        "owner_members": [],
        "all_members": [],
        "messages": []
    }

- u_id and channel_id start from 0 and it increases
'''
