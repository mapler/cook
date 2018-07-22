import json
from typing import NamedTuple, List, Optional


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
    recipes = {data['id']: Recipe.load(data) for data in json.load(f)}
