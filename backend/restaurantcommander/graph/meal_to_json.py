import requests
import json

def get_recipe_by_name(name):
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={name.replace(' ', '%20')}"
    response = requests.get(url)
    data = response.json()

    if not data["meals"]:
        print("Recipe not found.")
        return None

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
        "image": meal.get("strMealThumb"),
        "tasks": []
    }
    return ai_ready_json

# -----------------------------
# Interactive input
recipe_name = input("Enter the recipe name: ")
recipe_json = get_recipe_by_name(recipe_name)

if recipe_json:
    print("Recipe JSON ready for AI:\n")
    print(json.dumps(recipe_json, indent=2))

    # Optional: save to file
    with open("recipe.json", "w", encoding="utf-8") as f:
        json.dump(recipe_json, f, indent=2, ensure_ascii=False)
    print("\nRecipe JSON saved to recipe.json")
