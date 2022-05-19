# **Monke Rank**

This is mainly a way to replace ActivityRank in our current server (Nanahira Monke). Trying to have less reliance on random bots from outside sources and by making our own bot, we'll have full customization and features that ActivityRank won't have (such as extra XP for boosted members or adding role images to users).

Probably will be appended into [kanadeBot](https://github.com/LEOIIDX/kanadeBot) at some point, but should get working standalone first to make sure it gets put in smoothly.

### **To use:**
Note: This is for a Windows install
1. Download this repo as a .zip file
2. Create a a file called ".env" and open it in a text editor and add your [Discord Bot Token](https://www.writebots.com/discord-bot-token/) as:</br>
`TOKEN=your token here`</br>
3. Invite the bot to whatever server you wish with the Scopes of "bot" and "applications.commands" and with the permissions of "Administrator" ([Instructions on how here](https://discordpy.readthedocs.io/en/stable/discord.html))
4. Run the bot in [Python 3.10](https://www.python.org/downloads/) by installing Python 3.10 and entering the following into a command prompt (ex. cmd, Powershell):</br>
Install dependencies:</br>
`py -3 -m pip install -U py-cord --pre` Pycord to run Discord API</br>
`pip install asyncio` Asyncio, needed for Pycord</br>
`pip install dotenv` dotenv, needed for reading .env file</br>
Run bot:</br>
`cd "dir/to/the/bot/folder/Monke Rank"`</br>
`python main.py`</br>

5. Should be running smootly and activity should start being tracked! Test out what commands you can use using /help
6. If you want this bot to continue running, consider running it on a dedicated server to keep it up all the time. There are tutorials online for this if you wish to do so.

#### **TODO:**
- **[In progress]** Change roles in a server depending on level of user 
- **[In progress]** Create embeds that show users level, xp, message count, etc. 
- **[In progress]** Create a leaderboard of all top users in the server that shows xp, level, messages, etc. 
- Transfer over/export current ActivityRank levels to this bot (will need to be done manually but not too hard)
- Special things for boosted members, such as extra xp
- Return of a special ranking...
- Amount of channels active in the past week
- Guess future ranks and time of arrival by extrapolation?
- Make a command that gives extra xp for a specified amount of time (used for an event in the server to promote engagement)

#### **Done!:**
- Create new users in the users.json file
- Be able to calculate each of the values inside the users.json file
- Track voice call time in minutes
- Track new things that ActivityRanker does not: Reaction counts, images/embeds sent counts
- Send an embed using a command to show the current user's level and activity
