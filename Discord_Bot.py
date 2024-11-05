import discord
from discord.ext import commands
import requests
import json
import asyncio

TOKEN = 'Bot_Token' # put you bot token here
API_URL = 'http://localhost:12345/api/generate'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.slash_command(description="Ask a question to the bot")
async def ask(ctx, prompt: str):
    loading_message = await ctx.respond("Loading...")
    response = await generate_response(prompt, ctx.channel)
    await loading_message.edit(content=response)

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
