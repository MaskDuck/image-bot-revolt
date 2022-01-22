import asyncio
import aiohttp
import revolt
import io
import typing
import os

from revolt.ext import commands

async def request(ctx, endpoint, params):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.jeyy.xyz/image/{endpoint}', params=params) as response:
            buffer = io.BytesIO(await response.read())
            await ctx.send(file=revolt.File(buffer, f'{endpoint}.gif'))

class Client(commands.CommandsClient):
    async def get_prefix(self, message: revolt.Message):
        return "pls make "

    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.send("pong")
    
    @commands.command()
    async def shear(self, ctx, *, member: typing.Union[revolt.User, str] = None, level: int = None):
        if isinstance(member, revolt.User):
            params = {
                'image_url': member.avatar.url
            }
        elif isinstance(member, str):
            params = {
                'image_url': member
            }
        if level is not None:
            if 1 <= level <= 10:
                params['level'] = level
            else:
                await ctx.send("Level must be within 1 and 10!")
        
        await request(ctx, 'shear', params)
        

async def main():
    async with aiohttp.ClientSession() as session:
        client = Client(session, os.environ['revoltToken'])
        await client.start()

asyncio.run(main())