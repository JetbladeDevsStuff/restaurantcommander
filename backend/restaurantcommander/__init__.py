from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from dotenv import load_dotenv


from .state import State
from .graph.manualimport import GraphDict, graph_from_dict
from .graph.aiimport import graph_from_description_ai
from .chef import create_stepgraph, split_graph_among_chefs, topo_layers
from .graph.mealdbimport import graph_from_mealdb
from .chef import Chef

import networkx

app = FastAPI()
curstate = State()

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


@app.get("/user/{user_id}")
def get_user(user_id: int):
    if user_id > len(curstate.chefs):
        raise HTTPException(status_code=404, detail="user_id not found")
    name = curstate.chefs[user_id].name
    return {"user_id": user_id, "username": name}


@app.get("/user/{user_id}/tasks")
def get_user_tasks(user_id: int):
    if user_id < 0 or user_id >= len(curstate.chefs):
        raise HTTPException(status_code=404, detail="user_id not found")
    return curstate.chefs[user_id].tasks

class SetUsername(BaseModel):
    username: str

@app.post("/user/{user_id}/username")
def set_username(user_id: int, username: SetUsername):
    if user_id < 0 or user_id >= len(curstate.chefs):
        raise HTTPException(status_code=404, detail="user_id not found")
    curstate.chefs[user_id].name = username.username


@app.post("/user/new")
def make_user():
    curstate.chefs.append(Chef())
    id = len(curstate.chefs) - 1
    curstate.chefs[id].name = f"Chef {id}"
    recipe_split_to_chefs()
    return {"user_id": id, "username": f"Chef {id}"}


@app.delete("/user/delete")
def delete_user():
    if not curstate.chefs:
        raise HTTPException(status_code=404, detail="No users")
    chef = curstate.chefs.pop()
    recipe_split_to_chefs()
    return {"user_id": len(curstate.chefs), "username": chef.name}


class SetManual(BaseModel):
    # image: AnyHttpUrl
    recipe: GraphDict


# Updates curstate.chefs with the new recipe
def recipe_split_to_chefs():
        num_chefs = len(curstate.chefs)
        if num_chefs == 0:
            return
        split_graph_among_chefs(curstate.recipe, curstate.chefs)


@app.post("/recipe/set/manual")
def recipe_set_manual(recipe: SetManual):
    curstate.recipe = graph_from_dict(recipe.recipe)
    recipe_split_to_chefs()


class SetAI(BaseModel):
    # name: str
    description: str
    # image: AnyHttpUrl

@app.post("/recipe/set/ai")
async def recipe_set_ai(model: SetAI):
    curstate.recipe = await graph_from_description_ai(model.description)
    recipe_split_to_chefs()
    # curstate.recipe.name = model.name
    # curstate.recipe.image = model.image

class SetMealDB(BaseModel):
    name: str


@app.post("/recipe/set/mealdb")
async def recipe_set_mealdb(name: SetMealDB):
    # TODO: This
    try:
        recipe_graph = await graph_from_mealdb(name.name)
    except RuntimeError as e:
            raise HTTPException(status_code=404, detail=str(e))
    curstate.recipe = recipe_graph
    recipe_split_to_chefs()
    


@app.get("/recipe")
def recipe():
    return {"name": curstate.recipe.name}


@app.get("/recipe/visualize", response_class=PlainTextResponse)
def recipe_visualize():
    # TODO: get edges here?
    namedgraph = networkx.relabel_nodes(curstate.recipe.graph, {node: curstate.recipe.nodes[node].ingredient for node in curstate.recipe.graph.nodes})
    return networkx.nx_pydot.to_pydot(namedgraph).to_string()


@app.get("/recipe/visualize/stepgraph", response_class=PlainTextResponse)
def recipe_visualize_stepgraph():
    stepgraph = create_stepgraph(curstate.recipe)
    return networkx.nx_pydot.to_pydot(stepgraph).to_string()


@app.get("/recipe/visualize/topo")
def recipe_visualize_topograph():
    stepgraph = create_stepgraph(curstate.recipe)
    return topo_layers(stepgraph)

