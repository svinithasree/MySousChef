from langchain_core.prompts import ChatPromptTemplate

ingredient_categorizer_prompt = ChatPromptTemplate.from_template("""
You are a helpful kitchen assistant. The user has listed their available ingredients in no particular order.
Categorize them into: Vegetables, Fruits, Grains, Dairy, Proteins, Spices, Other.

Ingredients listed: {raw_ingredients}

Return a clean JSON object like:
{{
  "Vegetables": ["spinach", "onion"],
  "Fruits": ["apple"],
  "Grains": ["rice", "wheat flour"],
  "Dairy": ["milk", "paneer"],
  "Proteins": ["lentils", "chickpeas"],
  "Spices": ["cumin", "turmeric"],
  "Other": ["oil", "salt"]
}}
Return ONLY the JSON, no explanation.
""")

meal_plan_prompt = ChatPromptTemplate.from_template("""
You are MySousChef, an expert meal planner for an Indian vegetarian family of 3 (2 adults, 1 teenager).

Available ingredients:
{ingredients}

Available recipes from the recipe book:
{recipes}

Today is Saturday. Create a 7-day vegetarian meal plan (Sunday to Saturday) with:
- Breakfast
- Lunch  
- Evening Snack
- Dinner

Rules:
1. Only use VEGETARIAN recipes
2. Match meals to available ingredients as closely as possible
3. Each day should have a good balance of protein, fiber, and carbs
4. Estimate nutrients for each meal (High/Medium/Low for Protein, Fiber, Carbs)
5. Prefer recipes from the recipe book. You may suggest simple extras if needed.
6. Variety is important — don't repeat the same meal more than twice in a week

Return ONLY a JSON object in this exact format:
{{
  "Sunday": {{
    "Breakfast": {{"recipe": "Name", "link": "url or N/A", "protein": "High/Medium/Low", "fiber": "High/Medium/Low", "carbs": "High/Medium/Low"}},
    "Lunch": {{"recipe": "Name", "link": "url or N/A", "protein": "High/Medium/Low", "fiber": "High/Medium/Low", "carbs": "High/Medium/Low"}},
    "Evening Snack": {{"recipe": "Name", "link": "url or N/A", "protein": "High/Medium/Low", "fiber": "High/Medium/Low", "carbs": "High/Medium/Low"}},
    "Dinner": {{"recipe": "Name", "link": "url or N/A", "protein": "High/Medium/Low", "fiber": "High/Medium/Low", "carbs": "High/Medium/Low"}}
  }},
  "Monday": {{ ... }},
  "Tuesday": {{ ... }},
  "Wednesday": {{ ... }},
  "Thursday": {{ ... }},
  "Friday": {{ ... }},
  "Saturday": {{ ... }}
}}
Return ONLY the JSON. No extra text.
""")
