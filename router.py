from optionScraper import findRecipes
from recipeScraper import findInstructions
from flask import Flask, render_template
app = Flask(__name__)


""" index()

Parameters:
    None

Returns:
    Mainpage of the 'Food.ly' website.
"""


@app.route('/')
def index():
    return render_template('index.html')


""" search(form)

Parameters:
    form (string): User recipe search.

Returns:
    Page with the possible recipes found from user search.
"""


@app.route('/search/<form>')
def search(form):
    recipes = findRecipes(form)
    if len(recipes) == 0:
        return render_template('null.html')
    return render_template('options.html', recipes=recipes)


""" recipe(link)

Parameters:
    link: 'foodnetwork.com' url extension for chosen recipe.

Returns:
    Interactive recipe layout for chosen recipe.
"""


@app.route('/recipe/<path:link>')
def recipe(link):
    ingredients, steps, image, title = findInstructions(link)
    return render_template('recipe.html', ingredients=ingredients,
                           steps=steps, image=image, title=title)


if __name__ == '__main__':
    app.run(debug=True)
