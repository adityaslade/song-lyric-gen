import streamlit as st
from google import genai
from google.genai import types

# --- Configuration & Setup ---

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="AI Lyric Generator + Controller",
    page_icon="🎤",
    layout="wide"
)

# --- LLM API Setup ---
# Tries to get the API key from secrets.toml (Streamlit Cloud) or environment variables (local)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except KeyError:
    API_KEY = st.sidebar.text_input(
        "Enter your Gemini API Key:", type="password", help="The API key is required to run the model."
    )
    if not API_KEY:
        st.warning("Please enter your Gemini API Key to continue.")
        st.stop()
    
# Initialize the Gemini Client
try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error(f"Error initializing Gemini client: {e}")
    st.stop()

# Define the model and base generation settings
MODEL = "gemini-2.5-flash"
BASE_CONFIG = types.GenerateContentConfig(
    temperature=0.8, # Higher temperature for more creativity
    max_output_tokens=2048
)

# --- Prompt Templates (The Core of the Project) ---

# 1. Base System Prompt: The foundational rules for the LLM
BASE_SYSTEM_PROMPT = """
You are a master songwriter and poet. Your task is to generate complete song lyrics based on a user-provided theme, a specified mood, and a strict musical style.
You MUST adhere to the following structural and formatting rules:
1. STRUCTURE: Output the song in a standard structure: [Verse 1], [Chorus], [Verse 2], [Chorus], [Bridge], [Chorus], [Outro]. Label each section clearly using Markdown headings (e.g., **[Chorus]**).
2. RHYME & METER: Ensure the lyrics have a consistent, natural-sounding rhythm and at least an AABB or ABAB rhyme scheme within each section (Verse/Chorus/Bridge).
3. COHERENCE: The entire song must revolve around the main **THEME** provided by the user. Use vivid, relevant imagery.

The user will provide the **THEME** and select the **STYLE**. Your response must ONLY be the song lyrics.
"""

# 2. Style-Specific Control Prompts (From the 3-5 Style/Control Experts)
STYLE_CONTROLS = {
    "Gothic/Poetic Ballad": {
        "mood": "Melancholy, dramatic, and ornate.",
        "instructions": (
            "**RHYME/METER:** Use complex internal rhymes and a slightly formal, iambic meter (or close to it). "
            "**VOCABULARY:** Employ archaic or highly descriptive language (e.g., 'azure,' 'veridian,' 'shadow-veil,' 'lament'). "
            "**IMAGERY:** Focus on themes of eternal loss, rain, stone, moonlight, decay, and dramatic, dark romance."
        )
    },
    "Hip-Hop/Rap Banger": {
        "mood": "Confident, rhythmic, and wordplay-heavy.",
        "instructions": (
            "**RHYME/METER:** Prioritize complex multi-syllabic rhymes, internal rhymes, and punchlines. The flow should be tight and aggressive. "
            "**VOCABULARY:** Incorporate modern slang and strong, direct metaphors. Avoid simple language. "
            "**IMAGERY:** Focus on themes of ambition, overcoming struggle, city life, and declarative self-confidence."
        )
    },
    "Upbeat Pop/Country": {
        "mood": "Optimistic, simple, and radio-friendly.",
        "instructions": (
            "**RHYME/METER:** Use simple AABB or ABAB rhyme schemes. The rhythm should be bright, major-key, and easy to sing along to. "
            "**VOCABULARY:** Use universally understood, emotional language and relatable, everyday nouns (e.g., 'truck,' 'sunshine,' 'heart,' 'road'). "
            "**IMAGERY:** Focus on themes of nostalgia, new beginnings, driving, love, and summer."
        )
    }
}

# --- Streamlit UI Components ---

st.title("🎤 AI Song Lyric Generator")
st.markdown("""
A fun, controlled GenAI demo using advanced prompting to control **Rhyme, Theme, and Style**.
""")

# Input Area
with st.container(border=True):
    col1, col2 = st.columns([1, 1])

    with col1:
        # 1. Theme Input (User Control)
        theme = st.text_input(
            "🎶 Enter a Core Theme/Topic:",
            placeholder="e.g., The feeling of realizing you left your keys inside, or, A celebration of the first day of snow."
        )
    
    with col2:
        # 2. Style Control (Style/Control Experts' Control)
        style_selection = st.selectbox(
            "🎭 Select a Musical Style/Controller:",
            options=list(STYLE_CONTROLS.keys()),
            index=0,
            key="style_select"
        )

# Generate Button
if st.button("🚀 Generate Lyrics", type="primary", use_container_width=True):
    if not theme:
        st.error("Please enter a core theme to generate the lyrics.")
    else:
        # --- Prompt Assembly (The Technical Core) ---
        selected_style = STYLE_CONTROLS[style_selection]
        
        # Combine all parts into the final, directive prompt
        full_user_prompt = f"""
        **THEME:** {theme}
        **STYLE INSTRUCTIONS:** - Mood: {selected_style['mood']}
        - Specific Instructions: {selected_style['instructions']}
        - **FINALLY:** Generate the full song lyrics now, adhering strictly to the structure, rhyme, and style rules provided.
        """

        # Display waiting message
        with st.spinner("Writing the next big hit..."):
            try:
                # --- API Call with Corrected System Instruction Passing ---
                
                # Create a dynamic config object, injecting the system instruction correctly
                # THIS FIXES THE 'unexpected keyword argument system_instruction' ERROR
                generation_config = types.GenerateContentConfig(
                    temperature=BASE_CONFIG.temperature,
                    max_output_tokens=BASE_CONFIG.max_output_tokens,
                    system_instruction=BASE_SYSTEM_PROMPT
                )
                
                # Call the LLM API, passing the user prompt and the configuration
                response = client.models.generate_content(
                    model=MODEL,
                    contents=[full_user_prompt],
                    config=generation_config
                )
                
                # --- Output ---
                st.subheader("📝 Generated Song Lyrics")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"An error occurred during generation: {e}")
                st.info("Check your API key and try again. For detailed errors, see the console.")

# --- Project Info & Next Steps ---
st.markdown("---")
st.subheader("💡 Project Details & Next Steps")
st.markdown(
    f"""
This application meets the project requirement for a fun, working GenAI demo with theme and style control.

* **Model Used:** `{MODEL}` (using the Gemini API)
* **Controller Implementation:** The three distinct styles are controlled via advanced **System Prompt** injection.
* **Next Steps:** The **Project Manager** can deploy this `app.py` and `requirements.txt` file to **Streamlit Community Cloud** for a one-click live demo link (linking the GitHub repository). The **Evaluation & Ethics Captain** can then use the generated results for the required human evaluation.
"""
)

# Instructions for GitHub Deployment
st.sidebar.title("GitHub & Deployment Guide")
st.sidebar.markdown(
    """
1.  **Create Repo:** Make a new **public** GitHub repository.
2.  **Add Files:** Add `app.py` and `requirements.txt`.
3.  **Deploy:** Go to **Streamlit Community Cloud** (share.streamlit.io), connect your GitHub, select the repository and the `app.py` file.
4.  **Secrets:** Use the **Secrets** section on Streamlit Cloud to securely add your `GEMINI_API_KEY` (matching the key name in `secrets.toml`).
"""
)
