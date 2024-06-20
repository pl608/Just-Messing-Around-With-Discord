import discord
from discord.ext import commands
import os

mod_channels = []
ignore_people = []
emoji_list = []

jayden = None
# Create a bot instance
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
intents.messages = True
intents.dm_messages = True

#client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='!', intents=discord.Intents.all())


# Event handler for when the bot is ready
@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} ({client.user.id})')
    user = await client.fetch_user(1083462612857139320)
    jayden = await client.fetch_user(1243391980076138648)
    mod_channels.append(user)
    ignore_people.append(user)
    emoji_list.append((jayden, '\U0001F44D'))
async def get_user_by_id(uid):
    if uid.startswith('<'):
        uid = uid[2:-1]
    u = await client.fetch_user(int(uid))
    return u
# Event handler for when a message is received
@client.event
async def on_message(message):
    global jayden
    jayden = await client.fetch_user(1243391980076138648)
    # Send a response to the same channel
    if (message.author != client.user) and (message.author not in ignore_people):
        await message.channel.send('Hello!')
    for emoji, user in emoji_list:
        if message.author == user:
            await message.add_reaction(emoji)
    if message.content.startswith('!ignore'):
        u = await get_user_by_id( message.content.split(' ')[-1])
        if u not in ignore_people:
            ignore_people.append(u)
            await message.channel.send(f'Ignoreing messages from {u.name}')
        else:
            await message.channel.send(f'{u.name} already is in ignored users')
        
    elif message.content.startswith('!uningnore'):
        u = await get_user_by_id( message.content.split(' ')[-1])
        if u in ignore_people:
            ignore_people.remove(u)
            await message.channel.send(f'removed {u.name} from ignored users')
        else:
            await message.channel.send(f'{u.name} not in ignored users')
    elif message.content.startswith('!react'):
        u = await get_user_by_id( message.content.split(' ')[1])
        emoji = message.content.split(' ')[2]
        emoji_list.append((emoji, u))
        await message.channel.send(f'Now reacting with {emoji} to {u.name}')
@client.event
async def on_message_delete(message):
    print('message deleted')
    for chnl in mod_channels:
        await chnl.send(
            f"Message deleted\nAuthor:{message.author}\nContent: `{message.content}`\nCreated: {message.created_at}"
        )

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
client.run(os.getenv("TOKEN"))
