import json
from typing import NamedTuple, List, Dict, Optional

from flask import Flask, render_template
app = Flask(__name__)


class Ingredient(NamedTuple):
    iid: int
    name: str
    unit: Optional[str]
    image: str


with open('./data/ingredient.json') as f:
    ingredients = {data['iid']: Ingredient(**data) for data in json.load(f)}


class RecipeIngredient(NamedTuple):

    iid: int
    count: Optional[int]
    weight: Optional[int]
    comment: Optional[str]

    @property
    def ingredient(self):
        return ingredients[self.iid]


class Procedure(NamedTuple):
    step: int
    image: str
    timer: Optional[int]
    description: List[str]


class Recipe(NamedTuple):
    id: int
    name: str
    level: int
    image_url: str
    ingredient_image: str
    ingredients: RecipeIngredient
    procedures: List[Procedure]

    @classmethod
    def load(cls, d):
        d['ingredients'] = [RecipeIngredient(**data) for data in d['ingredients']]
        d['procedures'] = [Procedure(**data) for data in d['procedures']]
        return cls(**d)


with open('./data/recipes.json') as f:
    recipes_data = json.load(f)
    recipes = {data['id']: Recipe.load(data) for data in recipes_data}


@app.route('/')
def top():
    context = dict(
        recipes=recipes
    )
    return render_template('top.html', **context)


@app.route('/recipe/<int:rid>/ingredient')
def ingredient(rid: int):
    recipe = recipes.get(rid)
    context = dict(
        current_step=1,
        max_step=1 + len(recipe.procedures),
        recipe=recipes.get(rid),
        active_ri_idx=0,
    )
    return render_template('ingredient.html', **context)


@app.route('/recipe/<int:rid>/procedures/<int:step_id>')
def procedure(rid: int, step_id: int):
    recipe = recipes.get(rid)
    current_procedure = recipe.procedures[step_id - 1]
    try:
        next_procedure = recipe.procedures[step_id]
    except IndexError:
        next_procedure = None
    context = dict(
        current_step=step_id + 1,
        max_step=1 + len(recipe.procedures),
        recipe=recipes.get(rid),
        current_procedure=current_procedure,
        next_procedure=next_procedure
    )
    return render_template('procedure.html', **context)


if __name__ == '__main__':
    app.run()
