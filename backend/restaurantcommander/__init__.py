from fastapi import FastAPI

app = FastAPI()

# Draft AI-generated recipe data (mock)
recipe_data = {
    "recipe_title": "Pizza Express Margherita",
    "tasks": {
        "user_001": [
            "Spread passata on dough",
            "Add mozzarella and seasoning",
            "Preheat oven",
            "Bake pizza"
        ],
        "user_002": [
            "Prepare dough",
            "Chop basil",
            "Arrange toppings"
        ]
    }
}

# Track user progress
user_progress = {}

@app.get("/")
def read_root():
    return {"message": "Recipe Task Tracker running!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.get("/items/{item_id}/user/{user_id}")
def read_user(user_id: str, item_id: str):
    # Initialize user progress if not set
    if user_id not in user_progress:
        user_progress[user_id] = 0

    # Get that user's tasks (mock AI JSON)
    user_tasks = recipe_data["tasks"].get(user_id, [])
    if not user_tasks:
        return {"error": "No tasks for this user"}

    current_index = user_progress[user_id]
    current_step = user_tasks[current_index]
    next_steps = user_tasks[current_index + 1:]

    progress = f"{current_index + 1}/{len(user_tasks)}"

    return {
        "user_id": user_id,
        "recipe_title": recipe_data["recipe_title"],
        "current_step": current_step,
        "next_steps": next_steps,
        "progress": progress
    }

@app.post("/items/{item_id}/user/{user_id}/complete_step")
def complete_step(user_id: str, item_id: str):
    # Mark step complete for user
    if user_id in user_progress:
        user_progress[user_id] += 1
    return {"message": "Step completed!", "user_progress": user_progress[user_id]}
