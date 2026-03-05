import streamlit as st


def ingredient_input_section(api_key: str) -> tuple[str, bool]:
    """Ingredient input section — text with always-visible submit button."""
    st.markdown("### 🥦 What ingredients do you have at home?")
    st.caption("List everything you have — AI will sort them into categories automatically.")

    raw_ingredients = st.text_area(
        "Type your ingredients naturally:",
        placeholder="e.g. spinach, onions, tomatoes, rice, lentils, paneer, apples, yogurt, cumin...",
        height=150,
        key="ingredients_input",
        label_visibility="collapsed"
    )

    submitted = st.button(
        "✅ Categorize My Ingredients",
        use_container_width=True,
        type="primary",
        disabled=not raw_ingredients
    )

    return raw_ingredients, submitted
