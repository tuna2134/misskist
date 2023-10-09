from misskist import Client, ChannelType, Channel, events
import asyncio

from os import getenv


class GlobalChannel(Channel, channel_type=ChannelType.global_timeline):
    @events.on_event("note")
    async def on_note(self, note):
        print(note.text)


async def main():
    client = Client("misskey.io", loop=asyncio.get_running_loop())
    await client.add_channel(GlobalChannel())
    token = getenv("TOKEN")
    client.set_token(token)
    print(await client.create_note("Hello, World!"))
    await client.connect()


asyncio.run(main())
