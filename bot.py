# This example requires the 'message_content' intent.

import os
from dotenv import load_dotenv
import discord
from discord.utils import get
from discord.ext import commands

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

poll_message_info = [{"time": "intro", "sent": False, "reactions": [], "text": "Ready to fight? 🤜👊🤛 We're asking the controversial questions here at DEX. React to the polls with the emoji that indicates your preference and see the results at https://bit.ly/sort-the-madness"},
                     {"time": "9am", "sent": False, "reactions": ['🔵', '🟣'], "text":
                      """The age old question...
Tabs (🔵) or Spaces (🟣)?"""},
                     {"time": "10am", "sent": False, "reactions": ['🔵', '🟣', '🔴', '🟠'], "text":
                      """What editor will you throw down for?
Emacs (🔵)
Vim (🟣)
JetBrains (🔴)
Notepad (🟠)"""},
                     {"time": "11am", "sent": False, "reactions": ['🔵', '🟣', '🔴'], "text":
                      """Best OS?
Windows (🔵), MacOS (🟣) or Linux (🔴)"""},
                     {"time": "12pm", "sent": False, "reactions": ['🔵', '🟣', '🔴', '🟠', '🟡'], "text":
                      """Preferred cloud?
AWS (🔵)
Azure (🟣)
GCP (🔴)
IBM (🟠)
My own servers (🟡)"""},
                     {"time": "1pm", "sent": False, "reactions": ['🔵', '🟣', '🔴', '🟠', '🟡'], "text":
                      """Best web framework?
Next.js (🔵)
React (🟣)
Flask (🔴)
FastAPI (🟠)
Svelte (🟡)"""},
                     {"time": "2pm", "sent": False, "reactions": ['🔵', '🟣', '🔴', '🟠'], "text":
                      """Most important keyboard attribute?
Mechanical (🔵)
Split (🟣)
Backlit (🔴)
It's my laptop (🟠)"""},
                     {"time": "3pm", "sent": False, "reactions": ['🔵', '🟣', '🔴', '🟠', '🟡'], "text": """Favorite music for coding?
Lofi (🔵)
Classical (🟣)
Ambient (🔴)
Podcasts (🟠)
Silence (🟡)"""}
                     ]
poll_message_ids_to_reactions = {}


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

        poll_info = poll_message_info[poll_id]
        if poll_id != 0 and poll_info["sent"]:
            return

        poll_info["sent"] = True
        sent_message = await message.channel.send(content=poll_info['text'], delete_after=3600)
        poll_info['id'] = sent_message.id
        poll_message_ids_to_reactions[sent_message.id] = poll_info['reactions']

        for react in poll_info['reactions']:
            await sent_message.add_reaction(react)


@client.event
async def on_raw_reaction_add(payload):
    if payload.message_id in poll_message_ids_to_reactions.keys() and payload.member.id != 1017216995575463986:  # if not done by the bot
        print(poll_message_ids_to_reactions[payload.message_id])
        if payload.emoji.name in poll_message_ids_to_reactions[payload.message_id]:
            print('got valid reaction')
            channel = client.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            reaction = get(message.reactions, emoji=payload.emoji.name)
            # if reaction and reaction.count > 4:
            #     await message.delete()


# @client.event
# async def on_raw_reaction_remove(payload):
#     if payload.channel_id == 1009916854279602269:  # shana todo update this to the Sort the Madness channel
#         if payload.emoji.name == "🔁":
#             print('got reaction')
#             channel = client.get_channel(payload.channel_id)
#             message = await channel.fetch_message(payload.message_id)
#             reaction = get(message.reactions, emoji=payload.emoji.name)
#             if reaction and reaction.count > 4:
#                 await message.delete()


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
