# Imports

import json
import discord
from discord.ext import commands
from pyrule_compendium import compendium
import config

# Created an instance of the client using Bot() which
# can do what discord.client does as well
# .Bot() is a subclass of Discord.Client()

client = commands.Bot(command_prefix = '!', intents = discord.Intents.all()) # Used .Bot(command_prefix=) to set the bot's command invokation prefix to '!' — Enabled all intents

# Created an event using Discord.py's decorator to
# print a statement when bot is on_ready

@client.event # No parentheses as there are no parameters to set for events
async def on_ready(): # Async function — function names have to come from Discord library
    print('We are connected and ready to go!')

# Created a test command with info on how everything wroks with Discord library
# Must use () when using .command(), in case we're changing attributes for our commands via paraemters
# With commands, the function name is the command name,
# meaning users must say <"!ping"> for this command to work
# Must pass context <ctx> into function as the first parameter

@client.command()
async def ping(ctx):
     await ctx.send('Pong!') # .send() is from Discord library. Start .send() with an <await>

# Created a command to send BOTW data when the function is called
# The response is a rich text embed with content imported from pyrule API via wrapper
# Used <aliases => as a parameter to change how the function in the command can be called by users

# Created an async function for the command and titled it
# whatever I wanted as, unlike events, commands
# are not titled after functions or methods in Discord.py

# The title of the function is what users must type when
# calling the command via the ping (!FUNCTIONNAME)

# The function name can be given aliases if
# <aliases = > is passed as a parameter into client.commands()

# Passed 3 parameters to function, ctx, *, and a made-up parameter
# Ctx for Discord lib requirements, * to take in 
# multiple would-be values into function as one argument
# (i.e: a sentence with spaces and multiple words will be one arguement)
# user_request as a made-up parameter requesting a user input

@client.command(aliases = ['Sheikahslate', 'info', 'botw', 'botwinfo'])
async def sheikahslate(ctx, *, user_request):
    api_input = user_request.replace(' ', '_') # Take and stores user_input, replacing spaces with underscores to match API's format
    try:
        result_json_str_from_api = compendium().get_entry(api_input) # Takes and matches formatted user input with compendium data, gets data and stores it
    except Exception as ex:
        await ctx.send(f'"{user_request}" not found in Compendium. Please check spelling and try again.')
        return

    json_from_api = json.loads(json.dumps(result_json_str_from_api)) # Encodes matched and retrieved data into json via dumps, then loads it and stores it

    # Create embed object, adding content from API gotten from above

    embed = discord.Embed(title = f"**{json_from_api['name'].title()}**", url = 'https://zelda.fandom.com/wiki/The_Legend_of_Zelda:_Breath_of_the_Wild', color = 0x60f8fd)
    embed.set_thumbnail(url = json_from_api['image']) # Taking embed object and with method adding a thumbnail - image url parsed and taken from API's json data
    properties_to_not_include = ['id', 'name', 'image', 'description']
    for prop in json_from_api:
        if prop not in properties_to_not_include:
            formatted_value = await validate_prop_and_get_formatted_value(json_from_api[prop])
            if formatted_value is None:
                print(f"Unexpected type. Type = {type(json_from_api[prop])}")
                await ctx.send("Unexpected error! Please try again.")
                return
            embed.add_field(name = prop.replace('_', ' ').title(), value = formatted_value.title(), inline = True)

    embed.add_field(name = "Description", value = json_from_api['description'], inline = False) # Adds description field to embed object - value data parsed and taken from API's json data
    await ctx.send(embed = embed) # Awaits and sends embed back to channel where user called command 

async def validate_prop_and_get_formatted_value(json_prop_value):
    type_returned_from_prop = type(json_prop_value)
    
    if type_returned_from_prop == type(None):
        formatted_value = "N/A"
    elif type_returned_from_prop in [int, float, complex]:
        formatted_value = str(json_prop_value)
    elif type_returned_from_prop == list:
        if len(json_prop_value) == 0:
            formatted_value = "N/A"
        else:
            formatted_value = "\n".join(json_prop_value)
    elif type_returned_from_prop == str:
        if json_prop_value == '':
            formatted_value = 'N/A'
        else:
            formatted_value = json_prop_value
    else:
        formatted_value = None

    return formatted_value
# Run the bot using its token from config.py for security

client.run(config.token)