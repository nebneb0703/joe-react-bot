import dotenv
import os
import discord.ext

bot = discord.ext.commands.Bot(command_prefix="!")

dotenv.load_dotenv()

bot.run(os.getenv("TOKEN"))

