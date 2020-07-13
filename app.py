from telethon import TelegramClient, events, sync
import env

PERMITTED_USERS = ['ChelpBots']

channels = {'Granma':-1001360204322,'Pinar': 'AlertaTuenvioPinar'}
groups = {'Granma': 'tuenviogranma','Pinar':'TuenvioPinardelRio'}
log_channels = {'Granma':-1001394912157,'Pinar':'logpinardelrio'}


channel = channels['Pinar']
group = groups['Pinar']
log_channel = log_channels['Pinar']

def get_api_credentials():
    return (env.API_ID,env.API_HASH)


def get_users_not_in_group(client,channel,group):

    global PERMITTED_USERS
    UNWANTED_USERS = []

    group_users = client.get_participants(group)
    channel_users = client.get_participants(channel)

    for user in channel_users:
        if (user.username not in PERMITTED_USERS) and ( not user.bot ) and (user not in group_users):
            print(user.username or user.id)
            UNWANTED_USERS.append(user)

    return UNWANTED_USERS

def get_users_without_username(client,group):

    UNWANTED_USERS = []

    group_users = client.get_participants(group)

    for user in group_users:
        if not user.username:
            UNWANTED_USERS.append(user)

    
    return UNWANTED_USERS

def get_users_in_forbidden_groups(client,forbidden_groups):

    UNWANTED_USERS = []

    for group in forbidden_groups:
        for user in client.get_participants(group):
            UNWANTED_USERS.append(user)

    return UNWANTED_USERS            

def purge_unwanted_users(client,channel,group,log_channel,forbidden_groups):

    group_users = client.get_participants(group)

    try:

        users_to_be_kicked_from_channel = get_users_not_in_group(client,channel,group)
        users_to_be_kicked_from_group = get_users_without_username(client,group)
        users_in_forbidden_groups = get_users_in_forbidden_groups(client,forbidden_groups)

        for user in users_to_be_kicked_from_group:
            client.kick_participant(entity=group,user=user)
            username = ('@' + user.username) if user.username else ''
            client.send_message(entity=log_channel,message= f'Kicked {user.id if not user.username else username} for not having username')

        for user in users_to_be_kicked_from_channel:
            client.kick_participant(entity=group,user=user)
            username = ('@' + user.username) if user.username else ''
            client.send_message(entity=log_channel,message= f'Kicked {user.id if not user.username else username} for not subscribing to the group')

        # for user in users_to_be_kicked_from_channel:
        #     client.edit_permissions(channel, user, view_messages=False)
        #     username = ('@' + user.username) if user.username else ''
        #     client.send_message(entity=log_channel,message= f'Banned {user.id if not user.username else username} for not subscribing to the group')


        for user in users_in_forbidden_groups:
            if user in group_users:
                client.edit_permissions(channel, user, view_messages=False)
                client.edit_permissions(group, user, view_messages=False)
                username = ('@' + user.username) if user.username else ''
                client.send_message(entity=log_channel,message= f'Banned {user.id if not user.username else username} for belonging to forbidden group')
            

    except ValueError as e:
        raise e


api_id, api_hash = get_api_credentials()

client = TelegramClient('session1', api_id, api_hash)
client.start(phone=env.PHONE,password=env.PASSWORD)

purge_unwanted_users(client,channel,group,log_channel,['tuenviopinargrupo'])


