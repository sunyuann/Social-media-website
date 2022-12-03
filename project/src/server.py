'''
re module is used to substitute and cut off end of base url
dumps from json module is used as a format of returning values in flask
flask module is used to run app (flask server)
all functions from all files are imported into here for flask implementation
'''
import re
from json import dumps
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from auth import auth_register, auth_login, auth_logout
from auth import auth_passwordreset_request, auth_passwordreset_reset
from user import user_profile, user_profile_setname, user_profile_setemail, user_profile_sethandle
from user import user_profile_uploadphoto
from channel import channel_invite, channel_details, channel_messages
from channel import channel_leave, channel_join, channel_addowner, channel_removeowner
from channels import channels_list, channels_listall, channels_create
from message import message_send, message_edit, message_remove, message_sendlater
from message import message_react, message_unreact, message_pin, message_unpin
from other import clear, users_all, admin_userpermission_change, search
from other import standup_send, standup_start, standup_active
from error import InputError

def default_handler(err):
    '''
    handler to catch errors (e.g. InputErrors, AccessErrors)
    '''
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, default_handler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    '''
    example flask implementation
    '''
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

# routes are written here
# auth functions
@APP.route('/auth/login', methods=['POST'])
def auth_login_http():
    '''
    auth_login_http function based on auth_login function
    '''
    payload = request.get_json()
    email = payload['email']
    password = payload['password']
    user_details = auth_login(email, password)
    return dumps(user_details)

@APP.route('/auth/logout', methods=['POST'])
def auth_logout_http():
    '''
    auth_logout_http function based on auth_logout function
    '''
    payload = request.get_json()
    token = payload['token']
    is_success = auth_logout(token)
    return dumps(is_success)

@APP.route('/auth/register', methods=['POST'])
def auth_register_http():
    '''
    auth_register_http function based on auth_register function
    '''
    payload = request.get_json()
    email = payload['email']
    password = payload['password']
    name_first = payload['name_first']
    name_last = payload['name_last']
    user_details = auth_register(email, password, name_first, name_last)
    return dumps(user_details)

@APP.route('/auth/passwordreset/request', methods=['POST'])
def auth_passwordreset_request_http():
    '''
    auth_passwordreset_request_http function based on auth_passwordreset_request function
    '''
    payload = request.get_json()
    email = payload['email']
    return_val = auth_passwordreset_request(email)
    return dumps(return_val)

@APP.route('/auth/passwordreset/reset', methods=['POST'])
def auth_passwordreset_reset_http():
    '''
    auth_passwordreset_reset_http function based on auth_passwordreset_reset function
    '''
    payload = request.get_json()
    reset_code = payload['reset_code']
    new_password = payload['new_password']
    return_val = auth_passwordreset_reset(reset_code, new_password)
    return dumps(return_val)

# channel functions
@APP.route('/channel/invite', methods=['POST'])
def channel_invite_http():
    '''
    channel_invite_http function based on channel_invite function
    '''
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    u_id = payload['u_id']
    result = channel_invite(token, channel_id, u_id)
    return dumps(result)

@APP.route('/channel/details', methods=['GET'])
def channel_details_http():
    '''
    channel_details_http function based on channel_details function
    '''
    payload = request.args
    token = payload['token']
    channel_id = int(payload['channel_id'])
    result = channel_details(token, channel_id)
    return dumps(result)

@APP.route('/channel/messages', methods=['GET'])
def channel_messages_http():
    '''
    channel_messages_http function based on channel_messages function
    '''
    payload = request.args
    token = payload['token']
    channel_id = int(payload['channel_id'])
    start = int(payload['start'])
    result = channel_messages(token, channel_id, start)
    return dumps(result)

@APP.route('/channel/leave', methods=['POST'])
def channel_leave_http():
    '''
    channel_leave_http function based on channel_leave function
    '''
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    result = channel_leave(token, channel_id)
    return dumps(result)

@APP.route('/channel/join', methods=['POST'])
def channel_join_http():
    '''
    channel_join_http function based on channel_join function
    '''
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    result = channel_join(token, channel_id)
    return dumps(result)

@APP.route('/channel/addowner', methods=['POST'])
def channel_addowner_http():
    '''
    channel_addowner_http function based on channel_addowner function
    '''
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    u_id = payload['u_id']
    result = channel_addowner(token, channel_id, u_id)
    return dumps(result)

@APP.route('/channel/removeowner', methods=['POST'])
def channel_removeowner_http():
    '''
    channel_removeowner_http function based on channel_removeowner function
    '''
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    u_id = payload['u_id']
    result = channel_removeowner(token, channel_id, u_id)
    return dumps(result)

# channels functions
@APP.route('/channels/list', methods=['GET'])
def channels_list_http():
    '''
    channels_list_http function based on channels_list function
    '''
    payload = request.args
    token = payload['token']
    result = channels_list(token)
    return dumps(result)

@APP.route('/channels/listall', methods=['GET'])
def channels_listall_http():
    '''
    channels_listall function based on channels_listall function
    '''
    payload = request.args
    token = payload['token']
    result = channels_listall(token)
    return dumps(result)

@APP.route('/channels/create', methods=['POST'])
def channels_create_http():
    '''
    channels_create_http function based on channels_create function
    '''
    payload = request.get_json()
    token = payload['token']
    name = payload['name']
    is_public = payload['is_public']
    result = channels_create(token, name, is_public)
    return dumps(result)

# user functions
@APP.route('/user/profile', methods=['GET'])
def user_profile_http():
    '''
    user_profile_http function based on user_profile function
    '''
    payload = request.args
    token = payload['token']
    u_id = int(payload['u_id'])
    user = user_profile(token, u_id)
    return dumps(user)

@APP.route('/user/profile/setname', methods=['PUT'])
def user_profile_setname_http():
    '''
    user_profile_setname_http function based on user_profile_setname function
    '''
    payload = request.get_json()
    token = payload['token']
    name_first = payload['name_first']
    name_last = payload['name_last']
    user = user_profile_setname(token, name_first, name_last)
    return dumps(user)

@APP.route('/user/profile/setemail', methods=['PUT'])
def user_profile_setemail_http():
    '''
    user_profile_setemail_http function based on user_profile_setemail function
    '''
    payload = request.get_json()
    token = payload['token']
    email = payload['email']
    user = user_profile_setemail(token, email)
    return dumps(user)

@APP.route('/user/profile/sethandle', methods=['PUT'])
def user_profile_sethandle_http():
    '''
    user_profile_sethandle_http function based on user_profile_sethandle
    function
    '''
    payload = request.get_json()
    token = payload['token']
    handle_str = payload['handle_str']
    user = user_profile_sethandle(token, handle_str)
    return dumps(user)

@APP.route('/user/profile/uploadphoto', methods=['POST'])
def user_profile_uploadphoto_http():
    '''
    user_profile_uploadphoto_http function based on user_profile_uploadphoto
    function (takes in 6 parameters)
    (token, img_url, x_start, y_start, x_end, y_end)
    '''
    payload = request.get_json()
    token = payload['token']
    img_url = payload['img_url']
    x_start = payload['x_start']
    y_start = payload['y_start']
    x_end = payload['x_end']
    y_end = payload['y_end']
    base_url = request.base_url
    base_url = re.sub('/user/profile/uploadphoto', '', base_url)
    return_val = user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end, base_url)
    return dumps(return_val)

@APP.route("/imgurl/<filename>", methods=["GET"])
def profile_img_url(filename):
    '''
    profile_img_url function returns a url that opens the cropped uploaded image
    '''
    return send_from_directory('../static', filename)

# message functions
@APP.route('/message/send', methods=['POST'])
def message_send_http():
    '''
    message_send_http function based on message_send function
    '''
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    message = payload['message']
    result = message_send(token, channel_id, message)
    return dumps(result)

@APP.route('/message/remove', methods=['DELETE'])
def message_remove_http():
    '''
    message_remove_http function based on message_remove function
    '''
    payload = request.get_json()
    token = payload['token']
    message_id = payload['message_id']
    result = message_remove(token, message_id)
    return dumps(result)

@APP.route('/message/edit', methods=['PUT'])
def message_edit_http():
    '''
    message_edit_http function based on message_edit function
    '''
    payload = request.get_json()
    token = payload['token']
    message_id = payload['message_id']
    new_message = payload['message']
    result = message_edit(token, message_id, new_message)
    return dumps(result)

@APP.route('/message/sendlater', methods=['POST'])
def message_sendlater_http():
    '''
    message_sendlater_http function based on message_sendlater function
    '''
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    message = payload['message']
    time_sent = payload['time_sent']
    result = message_sendlater(token, channel_id, message, time_sent)
    return dumps(result)

@APP.route('/message/react', methods=['POST'])
def message_react_http():
    '''
    message_react_http function based on message_react function
    '''
    payload = request.get_json()
    token = payload['token']
    message_id = payload['message_id']
    react_id = payload['react_id']
    result = message_react(token, message_id, react_id)
    return dumps(result)

@APP.route('/message/unreact', methods=['POST'])
def message_unreact_http():
    '''
    message_unreact_http function based on message_unreact function
    '''
    payload = request.get_json()
    token = payload['token']
    message_id = payload['message_id']
    react_id = payload['react_id']
    result = message_unreact(token, message_id, react_id)
    return dumps(result)

@APP.route('/message/pin', methods=['POST'])
def message_pin_http():
    '''
    message_pin_http function based on message_pin function
    '''
    payload = request.get_json()
    token = payload['token']
    message_id = payload['message_id']
    result = message_pin(token, message_id)
    return dumps(result)

@APP.route('/message/unpin', methods=['POST'])
def message_unpin_http():
    '''
    message_unpin_http function based on message_unpin function
    '''
    payload = request.get_json()
    token = payload['token']
    message_id = payload['message_id']
    result = message_unpin(token, message_id)
    return dumps(result)

# other functions
@APP.route('/users/all', methods=['GET'])
def users_all_http():
    '''
    users_all_http function based on users_all function
    '''
    payload = request.args
    token = payload['token']
    user = users_all(token)
    return dumps(user)

@APP.route('/admin/userpermission/change', methods=['POST'])
def admin_userpermission_change_http():
    '''
    admin_userpermission_change_http function based on
    admin_userpermission_change function
    '''
    payload = request.get_json()
    token = payload['token']
    u_id = payload['u_id']
    permission_id = payload['permission_id']
    result = admin_userpermission_change(token, u_id, permission_id)
    return dumps(result)

@APP.route('/search', methods=['GET'])
def search_http():
    '''
    search_http function based on search function
    '''
    payload = request.args
    token = payload['token']
    query_str = payload['query_str']
    result = search(token, query_str)
    return dumps(result)

@APP.route('/clear', methods=['DELETE'])
def clear_http():
    '''
    clear_http function based on clear function
    '''
    clear_return_val = clear()
    return dumps(clear_return_val)

@APP.route('/standup/start', methods=['POST'])
def standup_start_http():
    '''
    standup_start_http function based on standup_start function
    '''
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    length = payload['length']
    result = standup_start(token, channel_id, length)
    return dumps(result)

@APP.route('/standup/active', methods=['GET'])
def standup_active_http():
    '''
    standup_active_http function based on standup_active function
    '''
    payload = request.args
    token = payload['token']
    channel_id = int(payload['channel_id'])
    result = standup_active(token, channel_id)
    return dumps(result)

@APP.route('/standup/send', methods=['POST'])
def standup_send_http():
    '''
    standup_send_http function based on standup_send function
    '''
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    message = payload['message']
    result = standup_send(token, channel_id, message)
    return dumps(result)

if __name__ == '__main__':
    APP.run(port=0)
