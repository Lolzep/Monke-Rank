import discord
import os

from dotenv import load_dotenv
from myfunctions import update_user, json_dump, json_read, restart_bot

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
	try:
		# Ignore bots
		if message.author.bot == True:
			return

		message_count, image_count, embeds_count = 0, 0, 0
		# Message counts
		data, user = update_user(message.author.id, message.author.name, "messages", False)
		message_count += 1

		# Image counts
		if message.attachments:
			data, user = update_user(message.author.id, message.author.name, "images", False)
			image_count += 1
		
		# Embed counts
		if message.embeds:
			data, user = update_user(message.author.id, message.author.name, "embeds", False)
			embeds_count += 1

		# XP
		# ActivityRank: Messages are 10 XP
		xp = 0
		xp = (message_count * 5) + (image_count * 10) + (embeds_count * 10)
		user["xp"] += xp 

		# Rank
		# ActivityRank: Level Factor
		current_level = user["level"]
		current_xp = user["xp"]
		data_level = json_read("levels.json")
		next_xp = data_level["levels"][current_level]["total_xp"]

		if next_xp < current_xp:
			data, user = update_user(message.author.id, message.author.name, "level", False)

		json_dump(data)

		if message.content.startswith('$hello'):
			await message.channel.send('Hello!')
	except PermissionError:
		print("Error!!")
		await restart_bot()

@bot.event
async def on_reaction_add(reaction, user):
	update_user(user.id, user.name, "reactionsadded", True)
	update_user(reaction.message.author.id, reaction.message.author.name, "reactionsrecieved", True)


@bot.event
async def on_voice_state_update(member, before, after):
	# ActivityRank: Voiceminutes are 5 XP
	# When user joins vc...
	if before.channel is None and after.channel is not None:
		print("start")
	# When user moves vc...
	elif before.channel is not None and after.channel is not None:
		print("moved")
	# When user leaves vc...
	else:
		print("end")


# @bot.slash_command(guild_ids=[273567091368656898])
# async def level(ctx):
#     await ctx.respond(f"Your level is {level}")


bot.run(TOKEN)

