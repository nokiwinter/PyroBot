import os
import time
import platform
import asyncio
try:
    import ping3
    from telethon.sync import TelegramClient
    from telethon import TelegramClient, events, sync
    from telethon import functions, types
except:
    os.system('pip install telethon')
    os.system('pip install ping3')
    import ping3
    from telethon.sync import TelegramClient
    from telethon import TelegramClient, events, sync
    from telethon import functions, types

# Etc
start_time = time.time()
python_version = platform.python_version()

# Api's
def save_api_credentials(api_id, api_hash):
    with open('api_credentials.txt', 'w') as file:
        file.write(f'API_ID={api_id}\n')
        file.write(f'API_HASH={api_hash}')
def load_api_credentials():
    try:
        with open('api_credentials.txt', 'r') as file:
            lines = file.readlines()
            api_id = lines[0].strip().split('=')[1]
            api_hash = lines[1].strip().split('=')[1]
            return api_id, api_hash
    except FileNotFoundError:
        return None, None
saved_api_id, saved_api_hash = load_api_credentials()
if saved_api_id is not None and saved_api_hash is not None:
    print("API credentials loaded from file:")
    print(f"API ID: {saved_api_id}")
    print(f"API Hash: {saved_api_hash}")
else:
    api_id = input("Enter your API ID (my.telegram.org): ")
    api_hash = input("Enter your API Hash (my.telegram.org): ")
    save_api_credentials(api_id, api_hash)
    print("API credentials saved to file.")

# Connecting
bot = "PyroBot"
try:
    client = TelegramClient(bot, saved_api_id, saved_api_hash)
except:
    client = TelegramClient(bot, api_id, api_hash)
client.start()

# Welcome
try:
    welcome_chat = client(functions.messages.CreateChatRequest(users=['me'], title="♠ PyroBot Beta"))
    chat_id = welcome_chat.chats[0].id
    client.send_message(chat_id, "**✨ Welcome to PyroBot beta!**\n\n|-✅ Loaded successful\n|-⚙ Try .help", parse_mode="Markdown")
except:
    client.send_message("me", "**✨ Welcome to PyroBot beta!**\n\n|-✅ Loaded successful\n|-⚙ Try .help", parse_mode="Markdown")

# Alive
try:
    @client.on(events.NewMessage)
    async def alive_command(event):
        if event.raw_text == ".alive":
            live_time = time.time()
            uptime = live_time - start_time
            uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime))
            await event.edit(f"**🔌 PyroBot Beta is alive! **\n\n|-⏳ Uptime: {uptime_str}\n|-🐍 Python version: {python_version}\n|-⚙ PyroBot version: Beta (v.0.1)", parse_mode="markdown")
except:
    pass

# Help
try:
    @client.on(events.NewMessage)
    async def help_command(event):
        if event.raw_text == ".help":
            await event.edit("**♠ Available commands: **\n\n|- help - shows all available commands.\n|- alive - shows uptime and other information.\n|- type - Typing animation, using: .type <text>\n|- Ping - Pings a hostname, usage: .ping <hostname>")
except:
    pass

# Ping
try:
    @client.on(events.NewMessage)
    async def type_command(event):
        if event.raw_text.startswith(".ping "):
            await event.edit("⏲ Pinging...")
            text = event.raw_text[6:]
            rtt = ping3.ping(text)
            await event.delete()
            if rtt is None or rtt == 0.00:
                await event.respond(f'⭕ Failed to ping.')
            else:
                await event.respond(f'⏲ Ping to <{text}> is <{rtt:.2f}>')
except:
    pass

# Type
try:
    @client.on(events.NewMessage)
    async def type_command(event):
        if event.raw_text.startswith(".type "):
            text = event.raw_text[6:]
            typing_event = await event.respond(".")  # Start with an empty message
            await event.delete()  # Delete the original command
            await asyncio.sleep(0.1)  # Pause briefly before starting the animation
            for i in range(len(text) + 1):
                await asyncio.sleep(0.1)  # Adjust the typing speed here
                message_to_send = text[:i] + "|"  # Add the cursor "|" at the current position
                if i == len(text):
                    await asyncio.sleep(0.1)  # Pause for a moment before removing the typing status
                else:
                    await asyncio.sleep(0.1)
                await typing_event.edit(message_to_send)
            await typing_event.delete()  # Remove the typing status
            await event.respond(text)
except:
    pass

#Keep
client.run_until_disconnected()
