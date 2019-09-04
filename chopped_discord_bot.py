#!/usr/bin/python3
# Created by Frank Steves
# Licensed for use in the GNU GPL v3.0 license.  Additional details can be found in the COPYING file with this software.
# Description:  This allows you to roll for ingredients based on real based used on the show Chopped by the Food Network
# Note: If for some reason the Wikipedia page changes the format, this will break in a bad way!
#

import random, re, requests, sys, operator, argparse
from collections import OrderedDict
from bs4 import BeautifulSoup
import random
import asyncio
import aiohttp
import json
from discord import Game
from discord.ext.commands import Bot
from discord.ext import commands

BOT_PREFIX = ("?", "!")
TOKEN = ''

client = Bot(command_prefix=BOT_PREFIX)

wikiepisodes = ['https://en.wikipedia.org/wiki/List_of_Chopped_episodes_(seasons_1%E2%80%9320)', 'https://en.wikipedia.org/wiki/List_of_Chopped_episodes']

basket = OrderedDict()

#This builds our basket dict of dicts
def buildBasket():

    basketnum = 0

    for episodeset in range(len(wikiepisodes)):

        page = requests.get(wikiepisodes[episodeset])
        soup = BeautifulSoup(page.text, 'html.parser')

        for a in soup.findAll('li'):
            for b in re.findall("^Appetizer:(.*$)", a.text):
                if b:
                    basketnum += 1
                    basket[basketnum] = OrderedDict()
                    basket[basketnum]['appetizer'] = b
            for b in re.findall("^Entrée:(.*$)", a.text):
                if b:
                    basket[basketnum]['entree'] = b
            for b in re.findall("^Dessert:(.*$)", a.text):
                if b:
                    basket[basketnum]['dessert'] = b

def returnBasket():

    basketid = random.randint(1, len(basket))

    for course in (basket[basketid]):
        if course == 'appetizer':
            app = (course + ":" + basket[basketid][course] + "\n")
    for course in (basket[basketid]):
        if course == 'entree':
            ent = (course + ":" + basket[basketid][course] + "\n")
    for course in (basket[basketid]):
        if course == 'dessert':
            des = (course + ":" + basket[basketid][course] + "\n")

    basketcontents = "```Basket #" + str(basketid) + "\n" + app + ent + des + "```"
    return basketcontents

def returnCourse(courselist):

    basketid = random.randint(1, len(basket))

    for course in (basket[basketid]):
        if course == 'appetizer' and courselist == 'appetizer':
            return ("```Basket #" + str(basketid) + "\n" + course + ":" + basket[basketid][course] + "\n```")
    for course in (basket[basketid]):
        if course == 'entree' and courselist == 'entree':
            return ("```Basket #" + str(basketid) + "\n" + course + ":" + basket[basketid][course] + "\n```")
    for course in (basket[basketid]):
        if course == 'dessert' and courselist == 'dessert':
           return ("```Basket #" + str(basketid) + "\n" + course + ":" + basket[basketid][course] + "\n```")


#Initialize our basket from the webscrape
buildBasket()

client = Bot(command_prefix=BOT_PREFIX)
@commands.cooldown(1, 10, commands.BucketType.user)
@client.command(name='chopped',
                description="Chopped show ingredient list!",
                brief="Rolls for random ingredients.",
                aliases=['ingredients', 'roll'],
                pass_context=True)
async def roll_ingredients(context):
    await client.say(returnBasket())

@commands.cooldown(1, 10, commands.BucketType.user)
@client.command(name='appetizer',
                description="Chopped show appetizer!",
                brief="Rolls for random appetizer.",
                aliases=['apps', 'app', 'appetizers'],
                pass_context=True)
async def roll_apps(context):
    await client.say(returnCourse("appetizer"))

@commands.cooldown(1, 10, commands.BucketType.user)
@client.command(name='entree',
                description="Chopped show entree!",
                brief="Rolls for random entree.",
                aliases=['ents', 'ent', 'entrees'],
                pass_context=True)
async def roll_ents(context):
    await client.say(returnCourse("entree"))

@commands.cooldown(1, 10, commands.BucketType.user)
@client.command(name='dessert',
                description="Chopped show dessert!",
                brief="Rolls for random dessert.",
                aliases=['des', 'desserts', 'desert', 'deserts'],
                pass_context=True)
async def roll_des(context):
    await client.say(returnCourse("dessert"))

async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)


client.loop.create_task(list_servers())
client.run(TOKEN)
