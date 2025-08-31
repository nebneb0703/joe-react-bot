import dotenv
import os
import discord
from discord.ext import commands
import psycopg2

conn = psycopg2.connect(os.getenv("DATABASE_URL"))

conn.set_session(autocommit=True)

def run_migrations(conn):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            message_id BIGINT PRIMARY KEY,
            author_id BIGINT NOT NULL,
            channel_id BIGINT NOT NULL,
            guild_id BIGINT NOT NULL,
            created_at TIMESTAMP NOT NULL
        );
        """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS reactions (
            user_id BIGINT NOT NULL,
            message_id BIGINT REFERENCES messages(message_id),
            emoji VARCHAR(255) NOT NULL,
            PRIMARY KEY(user_id, message_id, emoji)
        );
        """)

    cur.close()

run_migrations(conn)

dotenv.load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.hybrid_command()
async def ping(ctx):
    await ctx.send("Pong!")

bot.run(os.getenv("DISCORD_TOKEN"))
