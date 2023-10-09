from misskist import Client, ChannelType, Channel, events
import asyncio


class GlobalChannel(Channel, channel_type=ChannelType.global_timeline):

    @events.on_event("note")
    async def on_note(self, note):
        print(note.text)


async def main():
    client = Client("misskey.io", loop=asyncio.get_running_loop())
    await client.add_channel(GlobalChannel())
    await client.connect("1ato2t9c7WaKJgqv8AjcRkQljdtPgMjG")


asyncio.run(main())