import asyncio

from shazamio import Shazam


async def main():
    shazam = Shazam()
    out = await shazam.recognize_song('summergirl.mp3')
    track_title = out['track']['title']
    artist = out['track']['subtitle']
    print(track_title + ' by ' + artist)

    payload_json = {'song': {'title':track_title, 'artist':artist}}
    print(payload_json)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

