import discord
from discord.ext import commands
import requests
import json
import asyncio

TOKEN = 'Your bot token!'
API_URL = 'http://localhost:12345/api/generate'
YOUR_USER_ID = 12345 # Replace with your Discord User ID

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        # Force sync global commands
        synced = await bot.tree.sync()
        print("Global commands synced successfully.")
        print(f"Commands synced: {synced}")
    except Exception as e:
        print(f"Error syncing commands: {e}")

@bot.tree.command(name="ask", description="Ask a question to the bot")
async def ask(interaction: discord.Interaction, prompt: str):
    # Check if the command was issued by you
    if interaction.user.id != YOUR_USER_ID:
        await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)
        return

    # Provide initial response indicating that the bot is processing
    await interaction.response.send_message("Loading...", ephemeral=True)
    response = await generate_response(prompt, interaction.channel)
    
    # Use followup to edit the original response
    await interaction.followup.send(content=response)

@bot.command()
async def test(ctx):
    await ctx.send('On')

async def send_message(channel, message):
    await channel.send(message)

async def generate_response(prompt, channel):
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
                        if "remember" in prompt.lower() or "numbers" in prompt.lower():
                            return f"The numbers I remember are: {accumulated_response.strip()}"
                        return accumulated_response

                except json.JSONDecodeError as e:
                    print("Failed to parse JSON:", line)

    except requests.RequestException as e:
        await send_message(channel, f"Error generating response: {e}")

bot.run(TOKEN)

