from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq


""" findInstructions(link)

Web scrapes for the name, ingredients, and directions of the recipe tied to
the parameterized link.

Parameters:
    link (string): The URL addon to the 'foodnetwork.com' website

Returns:
    list: Title, image, ingredients, and steps of a recipe. 
"""


def findInstructions(link):
    instructions = mainSearch(link)
    ingredients = findIngredients(instructions)
    steps = findSteps(instructions)
    image = instructions.find('img',
                              class_=['m-MediaBlock__a-Image a-Image'])['src']
    title = instructions.find('span',
                              class_=['o-AssetTitle__a-HeadlineText']).text
    return [ingredients, steps, image, title]


""" mainSearch(link)

Scrapes the entire content from the respective website for the recipe.

Parameters:
    link (string): The URL addon to the 'foodnetwork.com' website

Returns:
    soup(): Navigatable DOM 
"""


def mainSearch(link):
    URL = 'https://www.foodnetwork.com/recipes/{}'.format(link)
    uClient = uReq(URL)
    html = uClient.read()
    uClient.close()
    return soup(html, 'html.parser')


""" findIngredients(instructions)

Scrapes the DOM for the recipe ingredients.

Parameters:
    instructions (soup()): Navigatable DOM

Returns:
    list: Recipe ingredients.
"""

def findIngredients(instructions):
    allIngredients = instructions.find('div', class_=['o-Ingredients__m-Body'])
    unfilteredIngredients = allIngredients.contents[5:]
    filteredIngredients = []
    for section in unfilteredIngredients:
        name = section.name
        
        if name == 'h6':
            content = section
        elif name == 'p':
            print(len(content))
            content = section.find('label')
            content = content.find('span', class_=['o-Ingredients__a-Ingredient--CheckboxLabel'])
        else:
            continue
            
        filteredIngredients.append({
            'type': name,
            'content': content.text.replace('\n', '').strip()
        })
    return filteredIngredients


""" findSteps(instructions)

Scrapes the DOM for the recipe instructions.

Parameters:
    instructions (soup()): Navigatable DOM

Returns:
    list: Recipe instructions.
"""


def findSteps(instructions):
    unfilteredSteps = instructions.find_all('li', class_=['o-Method__m-Step'])
    filteredSteps = []
    for step in unfilteredSteps:
        filteredSteps.append(step.text.replace('\n', '').strip())
    return filteredSteps
