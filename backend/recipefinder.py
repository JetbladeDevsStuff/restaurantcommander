import requests
import string

def get_all_recipes():
    recipes = {}

    for letter in string.ascii_lowercase:
        url = f"https://www.themealdb.com/api/json/v1/1/search.php?f={letter}"
        response = requests.get(url)
        data = response.json()

        if data["meals"]:
            for meal in data["meals"]:
                recipes[meal["idMeal"]] = {
                    "id": meal["idMeal"],
                    "name": meal["strMeal"],
                    "thumbnail": meal["strMealThumb"]
                }

    return list(recipes.values())

# Example usage
recipes = get_all_recipes()
print("Total recipes:", len(recipes))
print(recipes[:5])  # first 5 recipes
