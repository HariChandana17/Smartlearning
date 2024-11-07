import streamlit as st
import os
import google.generativeai as genai

GEMINI_API_KEY = "AIzaSyAaiQA7FzTBndF0ygx1NQJkHOaXTgUgbFE"
# Set up Google Gemini API configuration
genai.configure(api_key=GEMINI_API_KEY)

# Create the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Streamlit app layout and theme
st.set_page_config(page_title="Learning Aggregator", page_icon="📘", layout="wide")

# Theme setup for Streamlit
st.markdown("""
    <style>
        .main { background-color: #f5f5f5; color: #333; }
        h1, h2, h3 { color: #1f77b4; }
    </style>
    """, unsafe_allow_html=True)

st.title("📘 Personalized Learning Aggregator")

# Step 1: Ask user their preferred learning style
st.header("🧑‍🎓 Step 1: Choose Your Learning Preferences")
learning_type = st.selectbox(
    "What type of learning do you prefer?",
    ["Visual (Videos, Diagrams)", "Textual (Articles, Books)", "Interactive (Exercises, Quizzes)", "Hands-On (Projects)"]
)

effective_learning = st.radio(
    "Which type of learning has been effective for you in the past?",
    ["Visual", "Textual", "Interactive", "Hands-On"]
)

# Step 2: Ask about goal: Start from scratch or Upskill
st.header("🎯 Step 2: Select Your Learning Goal")
goal = st.radio("Do you want to prepare for a role from scratch, or upskill?", ["Start from Scratch", "Upskill"])

# Step 3: Get the role or skill they're aiming for
st.header("🔍 Step 3: Define Your Target")
if goal == "Start from Scratch":
    role_or_skill = st.text_input("Enter the role you want to start from scratch (e.g., Data Scientist, Web Developer)")
else:
    role_or_skill = st.text_input("Enter the skill you want to upskill in (e.g., Machine Learning, Cloud Computing)")

# If details are filled, proceed to suggest resources
if role_or_skill:
    # Generate a learning path with Gen AI based on user preferences
    st.header("📚 Your Personalized Learning Path")
    st.write("Generating a tailored learning path for you...")

    # Create chat session and send message using the configured Gemini model
    chat_session = model.start_chat(
        history=[]
    )
    prompt = f"""
    Given that the user prefers {learning_type} learning and finds {effective_learning} effective,
    create a detailed learning plan tailored for {goal.lower()} in {role_or_skill}.
    Include high-quality free resources and, if starting from scratch, focus on beginner-friendly materials.
    Otherwise, include advanced documentation and resources for upskilling.
    """

    response = chat_session.send_message(prompt)
    
    # Display the tailored learning plan
    st.write(response.text)

# Footer
st.markdown("---")
st.markdown("This learning aggregator app was created to help users find tailored resources and guidance for effective learning.")
