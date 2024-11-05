import discord
from discord.ext import commands
import requests
import json

TOKEN = 'You Discord Bot token' # Bot token!
API_URL = 'http://localhost:12345/api/generate'  # Removed trailing slash

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def ask(ctx, *, prompt):
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.send("**Direct Messages not allowed**")
        return
    
    response = generate_response(prompt)
    if isinstance(response, tuple):
        await ctx.send(response[0])
        await ctx.send(response[1])
    else:
        await ctx.send(response)

@bot.command()
async def test(ctx):
    await ctx.send('On')

def generate_response(prompt):
    data = {
        "model": "llama2",
        "prompt": prompt
    }
    try:
        response = requests.post(API_URL, json=data)
        response.raise_for_status()
        responses = response.json()
        final_response = ''
        for resp in responses:
            if 'response' in resp:
                final_response += resp['response'].strip() + ' '
        
        final_response = final_response.strip()
        if len(final_response) > 1990:
            return final_response[:1990], final_response[1990:]
        else:
            return final_response
    except requests.RequestException as e:
        return f"Error generating response: {e}"

bot.run(TOKEN)