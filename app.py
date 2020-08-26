from telethon import TelegramClient, events, sync
from telethon.errors.rpcerrorlist import UserAdminInvalidError
import env
import time, asyncio
from telethon.sync import TelegramClient
from telethon import functions, types

ALLOWED_USERS = ['ChelpBots']

channels = {'Granma': -1001360204322, 'Pinar': 'AlertaTuenvioPinar','Artemisa':'AlertaTuenvio_Artemisa',
            'Santa_Clara': 'TuEnvio_Canal'}

groups = {'Granma': 'tuenviogranma', 'Pinar': 'TuenvioPinardelRio','Artemisa':'TuenvioArtemisa',
          'Santa_Clara': 'TuEnvio_Sta_Clara'}

log_channels = {'Granma': -1001394912157, 'Pinar': 'logpinardelrio','Artemisa':'logsartemisa',
                'Santa_Clara': -1001219375136}

forbidden_groups = ['tuenviopinargrupo', ]

CHANNEL = channels['Granma']
GROUP = groups['Granma']
LOG_CHANNEL = log_channels['Granma']
bot_token = env.BOT_TOKEN

action_counter = 0


def get_api_credentials():
    return env.API_ID, env.API_HASH


async def get_users_not_in_group(client, channel_users, group_users):
    print('---------- USUARIOS QUE NO ESTAN EN GRUPO ----------- \n')
    global ALLOWED_USERS
    unwanted_users = []

    for user in channel_users:
        if ((user.username not in ALLOWED_USERS) and (not user.bot) and (not (user in group_users)) or (
        not user.username)):
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
            try:
                await client.kick_participant(entity=CHANNEL, user=user)
                time.sleep(5)
                username = ('@' + user.username) if user.username else ''
                await client.send_message(entity=LOG_CHANNEL,
                                          message=f'Kicked {user.id if not user.username else username} for not subscribing to the group')
            except UserAdminInvalidError as e:
                print(f"No se pude eliminar al usuario {user.username if user.username else user.id}")

            action_counter += 2


async def ban_from_channel(client, users_to_be_banned_from_channel):
    global action_counter
    for user in users_to_be_banned_from_channel:
        if action_counter > 80:
            action_counter = 0
            time.sleep(100)

        if not user.bot:

            try:
                await client.edit_permissions(CHANNEL, user.id, view_messages=False)
                time.sleep(5)
                username = ('@' + user.username) if user.username else ''
                await client.send_message(entity=LOG_CHANNEL,
                                          message=f'Banned {user.id if not user.username else username} for not subscribing to the group')
            except UserAdminInvalidError as e:
                print(f"No se pude eliminar al usuario {user.username if user.username else user.id}")

            action_counter += 2


async def kick_from_group(client, users_to_be_kicked_from_group):
    global action_counter
    for user in users_to_be_kicked_from_group:

        if action_counter > 80:
            action_counter = 0
            time.sleep(100)

        await client.kick_participant(entity=GROUP, user=user)
        # await kick_from_channel(client,[user])
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
            try:
                await client.edit_permissions(CHANNEL, user.id, view_messages=False)
                await client.edit_permissions(GROUP, user.id, view_messages=False)
                time.sleep(5)
                username = ('@' + user.username) if user.username else ''
                await client.send_message(entity=LOG_CHANNEL,
                                          message=f'Banned {user.id if not user.username else username} for belonging to forbidden group')

            except UserAdminInvalidError as e:
                print(f"No se pude eliminar al usuario {user.username if user.username else user.id}")

            action_counter += 2


async def purge_unwanted_users(client, channel, group, log_channel, forbidden_groups):
    channel_users = await client.get_participants(entity=channel, aggressive=True)
    group_users = await client.get_participants(entity=group, aggressive=True,
                                                filter=types.ChannelParticipantsSearch(''), limit=10000)
    print(f"Usuarios en grupo {len(group_users)}")
    print(f"Usuarios en canal {len(channel_users)}")

    try:

        not_abyding_users_from_channel = await get_users_not_in_group(client, channel_users, group_users)
        not_abyding_users_from_group = await get_users_without_username(client, group_users)
        users_in_forbidden_groups = await get_users_in_forbidden_groups(client, forbidden_groups)

        print('\n')

        take_actions = input("Presione 'y' para ejecutar la purga, otra tecla para cancelar\n")

        if take_actions == 'y':
            pass
            await kick_from_group(client, not_abyding_users_from_group)
            #
            # await kick_from_channel(client, not_abyding_users_from_channel)
            #
            await ban_from_channel(client, not_abyding_users_from_channel)
            #
            await forbidden_group_ban(client, users_in_forbidden_groups)
        else:
            print("Purga cancelada\n")
            return

    except ValueError as e:
        raise e


api_id, api_hash = env.API_ID, env.API_HASH

telethon_client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
print('Logged in')

loop = asyncio.get_event_loop()

loop.run_until_complete(purge_unwanted_users(telethon_client, CHANNEL, GROUP, LOG_CHANNEL, []))
# loop.run_until_complete(purge_unwanted_users(telethon_client,channels['Santa_Clara'], groups['Santa_Clara'],log_channels['Santa_Clara'],[]))

print("Done")
