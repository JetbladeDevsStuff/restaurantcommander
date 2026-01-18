import os
from typing import List
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv

load_dotenv()

from .manualimport import graph_from_dict  # no leading dot


class GraphEdgeModel(BaseModel):
    u: int
    v: int
    process: str


class GraphNodeModel(BaseModel):
    id: int
    ingredient: str
    is_original: bool
    is_final: bool


class GraphDictModel(BaseModel):
    name: str
    nodes: List[GraphNodeModel]
    edges: List[GraphEdgeModel]


SYSTEM_RULES = """Convert the recipe into a directed graph JSON.

Return ONLY JSON with exactly:
- name: string
- nodes: [{id, ingredient, is_original, is_final}]
- edges: [{u, v, process}]

Rules:
- Nodes are ingredient STATES (raw -> prepped -> cooked -> finished).
- Each edge is ONE instruction step transforming u -> v (put the step text in process).
- Node ids must be 0..n-1 with no gaps.
- Mark raw inputs is_original=true.
- Mark final dish is_final=true.
- No markdown, no extra text.
"""


async def graph_from_description_ai(description: str):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing GEMINI_API_KEY. Put it in a .env file or set it in your terminal.")

    async with genai.Client(api_key=api_key).aio as client:
        response = await client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{SYSTEM_RULES}\n\nRECIPE:\n{description}",
            config={
                "response_mime_type": "application/json",
                "response_json_schema": GraphDictModel.model_json_schema(),
            },
        )

    graph_model = GraphDictModel.model_validate_json(response.text)
    return graph_from_dict(graph_model.model_dump())

