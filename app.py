import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import os
import json
import pandas as pd
from components.voice_input import ingredient_input_section
from components.meal_planner import categorize_ingredients, generate_meal_plan
from components.excel_handler import load_recipes, format_recipes_for_prompt, generate_meal_plan_excel

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MySousChef",
    page_icon="🍽️",
    layout="wide"
)

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-title { font-size: 2.5rem; font-weight: 800; color: #2E4057; text-align: center; }
    .subtitle { font-size: 1.1rem; color: #666; text-align: center; margin-bottom: 2rem; }
    .section-header { font-size: 1.3rem; font-weight: 700; color: #2E4057; margin-top: 1.5rem; }
    .meal-card { background: #f8f9fa; border-radius: 10px; padding: 1rem; margin: 0.5rem 0; border-left: 4px solid #4F81BD; }
    .nutrient-badge { display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; margin: 2px; }
    .stButton > button { background-color: #2E4057; color: white; border-radius: 8px; padding: 0.5rem 2rem; font-weight: bold; }
    .stButton > button:hover { background-color: #4F81BD; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">🍽️ MySousChef</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your AI-powered weekly meal planner for the family</div>', unsafe_allow_html=True)
st.divider()

# ── Sidebar: API Key + Recipe Upload ─────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/color/96/chef-hat.png", width=80)
    st.markdown("### ⚙️ Settings")

    api_key = os.environ.get("GOOGLE_API_KEY", "")
    if not api_key:
        st.error("⚠️ GOOGLE_API_KEY not found in .env file. Please add it and restart the app.")

    st.divider()
    st.markdown("### 📂 Recipe Book")
    uploaded_recipe = st.file_uploader("Upload your recipes.xlsx", type=["xlsx"])

    recipe_path = "data/recipes.xlsx"
    if uploaded_recipe:
        with open("data/uploaded_recipes.xlsx", "wb") as f:
            f.write(uploaded_recipe.read())
        recipe_path = "data/uploaded_recipes.xlsx"
        st.success("✅ Recipe book loaded!")
    else:
        st.info("Using sample recipe book. Upload yours above.")

    st.divider()
    st.markdown("### 👨‍👩‍👧 Family")
    st.markdown("👨 Adult · 👩 Adult · 🧑 Teen")
    st.caption("Meal portions are planned for 3 people")

# ── Main flow ─────────────────────────────────────────────────────────────────
if not api_key:
    st.warning("⚠️ GOOGLE_API_KEY not found. Please add it to your .env file and restart the app.")
    st.stop()

# Load recipes
try:
    recipes_df = load_recipes(recipe_path)
    recipes_text = format_recipes_for_prompt(recipes_df)
except Exception as e:
    st.error(f"Could not load recipe book: {e}")
    st.stop()

# ── Step 1: Ingredient Input ──────────────────────────────────────────────────
st.markdown('<div class="section-header">Step 1 — What\'s in your kitchen? 🥦</div>', unsafe_allow_html=True)
st.caption("Every Saturday, tell us what ingredients you have and we'll plan your week.")

raw_ingredients = ingredient_input_section(api_key)

# ── Step 2: Categorize Ingredients ───────────────────────────────────────────
categorized = {}
if raw_ingredients and st.button("✅ Categorize Ingredients"):
    with st.spinner("Sorting your ingredients..."):
        categorized = categorize_ingredients(raw_ingredients, api_key)
    st.session_state["categorized"] = categorized

if "categorized" in st.session_state:
    categorized = st.session_state["categorized"]
    st.markdown('<div class="section-header">Step 2 — Your Ingredients 🗂️</div>', unsafe_allow_html=True)

    cols = st.columns(3)
    for i, (cat, items) in enumerate(categorized.items()):
        with cols[i % 3]:
            items_list = items if isinstance(items, list) else [items]
            edited = st.text_area(
                f"**{cat}**",
                value=", ".join(items_list),
                height=80,
                key=f"cat_{cat}"
            )
            categorized[cat] = [x.strip() for x in edited.split(",") if x.strip()]

    # ── Step 3: Generate Meal Plan ────────────────────────────────────────────
    st.divider()
    st.markdown('<div class="section-header">Step 3 — Generate Weekly Meal Plan 📅</div>', unsafe_allow_html=True)

    if st.button("🍽️ Generate My Weekly Meal Plan"):
        with st.spinner("MySousChef is planning your week... This may take a moment ✨"):
            try:
                meal_plan = generate_meal_plan(categorized, recipes_text, api_key)
                st.session_state["meal_plan"] = meal_plan
            except Exception as e:
                st.error(f"Error generating meal plan: {e}")

# ── Step 4: Display + Edit + Download ─────────────────────────────────────────
if "meal_plan" in st.session_state:
    meal_plan = st.session_state["meal_plan"]

    st.markdown('<div class="section-header">Your Weekly Meal Plan ✨</div>', unsafe_allow_html=True)
    st.caption("You can edit any meal below before downloading.")

    DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    MEALS = ["Breakfast", "Lunch", "Evening Snack", "Dinner"]
    MEAL_ICONS = {"Breakfast": "🌅", "Lunch": "☀️", "Evening Snack": "🫖", "Dinner": "🌙"}

    # Display as editable table
    tabs = st.tabs(DAYS)
    edited_plan = {}

    for tab, day in zip(tabs, DAYS):
        edited_plan[day] = {}
        with tab:
            for meal in MEALS:
                meal_data = meal_plan.get(day, {}).get(meal, {})
                with st.expander(f"{MEAL_ICONS[meal]} {meal}", expanded=True):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        recipe = st.text_input(
                            "Recipe",
                            value=meal_data.get("recipe", ""),
                            key=f"{day}_{meal}_recipe"
                        )
                        link = st.text_input(
                            "Link",
                            value=meal_data.get("link", ""),
                            key=f"{day}_{meal}_link"
                        )
                    with col2:
                        protein = st.selectbox("Protein", ["High", "Medium", "Low"],
                            index=["High","Medium","Low"].index(meal_data.get("protein","Medium")),
                            key=f"{day}_{meal}_protein")
                        fiber = st.selectbox("Fiber", ["High", "Medium", "Low"],
                            index=["High","Medium","Low"].index(meal_data.get("fiber","Medium")),
                            key=f"{day}_{meal}_fiber")
                        carbs = st.selectbox("Carbs", ["High", "Medium", "Low"],
                            index=["High","Medium","Low"].index(meal_data.get("carbs","Medium")),
                            key=f"{day}_{meal}_carbs")

                    edited_plan[day][meal] = {
                        "recipe": recipe, "link": link,
                        "protein": protein, "fiber": fiber, "carbs": carbs
                    }

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔄 Regenerate Plan"):
            del st.session_state["meal_plan"]
            st.rerun()

    with col2:
        excel_bytes = generate_meal_plan_excel(edited_plan)
        st.download_button(
            label="📥 Download Meal Plan (Excel)",
            data=excel_bytes,
            file_name="MySousChef_WeeklyMealPlan.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    st.success("✅ Your meal plan is ready! Download it or share the link with your family.")
