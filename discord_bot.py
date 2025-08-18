import dotenv
import os
import discord
from discord.ext import commands
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT 


dotenv.load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  
intents.reactions = True 

bot = commands.Bot(command_prefix="!", intents=intents)

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="reaction_tracker",
            user="postgres",  
            password="password" 
        )
        return conn
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        return None

def initialize_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            message_id BIGINT UNIQUE NOT NULL,
            author_id BIGINT NOT NULL,
            channel_id BIGINT NOT NULL,
            guild_id BIGINT NOT NULL,
            content TEXT,
            created_at TIMESTAMP NOT NULL,
            month_year VARCHAR(7) NOT NULL
        """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS reactions (
            id SERIAL PRIMARY KEY,
            message_id BIGINT REFERENCES messages(message_id),
            emoji VARCHAR(255) NOT NULL,
            count INTEGER DEFAULT 1,
            users BIGINT[] DEFAULT ARRAY[]::BIGINT[],
            UNIQUE(message_id, emoji)
        """)

bot.run(os.getenv("TOKEN"))



