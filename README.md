# 🍽️ MySousChef — AI Weekly Meal Planner

A Streamlit app powered by Google Gemini that plans your family's vegetarian meals every week based on what's in your kitchen.

## Features
- 🎙️ Voice input for ingredients (or type them)
- 🤖 Gemini AI categorizes ingredients automatically
- 📖 Matches your ingredients to your personal recipe book
- 📅 Generates a full 7-day meal plan (Breakfast, Lunch, Snack, Dinner)
- ✏️ Editable meal plan in the app
- 📥 Download as a formatted Excel file

## Project Structure
```
MySousChef/
├── app.py                    # Main Streamlit app
├── requirements.txt
├── .env.example              # Copy to .env and add your API key
├── data/
│   └── recipes.xlsx          # Your recipe book
├── components/
│   ├── voice_input.py        # Mic recording + transcription
│   ├── meal_planner.py       # LangChain + Gemini logic
│   └── excel_handler.py      # Read/write Excel files
└── prompts/
    └── meal_plan_prompt.py   # Prompt templates
```

## Local Setup (VS Code)

1. **Clone the repo and navigate to folder:**
   ```bash
   cd MySousChef
   ```

2. **Activate your virtual environment:**
   ```bash
   # Windows
   mysouschef-mvp-env\Scripts\activate
   # Mac/Linux
   source mysouschef-mvp-env/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key:**
   - Copy `.env.example` to `.env`
   - Add your Google AI Studio API key

5. **Run the app:**
   ```bash
   streamlit run app.py
   ```

## Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Add `GOOGLE_API_KEY` in the Secrets section
5. Deploy! You'll get a shareable public URL.

## Recipe Book Format

Your `recipes.xlsx` must have these columns:
| Recipe Name | Link/URL | Ingredients | Category | Vegetarian |
|---|---|---|---|---|
| Palak Paneer | https://... | spinach, paneer... | Dinner | Yes |

Categories: `Breakfast`, `Lunch`, `Evening Snack`, `Dinner`

## Family Setup
Planned for: 2 Adults + 1 Teenager
