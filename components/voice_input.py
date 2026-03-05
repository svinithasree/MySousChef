import streamlit as st
import tempfile
import os

def record_ingredients():
    """Voice input component using streamlit audio recorder."""
    st.markdown("### 🎙️ Tell us what ingredients you have at home")
    st.caption("Click the mic, speak your ingredients naturally, then click stop.")

    try:
        from streamlit_audiorecorder import audiorecorder
        audio = audiorecorder("🎙️ Click to Record", "⏹️ Stop Recording")

        if len(audio) > 0:
            st.audio(audio.export().read(), format="audio/wav")
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                audio.export(f.name, format="wav")
                return f.name
    except ImportError:
        st.warning("audiorecorder not installed. Using text input instead.")

    return None


def transcribe_audio(audio_path: str, api_key: str) -> str:
    """Transcribe audio using Google Gemini."""
    import google.generativeai as genai

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

    with open(audio_path, "rb") as f:
        audio_data = f.read()

    import base64
    audio_b64 = base64.b64encode(audio_data).decode()

    response = model.generate_content([
        {
            "inline_data": {
                "mime_type": "audio/wav",
                "data": audio_b64
            }
        },
        "Please transcribe exactly what ingredients are mentioned in this audio. Return only the list of ingredients as plain text, comma separated."
    ])

    os.unlink(audio_path)
    return response.text.strip()


def ingredient_input_section(api_key: str) -> str:
    """Full ingredient input section with voice + text fallback."""
    input_method = st.radio(
        "How would you like to enter ingredients?",
        ["🎙️ Voice Input", "⌨️ Type them in"],
        horizontal=True
    )

    raw_ingredients = ""

    if input_method == "🎙️ Voice Input":
        audio_path = record_ingredients()
        if audio_path:
            with st.spinner("Transcribing your ingredients..."):
                raw_ingredients = transcribe_audio(audio_path, api_key)
            st.success("✅ Transcribed!")
            raw_ingredients = st.text_area(
                "Edit if needed:", value=raw_ingredients, height=100
            )
    else:
        raw_ingredients = st.text_area(
            "Type your ingredients (comma separated or just list them naturally):",
            placeholder="e.g. spinach, onions, tomatoes, rice, lentils, paneer, apples...",
            height=120
        )

    return raw_ingredients
