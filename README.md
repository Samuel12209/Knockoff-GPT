# llama2 LM Discord bot | Status: functional
Ran on ![ollama](https://img.shields.io/badge/Ollama-000000.svg?style=for-the-badge&logo=Ollama&logoColor=white)

a Discord bot that uses Ollama to generate responses that you host locally!

If you have any issues please create an issue and let me know!
# llama2 Model
You can find the LM that i am using [here](https://ollama.com/library/llama2:7b) to run this discord bot

# Setup
First download and setup ollama then go to [llama2](https://ollama.com/library/llama2:7b) model and run the steps there. then Run the command ```$env:OLLAMA_HOST="localhost:12345"``` then ```ollama serve``` to start it, you can do this in terminal or an IDE of your choice if you choose to. Once you have made a request on discord it should give you a 200 response code. make an issue ![here](https://github.com/Samuel12209/Knockoff-GPT/issues) if you run into problems

(Optional) You can then make this into a user application so you can run it in direct messages and other servers!
## Optional
if you want to use the ai without discord, then go to a new terminal then run ```ollama run llama2:7b``` ignoring the first the first step
it will install them model(~7GB) and will use 16 Gigs  of ram Maximum but is operable with partially operable with 13 Gigs of ram

# Quick fixes

If you run into the problem of your port being allready used, you can go into task manager and terminate ollama. If you dont want to or its needed then you can change the port number