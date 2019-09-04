#!/usr/bin/python3
# Created by Frank Steves
# Licensed for use in the GNU GPL v3.0 license.  Additional details can be found in the COPYING file with this software.
# Description:  This allows you to roll for ingredients based on real based used on the show Chopped by the Food Network
# Note: If for some reason the Wikipedia page changes the format, this will break in a bad way!
#

import random, re, requests, sys, operator, argparse
from collections import OrderedDict
from bs4 import BeautifulSoup

wikiepisodes = ['https://en.wikipedia.org/wiki/List_of_Chopped_episodes_(seasons_1%E2%80%9320)', 'https://en.wikipedia.org/wiki/List_of_Chopped_episodes']

parser = argparse.ArgumentParser()

parser.add_argument("-r", "--random", help="Randomizes the basket selections (Select a course below)", action="store_true", default=False)
parser.add_argument("-a", "--appetizer", help="List only the appetizer ingredients", action="store_true", default=False)
parser.add_argument("-e", "--entree", help="List only the entree ingredients", action="store_true", default=False)
parser.add_argument("-d", "--dessert", help="List only the dessert ingredients", action="store_true", default=False)

args = parser.parse_args()

basket = OrderedDict()

#This will print out the list of ingredients based on the basketID
def printIngredients(basket, basketid, course):
    if course:
        print(course, " ", basket[basketid][course])
    else:
        for course in basket[basketid]:
            print(course, " ", basket[basketid][course])

def printBasket(basket, basketid):

    if not args.appetizer and not args.entree and not args.dessert:
        args.appetizer=True
        args.entree=True
        args.dessert=True

    print("Basket #", basketid)

    if args.appetizer:
        for course in (basket[basketid]):
            if course == 'appetizer':
                printIngredients(basket, basketid, course)

    if args.entree:
        for course in (basket[basketid]):
            if course == 'entree':
                printIngredients(basket, basketid, course)

    if args.dessert:
        for course in (basket[basketid]):
            if course == 'dessert':
                printIngredients(basket, basketid, course)

#This builds our basket dict of dicts
def buildBasket():

    basketnum = 0

    for episodeset in range(len(wikiepisodes)):
        print (wikiepisodes[episodeset])

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

#Run the list of ingredients, taking into account args, and print the results to the screen
def rollBasket():
    if args.random:
        basketid = random.randint(1, len(basket))
        printBasket(basket, basketid)
    else:
        for basketid in basket:
            printBasket(basket, basketid)

#Initialize our basket from the webscrape
buildBasket()
#Rull the dice and see what we get!
rollBasket()
