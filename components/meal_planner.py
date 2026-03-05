import json
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from prompts.meal_plan_prompt import ingredient_categorizer_prompt, meal_plan_prompt


def get_llm(api_key: str):
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.6,
        google_api_key=api_key
    )


def categorize_ingredients(raw_ingredients: str, api_key: str) -> dict:
    """Use Gemini to categorize raw ingredient text into structured categories."""
    llm = get_llm(api_key)
    chain = ingredient_categorizer_prompt | llm | StrOutputParser()
    result = chain.invoke({"raw_ingredients": raw_ingredients})
    try:
        cleaned = re.sub(r"```json|```", "", result).strip()
        return json.loads(cleaned)
    except Exception:
        return {"All Ingredients": raw_ingredients}


def generate_meal_plan(categorized_ingredients: dict, recipes_text: str, api_key: str) -> dict:
    """Use Gemini to generate a full weekly meal plan."""
    llm = get_llm(api_key)
    chain = meal_plan_prompt | llm | StrOutputParser()

    ingredients_text = "\n".join(
        [f"{cat}: {', '.join(items)}" for cat, items in categorized_ingredients.items()]
    )

    result = chain.invoke({
        "ingredients": ingredients_text,
        "recipes": recipes_text
    })

    try:
        cleaned = re.sub(r"```json|```", "", result).strip()
        return json.loads(cleaned)
    except Exception as e:
        raise ValueError(f"Could not parse meal plan from Gemini response: {e}\n\nRaw response:\n{result}")
