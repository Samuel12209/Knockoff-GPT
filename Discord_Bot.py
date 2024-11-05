import discord
from discord.ext import commands
import requests
import json
import asyncio

TOKEN = 'You_Discord_Token'  # Replace with your actual bot token!
API_URL = 'http://localhost:12345/api/generate'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.slash_command(description="Ask a question to the bot")
async def ask(ctx, prompt: str):
    await ctx.respond("Response loading...")
    response = await generate_response(prompt, ctx.channel)

@bot.command()
async def test(ctx):
    await ctx.send('On')

async def send_message(channel, message):
    await channel.send(message)

def handle_response(response_text, channel):
    MAX_CHAR_LIMIT = 2000

    # Check if the response is too long
    if len(response_text) > MAX_CHAR_LIMIT:
        # Split the response into chunks based on MAX_CHAR_LIMIT
        for i in range(0, len(response_text), MAX_CHAR_LIMIT):
            chunk = response_text[i:i + MAX_CHAR_LIMIT]
            asyncio.create_task(send_message(channel, chunk))
    else:
        asyncio.create_task(send_message(channel, response_text))

async def generate_response(prompt, channel):
    data = {
        "model": "llama2",
        "prompt": prompt
    }

    try:
        response = requests.post(API_URL, json=data, stream=True)
        response.raise_for_status()

        accumulated_response = ""
        # Process the streamed response
        for line in response.iter_lines():
            if line:  # Ensure there's data in the line
                # Attempt to parse JSON
                try:
                    response_data = json.loads(line)
                    response_text = response_data.get('response', '')
                    done = response_data.get('done', False)

                    accumulated_response += response_text

                    if done:
                        handle_response(accumulated_response, channel)
                        break

                except json.JSONDecodeError as e:
                    print("Failed to parse JSON:", line)  # Log the raw line that failed to parse

    except requests.RequestException as e:
        await send_message(channel, f"Error generating response: {e}")

bot.run(TOKEN)