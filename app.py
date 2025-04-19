import streamlit as st
import random
import mysql.connector

# ---------- CONFIGURATION ----------
st.set_page_config(page_title="Quiz App", page_icon="🧠", layout="centered")

# ---------- CUSTOM CSS ----------
def set_custom_css():
    st.markdown("""
    <style>
        .main {
            background-color: #f9f9f9;
        }
        h1, h2, h3 {
            color: #4CAF50;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 8px 20px;
        }
        .stRadio>div>label {
            font-size: 16px;
        }
    </style>
    """, unsafe_allow_html=True)

# ---------- DB CONNECTION ----------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="shashank",
        database="quiz_app"
    )

# ---------- FETCH RANDOM 10 QUESTIONS ----------
def fetch_random_questions():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM questions ORDER BY RAND() LIMIT 10")
    questions = cursor.fetchall()
    connection.close()
    return questions

# ---------- RUN QUIZ ----------
def run_quiz(name):
    if 'score' not in st.session_state:
        st.session_state.score = 0
        st.session_state.current_q = 0
        st.session_state.questions = fetch_random_questions()
        st.session_state.incorrect_questions = []

    st.markdown(f"### Question {st.session_state.current_q + 1}")
    q = st.session_state.questions[st.session_state.current_q]
    st.markdown(f"{q['question']}")

    options = [q['option1'], q['option2'], q['option3'], q['option4']]
    answer = st.radio("Select your answer:", options, key=st.session_state.current_q)

    if st.button("Submit Answer"):
        correct_index = q['correct_option'] - 1
        correct_answer = options[correct_index]

        if answer == correct_answer:
            st.success("✅ Correct!")
            st.session_state.score += 1
        else:
           # st.error(f"❌ Incorrect! Correct answer: {correct_answer}")
            st.session_state.incorrect_questions.append({
                "question": q['question'],
                "your_answer": answer,
                "correct_answer": correct_answer
            })

        st.session_state.current_q += 1

        if st.session_state.current_q == 10:
            st.balloons()
            st.success(f"🎉 Well done, {name}! You scored {st.session_state.score}/10.")

            if st.session_state.incorrect_questions:
                st.markdown("---")
                st.markdown("### ❌ Review of Incorrect Questions")
                for idx, item in enumerate(st.session_state.incorrect_questions, 1):
                    st.markdown(f"**{idx}. {item['question']}**")
                    st.markdown(f"- Your Answer: `{item['your_answer']}`")
                    st.markdown(f"- Correct Answer: `{item['correct_answer']}`")

            st.session_state.clear()
        else:
            st.rerun()

# ---------- MAIN ----------
def main():
    set_custom_css()

    st.title("🧠 Quiz Master")
    st.markdown("Welcome to the *Online Quiz System*. Enter your details to begin!")

    with st.sidebar:
        st.header("📘 Quiz Info")
        st.markdown("""
        - 10 Random Questions  
        - 1 Point per Correct Answer  
        - Instant Feedback  
        - Final Score at the End 🎯
        """)

    if 'username' not in st.session_state:
        name = st.text_input("Enter your name:")
        email = st.text_input("Enter your email:")
        phone = st.text_input("Enter your phone number:")

        if st.button("Start Quiz"):
            if name and email and phone:
                st.session_state.username = name
                st.session_state.email = email
                st.session_state.phone = phone
                st.rerun()
            else:
                st.warning("Please fill in all fields to start the quiz.")
    else:
        progress = st.session_state.current_q / 10 if 'current_q' in st.session_state else 0
        st.progress(progress)
        run_quiz(st.session_state.username)

if __name__ == "__main__":
    main()
