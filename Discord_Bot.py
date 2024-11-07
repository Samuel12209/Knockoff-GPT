import discord
from discord.ext import commands
import requests
import json
import asyncio

TOKEN = 'Your_Bot_Token' #put your bot's token here!
API_URL = 'http://localhost:12345/api/generate'

intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()  # Sync global commands
        print(f"Global commands synced successfully with {len(synced)} command(s).")
    except Exception as e:
        print(f"Error syncing commands: {e}")
    print(await bot.tree.fetch_commands())

@bot.tree.command(name="ask", description="Ask a question to the bot")
async def ask(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer(thinking=True)
    response = await generate_response(prompt)
    
    chunks = [response[i:i+2000] for i in range(0, len(response), 2000)]
    
    for chunk in chunks:
        await interaction.followup.send(content=chunk)
    
@bot.tree.command(name="placeholder", description="A basic placeholder command")
async def placeholder(interaction: discord.Interaction):
    await interaction.response.send_message("placeholder")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        await message.channel.send("Hello! How can I help you?")
        await bot.process_commands(message)

async def generate_response(prompt):
    data = {
        "model": "llama2",
        "prompt": prompt
    }
    try:
        response = requests.post(API_URL, json=data, stream=True)
        response.raise_for_status()

        accumulated_response = ""
        for line in response.iter_lines():
            if line:
                try:
                    response_data = json.loads(line)
                    response_text = response_data.get('response', '')
                    done = response_data.get('done', False)
                    accumulated_response += response_text

                    if done:
                        return accumulated_response
                except json.JSONDecodeError as e:
                    print("Failed to parse JSON:", line)
    except requests.RequestException as e:
        return f"Error generating response: {e}"

bot.run(TOKEN)

