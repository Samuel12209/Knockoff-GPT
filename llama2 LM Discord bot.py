import discord
from discord.ext import commands
import requests
import json

TOKEN = 'discord token'
API_URL = 'http://localhost:12345/api/generate'

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = commands.Bot(command_prefix='/', intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        await message.channel.send("**Direct Messages not allowed**")
        return
    
    if message.content.startswith('/ask'):
        prompt = message.content.split('/ask ', 1)[1]
        response = generate_response(prompt)
        if isinstance(response, tuple):
            await message.channel.send(response[0])
            await message.channel.send(response[1])
        else:
            await message.channel.send(response)

    if message.content.startswith('/test'):
        await message.channel.send('On')

def generate_response(prompt):
    data = {
        "model": "llama2",
        "prompt": prompt
    }
    try:
        response = requests.post(API_URL, json=data)
        if response.status_code == 200:
            responses = response.content.decode().split('\n')
            final_response = ''
            prev_char = ''
            for resp in responses:
                if resp.strip():
                    resp_json = json.loads(resp)
                    if 'response' in resp_json:
                        response_text = resp_json['response']
                        adjusted_text = ''
                        for char in response_text:
                            if char == ' ' and prev_char == ' ':
                                continue
                            if char in ',.!?':
                                if prev_char == ' ':
                                    adjusted_text = adjusted_text[:-1]
                            adjusted_text += char
                            prev_char = char
                        final_response += adjusted_text
                        
            if len(final_response) > 1990:
                cutoff_response = final_response[:1990].strip()
                remaining_response = final_response[1990:].strip()
                return cutoff_response, remaining_response
            else:
                return final_response.strip()
        else:
            return f"Error generating response: {response.status_code}"
    except Exception as e:
        return f"Error generating response: {e}"

client.run(TOKEN)