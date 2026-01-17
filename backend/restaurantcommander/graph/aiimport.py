# import from ai

import openrouter
import os

async def graph_from_description_ai(description: str):
    async with openrouter.OpenRouter(api_key=os.getenv("OPENROUTER_API_KEY")) as client:
        

