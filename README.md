# 🎤 AI Song Lyric Generator + Rhyme & Theme Controller

This project is a fun, working GenAI demo built in a 2-week sprint to demonstrate advanced prompt engineering and control over Large Language Models (LLMs) for creative text generation.

## 🚀 Live Demo

[PLACE YOUR LIVE STREAMLIT CLOUD URL HERE]

## ✨ Features

* **Rhyme & Meter Control:** The LLM is strictly instructed to use consistent rhyme schemes (AABB/ABAB) and natural meter.
* **Theme Coherence:** Users provide a theme, and the model ensures the entire song is focused on that topic.
* **Three Style Experts:** Dedicated style prompts enable the generation of lyrics in three highly distinct genres:
    1.  **Gothic/Poetic Ballad**
    2.  **Hip-Hop/Rap Banger**
    3.  **Upbeat Pop/Country**

## 🛠️ Technology Stack

* **Frontend/Demo:** [Streamlit](https://streamlit.io/)
* **Generative Model:** Google's Gemini API (`gemini-2.5-flash`)
* **Language:** Python

## 💡 How to Run Locally

1.  **Clone the Repository:**
    ```bash
    git clone [YOUR REPO URL]
    cd ai-lyric-generator-project
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set API Key:**
    * Create a folder named `.streamlit` in the root directory.
    * Create a file named `secrets.toml` inside the `.streamlit` folder.
    * Add your Gemini API key:
        ```toml
        GEMINI_API_KEY="YOUR_API_KEY_HERE"
        ```

4.  **Run the App:**
    ```bash
    streamlit run app.py
    ```

---

You now have all the necessary files to create your zip archive and start your project! Would you like me to help you draft the contents of the required **"Failures & Ethics"** section for your final report next?