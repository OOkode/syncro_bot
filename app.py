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
bot_token = '1256869136:AAFVAZ71-YSUXBcct1wBQuYryHO-1BXXsDg'

action_counter = 0


def get_api_credentials():
    return env.API_ID, env.API_HASH


async def get_users_not_in_group(client, channel_users, group_users):
    print('---------- USUARIOS QUE NO ESTAN EN GRUPO ----------- \n')
    global ALLOWED_USERS
    unwanted_users = []




    for user in channel_users:
        if (user.username not in ALLOWED_USERS) and (not user.bot) and (not (user in group_users)):
            print(user.username or user.id)
            unwanted_users.append(user)

    print(len(unwanted_users))

    return unwanted_users


async def get_users_without_username(client, users):
    print('---------- USUARIOS SIN ALIAS -----------')

    unwanted_users = []

    for user in users:
        if not user.username:
            print(user.username or user.id)
            unwanted_users.append(user)

    print(len(unwanted_users))
    return unwanted_users


async def get_users_in_forbidden_groups(client, forbidden_groups):
    unwanted_users = []

    for group in forbidden_groups:
        users_in_forbidden_group = await client.get_participants(entity=group, aggressive=True)
        for user in users_in_forbidden_group:
            unwanted_users.append(user)

    print(f'Numero de usuarios en grupo prohibido: {len(unwanted_users)}')
    return unwanted_users


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
    channel_users = await client.get_participants(entity=channel, aggressive=True)
    print(len(group_users))
    print(len(channel_users))

    try:

        not_abyding_users_from_channel = await get_users_not_in_group(client, channel_users, group_users)
        not_abyding_users_from_group = await get_users_without_username(client, group_users)
        users_in_forbidden_groups = await get_users_in_forbidden_groups(client, forbidden_groups)

        print('\n')

        take_actions = input("Presione 'y' para ejecutar la purga, otra tecla para cancelar\n")

        if take_actions == 'y':
            pass
            # await kick_from_group(client, not_abyding_users_from_group)
            #
            # await kick_from_channel(client, not_abyding_users_from_channel)
            #
            # await ban_from_channel(client,not_abyding_users_from_channel)
            #
            # await forbidden_group_ban(client, users_in_forbidden_groups)
        else:
            print("Purga cancelada\n")
            return




    except ValueError as e:
        raise e


api_id, api_hash = env.API_ID, env.API_HASH

# telethon_client = TelegramClient('session2', api_id, api_hash)
# telethon_client.start(phone=env.PHONE, password=env.PASSWORD)

telethon_client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

loop = asyncio.get_event_loop()

loop.run_until_complete(purge_unwanted_users(telethon_client, CHANNEL, GROUP, LOG_CHANNEL, forbidden_groups))
print("Done")

