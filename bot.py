# This example requires the 'message_content' intent.

import os
from dotenv import load_dotenv
import discord
from discord.utils import get
from discord.ext import commands

import requests
import json

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

messages = [
    "Ready to fight? 🤜👊🤛 We're asking the controversial questions here at DEX. React to the polls with the emoji that indicates your preference and see the results at https://bit.ly/sort-the-madness",
    """The age old question...
Tabs (🔵) or Spaces (🟣)?""",
    """What editor will you throw down for?
Emacs (🔵)
Vim (🟣)
JetBrains (🔴)
Notepad (🟠)""",
    """Best OS?
Windows (🔵), MacOS (🟣) or Linux (🔴)""",
    """Preferred cloud?
AWS (🔵)
Azure (🟣)
GCP (🔴)
IBM (🟠)
My own servers (🟡)""",
    """Best web framework?
Next.js (🔵)
React (🟣)
Flask (🔴)
FastAPI (🟠)
Svelte (🟡)""",
    """Most important keyboard attribute?
Mechanical (🔵)
Split (🟣)
Backlit (🔴)
It's my laptop (🟠)""",
    """Favorite music for coding?
Lofi (🔵)
Classical (🟣)
Ambient (🔴)
Podcasts (🟠)
Silence (🟡)"""
]

poll_message_info = [{"time": "intro", "sent": False, "reactions": {}, "text": messages[0]},
                     {"time": "9am", "sent": False, "reactions": {
                         '🔵': 0, '🟣': 0}, "text": messages[1]},
                     {"time": "10am", "sent": False, "reactions": {
                         '🔵': 0, '🟣': 0, '🔴': 0, '🟠': 0}, "text": messages[2]},
                     {"time": "11am", "sent": False, "reactions": {
                         '🔵': 0, '🟣': 0, '🔴': 0}, "text": messages[3]},
                     {"time": "12pm", "sent": False, "reactions": {
                         '🔵': 0, '🟣': 0, '🔴': 0, '🟠': 0, '🟡': 0}, "text": messages[4]},
                     {"time": "1pm", "sent": False, "reactions": {
                         '🔵': 0, '🟣': 0, '🔴': 0, '🟠': 0, '🟡': 0}, "text": messages[5]},
                     {"time": "2pm", "sent": False, "reactions": {
                         '🔵': 0, '🟣': 0, '🔴': 0, '🟠': 0}, "text": messages[6]},
                     {"time": "3pm", "sent": False, "reactions": {
                         '🔵': 0, '🟣': 0, '🔴': 0, '🟠': 0, '🟡': 0}, "text": messages[7]}
                     ]
poll_message_ids_to_info = {}


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author.id != 446079130094534656:  # only works for Shana's account
        return

    command, *middle, time = message.content.split()
    if command.startswith('$poll'):
        poll_id = 0
        match time:

            case "9am":
                poll_id = 1
            case "10am":
                poll_id = 2
            case "11am":
                poll_id = 3
            case "12pm":
                poll_id = 4
            case "1pm":
                poll_id = 5
            case "2pm":
                poll_id = 6
            case "3pm":
                poll_id = 7
            case _:
                poll_id = 0

        this_poll_info = poll_message_info[poll_id]
        if poll_id != 0 and this_poll_info["sent"]:
            return

        this_poll_info["sent"] = True
        sent_message = await message.channel.send(content=this_poll_info['text'], delete_after=3600)
        this_poll_info['id'] = sent_message.id
        poll_message_ids_to_info[sent_message.id] = this_poll_info

        for react in this_poll_info['reactions'].keys():
            await sent_message.add_reaction(react)


@client.event
async def on_raw_reaction_add(payload):
    if payload.message_id in poll_message_ids_to_info.keys() and payload.member.id != 1017216995575463986:  # if not done by the bot
        emoji = payload.emoji.name
        reactions = poll_message_ids_to_info[payload.message_id]['reactions']
        if emoji in reactions.keys():
            print('received valid reaction')
            reactions[emoji] += 1
            print(reactions[emoji])
            await write_reactions_to_gist()
            # channel = client.get_channel(payload.channel_id)
            # message = await channel.fetch_message(payload.message_id)
            # reaction = get(message.reactions, emoji=payload.emoji.name)
            # if reaction and reaction.count > 4:
            #     await message.delete()


@client.event
async def on_raw_reaction_remove(payload):
    if payload.message_id in poll_message_ids_to_info.keys():
        emoji = payload.emoji.name
        reactions = poll_message_ids_to_info[payload.message_id]['reactions']
        if emoji in reactions.keys():
            print('removed valid reaction')
            reactions[emoji] -= 1
            print(reactions[emoji])
        # if payload.emoji.name == "🔁":
        #     print('got reaction')
        #     channel = client.get_channel(payload.channel_id)
        #     message = await channel.fetch_message(payload.message_id)
        #     reaction = get(message.reactions, emoji=payload.emoji.name)
        #     if reaction and reaction.count > 4:
        #         await message.delete()


async def write_reactions_to_gist():
    url = os.environ['GIST_URL']
    headers = {'Authorization': 'token %s' % os.environ['GH_TOKEN']}
    params = {'scope': 'gist'}

    payload = {"description": "DEX 2022 bot data", "public": False, "files": {"dex-2022-bot-data.json": {
        "content": json.dumps(poll_message_info)}}}

    # make a requests
    res = requests.patch(url, headers=headers, params=params,
                         data=json.dumps(payload))

    # print response --> JSON
    print(res.status_code)
    # print(res.url)
    # print(res.text)
    # j = json.loads(res.text)

    # # Print created GIST's details
    # for gist in range(len(j)):
    #     print("Gist URL : %s" % (j['url']))
    #     print("GIST ID: %s" % (j['id']))

# @commands.command(name="poll")
# async def poll(self, ctx: commands.Context, arg1, arg2):
#     arg3 = int(arg2)/3600
#     embed = discord.Embed(
#         title="NEW POLL", description=f"{arg1} \nPoll lasts for: {round(arg3, 2)}h")
#     embed2 = discord.Embed(
#         title="POLL OVER", description="The answer is `yes`(✅)!")
#     embed3 = discord.Embed(
#         title="POLL OVER", description="The answer is `no` (❌)!")
#     embed4 = discord.Embed(title="POLL OVER", description="It's a tie!")
#     message = await ctx.send(embed=embed)
#     await message.add_reaction("✅")
#     await message.add_reaction("❌")
#     # time.sleep(int(arg2))

# @client.event
# async def on_raw_reaction_add(ctx):
#     if ctx.emoji.name == "✅":
#         channel = client.get_channel(chanelidhere)
#         message = await channel.fetch_message(ctx.message_id)
#         reaction = get(message.reactions, emoji=ctx.emoji.name)
#         COUNT = reaction.count

client.run(
    os.environ['BOT_LOGIN_TOKEN'])
