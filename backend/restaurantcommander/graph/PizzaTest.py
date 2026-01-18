
recipe_name = "Pizza Express Margherita"
recipe_json = get_recipe_by_name(recipe_name)

if recipe_json:
    print("Recipe JSON ready for AI:\n")
    print(json.dumps(recipe_json, indent=2)) 