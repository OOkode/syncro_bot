from telethon import TelegramClient, events, sync
import env
import time, asyncio

ALLOWED_USERS = ['ChelpBots']

channels = {'Granma': -1001360204322, 'Pinar': 'AlertaTuenvioPinar'}
groups = {'Granma': 'tuenviogranma', 'Pinar': 'TuenvioPinardelRio'}
log_channels = {'Granma': -1001394912157, 'Pinar': 'logpinardelrio'}
forbidden_groups = ['tuenviopinargrupo', ]

CHANNEL = channels['Pinar']
GROUP = groups['Pinar']
LOG_CHANNEL = log_channels['Pinar']
action_counter = 0


def get_api_credentials():
    return env.API_ID, env.API_HASH


async def get_users_not_in_group(client, channel, group):
    print('---------- USUARIOS QUE NO ESTAN EN GRUPO ----------- \n')
    global ALLOWED_USERS
    UNWANTED_USERS = []

    group_users = await client.get_participants(entity=group, aggressive=True)
    channel_users = await client.get_participants(entity=channel, aggressive=True)

    for user in channel_users:
        if (user.username not in ALLOWED_USERS) and (not user.bot) and (not (user in group_users)):
            print(user.username or user.id)
            UNWANTED_USERS.append(user)

    print(len(UNWANTED_USERS))

    return UNWANTED_USERS


async def get_users_without_username(client, group):
    print('---------- USUARIOS SIN ALIAS -----------')

    UNWANTED_USERS = []

    group_users = await client.get_participants(entity=group, aggressive=True)

    for user in group_users:
        if not user.username:
            print(user.username or user.id)
            UNWANTED_USERS.append(user)

    print(len(UNWANTED_USERS))
    return UNWANTED_USERS


async def get_users_in_forbidden_groups(client, forbidden_groups):
    UNWANTED_USERS = []

    for group in forbidden_groups:
        users_in_forbidden_group = await client.get_participants(entity=group, aggressive=True)
        for user in users_in_forbidden_group:
            UNWANTED_USERS.append(user)

    print(f'Numero de usuarios en grupo prohibido: {len(UNWANTED_USERS)}')
    return UNWANTED_USERS


async def kick_from_channel(client, users_to_be_kicked_from_channel):
    global action_counter
    for user in users_to_be_kicked_from_channel:

        if action_counter > 80:
            action_counter = 0
            time.sleep(100)

        if not user.bot:
            await client.kick_participant(entity=CHANNEL, user=user)
            time.sleep(5)
            username = ('@' + user.username) if user.username else ''
            await client.send_message(entity=LOG_CHANNEL,
                                      message=f'Kicked {user.id if not user.username else username} for not subscribing to the group')
            action_counter += 2


async def ban_from_channel(client, users_to_be_banned_from_channel):
    global action_counter
    for user in users_to_be_banned_from_channel:
        if action_counter > 80:
            action_counter = 0
            time.sleep(100)

        if not user.bot:
            await client.edit_permissions(CHANNEL, user, view_messages=False)
            time.sleep(5)
            username = ('@' + user.username) if user.username else ''
            await client.send_message(entity=LOG_CHANNEL,
                                      message=f'Banned {user.id if not user.username else username} for not subscribing to the group')
            action_counter += 2


async def kick_from_group(client, users_to_be_kicked_from_group):
    global action_counter
    for user in users_to_be_kicked_from_group:

        if action_counter > 80:
            action_counter = 0
            time.sleep(100)

        await client.kick_participant(entity=GROUP, user=user)
        time.sleep(5)
        username = ('@' + user.username) if user.username else ''
        await client.send_message(entity=LOG_CHANNEL,
                                  message=f'Kicked {user.id if not user.username else username} for not having username')
        action_counter += 2


async def forbidden_group_ban(client, users_in_forbidden_groups):
    global action_counter
    for user in users_in_forbidden_groups:
        if action_counter > 80:
            action_counter = 0
            time.sleep(100)

        if not user.bot:
            await client.edit_permissions(CHANNEL, user, view_messages=False)
            await client.edit_permissions(GROUP, user, view_messages=False)
            time.sleep(5)
            username = ('@' + user.username) if user.username else ''
            await client.send_message(entity=LOG_CHANNEL,
                                      message=f'Banned {user.id if not user.username else username} for belonging to forbidden group')
            action_counter += 2


async def purge_unwanted_users(client, channel, group, log_channel, forbidden_groups):
    group_users = await client.get_participants(entity=group, aggressive=True)

    try:

        not_abyding_users_from_channel = await get_users_not_in_group(client, channel, group)
        not_abyding_users_from_group = await get_users_without_username(client, group)
        users_in_forbidden_groups = await get_users_in_forbidden_groups(client, forbidden_groups)

        print('\n')

        print(f'Numero de usuarios baneados por estar en grupos prohibidos:  {len(users_in_forbidden_groups)}')
        print('\n')

        await kick_from_group(client, not_abyding_users_from_group)

        await kick_from_channel(client, not_abyding_users_from_channel)

        # await ban_from_channel(client,users_to_be_kicked_from_channel)

        # await forbidden_group_ban(client, users_in_forbidden_groups)





    except ValueError as e:
        raise e


api_id, api_hash = env.API_ID, env.API_HASH

telethon_client = TelegramClient('session2', api_id, api_hash)
telethon_client.start(phone=env.PHONE, password=env.PASSWORD)

# purge_unwanted_users(client,channel,group,log_channel,[])

loop = asyncio.get_event_loop()

# loop.run_until_complete(get_users_not_in_group(client,channel,group))
#
# loop.run_until_complete(get_users_without_username(client ,group))
loop.run_until_complete(purge_unwanted_users(telethon_client, CHANNEL, GROUP, LOG_CHANNEL, forbidden_groups))
print("Done")
# time.sleep(1)
# loop.close()
# get_users_not_in_group(client,channel,group)
# get_users_without_username(client,group)
