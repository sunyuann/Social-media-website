When a user logs in, a new token is generated for authentication purposes.
Therefore if a user who is already logged in tries to log in again, they will
get their token replaced by another number. Since the project specs do not cover this case, we are assuming that no error occurs, but their previous token is invalidated and can no longer be used

When a user's token is used to create a channel through channels_create, they
are immediately taken down as an owner of the channel

When an owner is removed from a channel through channel_leave, we assumed that
their 'owner' status is also taken away, since they are no longer a member.

A user being added through channel_addowner, has to be a member of the channel
initially. An inputerror is given otherwise. Therefore, all owners are always
members of the channel.

When a person is invited to a channel with 'is_public' set to False through
channel_invite, we assume that the invitee joins, as there is consent from the inviter

For auth_register function, if the handle created is already taken, underscores, '_' will be added to the handle until the length of the handle is 20. When the handle length reaches 20 characters, the last character will be replaced with alphabets. If all the last characters have been replaced by all alphabets, the last character will then be removed and the second last character will be replaced by all alphabets, and the cycle continues. We are assuming that there will not be that many users that could possibly use the same handle.

For auth_passwordreset_reset and auth_passwordreset_request, it is hard to obtain the reset code to change the password through the email for blackbox testing. Hence, we have decided to use manual testing instead and not implement blackbox testing due to the difficulty of obtaining the reset code. If the reset code could not be obtained, there is no way to test that auth_passwordreset_request will actually change the password. The only test we can do is test for InputErrors, which will be done. In doing this, the coverage will suffer as well. However, we will ensure that all functionalities of the function that are not covered via the pytests will be thoroughly covered through manual testing instead.

For user_profile_uploadphoto, it is hard to obtain the exact port (base URL) to set the profile_img_url, which is then used to test whether the image downloaded locally and then able to be viewed through a generated URL. Hence, we have decided to use manual testing instead and not implement blackbox testing due to the difficulty of comparing images, comparing the images from said URL. The only tests we can do is to thoroughly test for InputErrors, which can be done. In doing this, the coverage will suffer as not all lines of code are covered. However, we will ensure that all functionalities of the function that are not covered via the pytests will be thoroughly covered through manual testing instead.
