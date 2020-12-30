from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import re


""" findRecipes(search)

Gathers general background information about the most popular recipes from
'foodnetwork.com'.

Parameters:
    search (string): URL formatted user search.

Returns:
    list: A list of general background information for each
    recipe present within the first 3 pages of Food Network.
"""


def findRecipes(search):
    recipes = mainSearch(search)
    filteredRecipes = []
    for recipe in recipes:
        try:
            data = locateData(recipe)
            filteredData = filterData(data)
            filteredRecipes.append(filteredData)
        except (AttributeError, TypeError, ValueError):
            pass
    return filteredRecipes


""" mainSearch(search)

Web scrapes from the 'foodnetwork.com' website and separates content by recipe.

Parameters:
    search (string): URL formatted user search.

Returns:
    list: The 'foodnetwork.com' website separated into sections based on each
    recipe.
"""


def mainSearch(search):
    recipes = []
    search = search.strip().replace(' ', '-') + '-'
    templateURL = 'https://www.foodnetwork.com/search/{}/p/'.format(search)
    for count in range(1, 4):
        URL = templateURL + str(count)
        uClient = uReq(URL)
        html = uClient.read()
        uClient.close()
        page = soup(html, 'html.parser')
        recipes.extend(page.find_all('section', class_=['o-ResultCard']))
    return recipes


""" locateData(recipe)

Parses the information based on the recipe DOM into a dictionary.

Parameters:
    recipe (string): The HTML containing background data for a single recipe.

Returns:
    object: The DOM parsed into an object.
"""


def locateData(recipe):
    return {
        'link': recipe.find('h3',
                            class_=['m-MediaBlock__a-Headline']).a['href'],
        'header': recipe.find('span',
                              class_=['m-MediaBlock__a-HeadlineText']).text,
        'creator': recipe.find('span',
                               class_=['m-Info__a-AssetInfo']).text,
        'rating': recipe.find('span',
                              class_=['gig-rating-stars'])['title'],
        'ratingCount': recipe.find('span',
                                   class_=['gig-rating-ratingsum']).text,
        'timeText': recipe.find('dd',
                                class_=['o-RecipeInfo__a-Description']).text,
        'img': recipe.find('img',
                                class_=['m-MediaBlock__a-Image'])['src']
    }


""" filterData(recipe)

Further parses data by cleaning up the content contained from 'locateData()'.

Parameters:
    data (object): The object containing raw DOM content.

Returns:
    object: The cleaned DOM content from 'data'.
"""


def filterData(data):
    timeSplit = re.split('hour.', data['timeText'].replace('minutes', ''))
    time = int(timeSplit[0]) * 60 + int(timeSplit[0])
    return {
        'link': data['link'][30:],
        'header': data['header'].strip(),
        'creator': data['creator'].strip(),
        'rating': float(data['rating'].replace('of 5 stars', '')),
        'ratingCount': int(data['ratingCount'].replace(' Reviews', '')),
        'timeText': data['timeText'],
        'time': time,
        'img': data['img']
    }
