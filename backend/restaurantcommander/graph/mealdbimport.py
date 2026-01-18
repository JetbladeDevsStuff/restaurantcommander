import requests

from . import Graph
from .aiimport import graph_from_description_ai

def get_recipe_by_name(name):
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={name.replace(' ', '%20')}"
    response = requests.get(url)
    data = response.json()

    if not data["meals"]:
        raise RuntimeError(f"Recipe \"{name}\" not found.")

    meal = data["meals"][0]

    ingredients = []
    for i in range(1, 21):
        ingredient = meal.get(f"strIngredient{i}")
        measure = meal.get(f"strMeasure{i}")
        if ingredient and ingredient.strip():
            ingredients.append({
                "name": ingredient.strip(),
                "amount": measure.strip() if measure else ""
            })

    ai_ready_json = {
        "recipe_id": meal["idMeal"],
        "title": meal["strMeal"],
        "category": meal.get("strCategory"),
        "cuisine": meal.get("strArea"),
        "ingredients": ingredients,
        "instructions": meal.get("strInstructions"),
        "tasks": []
    }
    return ai_ready_json

async def graph_from_mealdb(name: str) -> Graph:
    recipe = get_recipe_by_name(name)
    return await graph_from_description_ai(recipe["instructions"])
