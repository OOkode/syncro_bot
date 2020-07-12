from telethon import TelegramClient, events, sync
import env

PERMITTED_USERS = ['ChelpBots']

channel = -1001360204322
group = 'tuenvio_granma'
log_channel = -1001394912157

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

def purge_unwanted_users(client,channel,group,log_channel):

    try:

        users_to_be_kicked_from_channel = get_users_not_in_group(client,channel,group)
        users_to_be_kicked_from_group = get_users_without_username(client,group)

        for user in users_to_be_kicked_from_group:
            client.kick_participant(entity=group,user=user)
            client.send_message(entity=log_channel,message= f'Kicked {user.id if not user.username else user.username} for not having username')

        for user in users_to_be_kicked_from_channel:
            client.kick_participant(entity=group,user=user)
            client.send_message(entity=log_channel,message= f'Kicked {user.id if not user.username else user.username} for not subscribing to the group')
            

    except ValueError as e:
        raise e

api_id = env.API_ID
api_hash = env.API_HASH

client = TelegramClient('session1', api_id, api_hash)
client.start(phone=env.PHONE,password=env.PASSWORD)

client.start()

purge_unwanted_users(client,channel,group,log_channel)


