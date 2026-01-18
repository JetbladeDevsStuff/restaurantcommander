from fastapi import FastAPI
from pydantic import AnyHttpUrl, BaseModel, TypeAdapter
from dotenv import load_dotenv

from restaurantcommander.chef import Chef

from .state import State
from .graph.manualimport import GraphDict, graph_from_dict
from .graph.aiimport import graph_from_description_ai

import networkx

app = FastAPI()
curstate = State()

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
load_dotenv()


@app.get("/")
def read_root():
    return {"message": "Recipe Task Tracker running!"}


# @app.get("/user/{user_id}")
# def read_user(user_id: int, item_id: str):
#     # Initialize user progress if not set
#     if user_id not in user_progress:
#         user_progress[user_id] = 0
#
#     # Get that user's tasks (mock AI JSON)
#     user_tasks = recipe_data["tasks"].get(user_id, [])
#     if not user_tasks:
#         return {"error": "No tasks for this user"}
#
#     current_index = user_progress[user_id]
#     current_step = user_tasks[current_index]
#     next_steps = user_tasks[current_index + 1:]
#
#     progress = f"{current_index + 1}/{len(user_tasks)}"
#
#     return {
#         "user_id": user_id,
#         "recipe_title": recipe_data["recipe_title"],
#         "current_step": current_step,
#         "next_steps": next_steps,
#         "progress": progress
#     }


# @app.post("/user/{user_id}/complete_step")
# def complete_step(user_id: int, item_id: str):
#     # Mark step complete for user
#     if user_id in user_progress:
#         user_progress[user_id] += 1
#     return {"message": "Step completed!", "user_progress": user_progress[user_id]}


@app.post("/user/{user_id}/username")
def set_username(user_id: int, username: str):
    curstate.chefs[user_id].name = username



@app.post("/user/new")
def make_user():
    curstate.chefs.append(Chef())

class SetManual(BaseModel):
    # image: AnyHttpUrl
    recipe: GraphDict


@app.post("/recipe/set/manual")
def recipe_set_manual(recipe: SetManual):
    curstate.recipe = graph_from_dict(recipe.recipe)


class SetAI(BaseModel):
    # name: str
    description: str
    # image: AnyHttpUrl

@app.post("/recipe/set/ai")
async def recipe_set_ai(model: SetAI):
    curstate.recipe = await graph_from_description_ai(model.description)
    # curstate.recipe.name = model.name
    # curstate.recipe.image = model.image


@app.get("/recipe/visualize")
async def recipe_visualize() -> str:
    namedgraph = networkx.relabel_nodes(curstate.recipe.graph, {node: curstate.recipe.nodes[node].ingredient for node in curstate.recipe.graph.nodes})
    return networkx.nx_pydot.to_pydot(namedgraph).to_string()
