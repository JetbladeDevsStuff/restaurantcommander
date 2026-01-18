import requests

def get_recipe_by_name(name):
    # Replace spaces with %20 for URL encoding
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={name.replace(' ', '%20')}"
    response = requests.get(url)
    data = response.json()

    if not data["meals"]:
        print("Recipe not found.")
        return None

    meal = data["meals"][0]  # take the first match

    # Extract ingredients and measures
    ingredients = []
    for i in range(1, 21):  # MealDB has 20 ingredient slots
        ingredient = meal.get(f"strIngredient{i}")
        measure = meal.get(f"strMeasure{i}")
        if ingredient and ingredient.strip():
            ingredients.append(f"{ingredient.strip()} - {measure.strip()}")

    # Build result
    recipe_info = {
        "id": meal["idMeal"],
        "name": meal["strMeal"],
        "category": meal.get("strCategory"),
        "area": meal.get("strArea"),
        "instructions": meal.get("strInstructions"),
        "ingredients": ingredients,
        "image": meal.get("strMealThumb")
    }

    return recipe_info

# Example usage
recipe_name = "Pizza Express Margherita"
recipe = get_recipe_by_name(recipe_name)

if recipe:
    print(f"Recipe: {recipe['name']}")
    print(f"Category: {recipe['category']}")
    print(f"Cuisine: {recipe['area']}")
    print("Ingredients:")
    for item in recipe["ingredients"]:
        print(f"  - {item}")
    print("\nInstructions:")
    print(recipe["instructions"])
    print("\nImage URL:", recipe["image"])
