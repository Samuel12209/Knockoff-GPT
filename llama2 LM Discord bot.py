import discord
import requests
import json

TOKEN = 'Discord bot token'
API_URL = 'http://localhost:11434/api/generate'

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/ask'):
        prompt = message.content.split('/ask ', 1)[1]
        response = generate_response(prompt)
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
        print("Response status code:", response.status_code)
        print("Response content:", response.content)
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
            return final_response.strip()
        else:
            return f"Error generating response: {response.status_code}"
    except Exception as e:
        return f"Error generating response: {e}"

client.run(TOKEN)
