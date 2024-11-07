from urllib import response
import streamlit as st
import os
import google.generativeai as genai

# Set up Google Gemini API configuration
GEMINI_API_KEY = "AIzaSyAaiQA7FzTBndF0ygx1NQJkHOaXTgUgbFE"
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

# Improved Theme
st.markdown("""
    <style>
        .main { background-color: #f8f9fa; color: #333; }
        h1, h2, h3 { color: #28a745; font-family: 'Arial', sans-serif;}
        .stTextInput > div > div > input {font-size: 16px;} /* Larger input text */
        .stButton > button {background-color: #28a745; color: white; font-weight: bold;}
        .stCheckbox label {font-size: 16px;}
    </style>
""", unsafe_allow_html=True)

st.title("📘 Personalized Learning Aggregator")

# --- Learning Style Quiz ---
st.header("❓ Learning Style Quiz")
quiz_questions = {
    "Q1": "I learn best by:",
    "Q2": "I prefer to:",
    "Q3": "I understand concepts better when they are:",
    "Q4": "I enjoy learning activities that involve:",
}
quiz_options = {
    "Q1": ["Seeing diagrams and visuals", "Reading and writing", "Doing and experimenting", "Discussing and interacting"],
    "Q2": ["Watch videos and demonstrations", "Read books and articles", "Work on projects and exercises", "Attend workshops and group discussions"],
    "Q3": ["Presented visually", "Explained in detail", "Demonstrated practically", "Discussed collaboratively"],
    "Q4": ["Visual aids and multimedia", "Text-based materials and notes", "Interactive simulations and games", "Group projects and presentations"],

}
quiz_answers = {}

for question, options in quiz_options.items():
    quiz_answers[question] = st.radio(quiz_questions[question], options, key=question)

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
    # ... (Gemini API call and response handling as before)

    # --- Progress Tracking ---
    st.header("✅ Progress Tracker")

    if "learning_paths" not in st.session_state:
        st.session_state.learning_paths = {}


    if role_or_skill not in st.session_state.learning_paths:
        st.session_state.learning_paths[role_or_skill] = {"checklist": [], "completed": []}


    checklist_items = [item.strip() for item in response.text.split("\n") if item.strip().startswith("-")]
    st.session_state.learning_paths[role_or_skill]["checklist"] = checklist_items

    for item in st.session_state.learning_paths[role_or_skill]["checklist"]:
        is_completed = st.checkbox(item, key=f"checkbox_{item}_{role_or_skill}")  # Unique key
        if is_completed:
            if item not in st.session_state.learning_paths[role_or_skill]["completed"]:
                st.session_state.learning_paths[role_or_skill]["completed"].append(item)
        else:
            if item in st.session_state.learning_paths[role_or_skill]["completed"]:
                 st.session_state.learning_paths[role_or_skill]["completed"].remove(item)


    if st.button("Save Progress"):
        st.success("Progress saved!")


    # Display saved learning paths and progress
    st.header("💾 Saved Learning Paths")
    for path, data in st.session_state.learning_paths.items():
        st.subheader(path)
        st.write("Checklist:")
        for item in data["checklist"]:
            check_mark = "✅" if item in data["completed"] else "⬜" #check emoji
            st.write(f"{check_mark} {item}")

        progress_percentage = (len(data["completed"]) / len(data["checklist"])) * 100 if data["checklist"] else 0

        st.write(f"Progress: {progress_percentage:.0f}%")
        st.progress(progress_percentage / 100)




# Footer
st.markdown("---")
st.markdown("This learning aggregator app was created to help users find tailored resources and guidance for effective learning.")