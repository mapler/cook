import json
from typing import NamedTuple, List, Optional


class Ingredient:

    def __init__(self, iid, name, image, unit=None):
        self.iid = iid
        self.name = name
        self.image = image
        self.unit = unit


with open('./data/ingredient.json') as f:
    ingredients = {data['iid']: Ingredient(**data) for data in json.load(f)}


class RecipeIngredient:

    def __init__(self, iid, count=None, weight=None, comment=None):
        self.iid = iid
        self.count = count
        self.weight = weight
        self.comment = comment

    @property
    def ingredient(self):
        return ingredients[self.iid]


class Action:

    def __init__(self, image, timer=None, description=None):
        self.image = image
        self.timer = timer
        self.description = description


class Procedure:

    def __init__(self, step, actions=None):
        self.step = step
        self.actions = actions

    @classmethod
    def load(cls, d):
        d['actions'] = [Action(**data) for data in d['actions']]
        return cls(**d)


class Recipe:

    def __init__(self, id, name, level, image_url, ingredient_image, ingredients, procedures):
        self.id = id
        self.name = name
        self.level = level
        self.image_url = image_url
        self.ingredient_image = ingredient_image
        self.ingredients = ingredients
        self.procedures = procedures

    @classmethod
    def load(cls, d):
        d['ingredients'] = [RecipeIngredient(**data) for data in d['ingredients']]
        d['procedures'] = [Procedure.load(data) for data in d['procedures']]
        return cls(**d)


with open('./data/recipes.json') as f:
    recipes = {data['id']: Recipe.load(data) for data in json.load(f)}
