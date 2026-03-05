import streamlit as st


def ingredient_input_section(api_key: str) -> str:
    """Ingredient input section — text only."""
    st.markdown("### 🥦 What ingredients do you have at home?")
    st.caption("List everything you have — AI will sort them into categories automatically.")

    raw_ingredients = st.text_area(
        "Type your ingredients naturally:",
        placeholder="e.g. spinach, onions, tomatoes, rice, lentils, paneer, apples, yogurt, cumin...",
        height=150
    )

    return raw_ingredients
