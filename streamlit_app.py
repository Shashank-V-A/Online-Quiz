import streamlit as st
import random

# ---------- CONFIGURATION ----------
st.set_page_config(page_title="Quiz Master", page_icon="🧠", layout="centered")

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

# ---------- SAMPLE QUESTIONS ----------
def get_sample_questions():
    return [
        {
            'question': 'What is the capital of India?',
            'option1': 'Mumbai',
            'option2': 'Delhi',
            'option3': 'Bangalore',
            'option4': 'Chennai',
            'correct_option': 2
        },
        {
            'question': 'Which programming language is known for web development?',
            'option1': 'Python',
            'option2': 'JavaScript',
            'option3': 'C++',
            'option4': 'Java',
            'correct_option': 2
        },
        {
            'question': 'What does HTML stand for?',
            'option1': 'HyperText Markup Language',
            'option2': 'High Tech Modern Language',
            'option3': 'Home Tool Markup Language',
            'option4': 'Hyperlink and Text Markup Language',
            'correct_option': 1
        },
        {
            'question': 'Which company developed Python?',
            'option1': 'Microsoft',
            'option2': 'Google',
            'option3': 'Guido van Rossum',
            'option4': 'Apple',
            'correct_option': 3
        },
        {
            'question': 'What is the largest planet in our solar system?',
            'option1': 'Earth',
            'option2': 'Saturn',
            'option3': 'Jupiter',
            'option4': 'Neptune',
            'correct_option': 3
        },
        {
            'question': 'Which year was Python first released?',
            'option1': '1989',
            'option2': '1991',
            'option3': '1995',
            'option4': '2000',
            'correct_option': 2
        },
        {
            'question': 'What does CSS stand for?',
            'option1': 'Computer Style Sheets',
            'option2': 'Creative Style Sheets',
            'option3': 'Cascading Style Sheets',
            'option4': 'Colorful Style Sheets',
            'correct_option': 3
        },
        {
            'question': 'Which tag is used to create a hyperlink in HTML?',
            'option1': '<link>',
            'option2': '<a>',
            'option3': '<href>',
            'option4': '<url>',
            'correct_option': 2
        },
        {
            'question': 'What is the main purpose of JavaScript?',
            'option1': 'Database management',
            'option2': 'Adding interactivity to web pages',
            'option3': 'Server-side programming',
            'option4': 'Image editing',
            'correct_option': 2
        },
        {
            'question': 'Which of the following is not a programming language?',
            'option1': 'Python',
            'option2': 'HTML',
            'option3': 'JavaScript',
            'option4': 'Java',
            'correct_option': 2
        },
        {
            'question': 'What does API stand for?',
            'option1': 'Application Programming Interface',
            'option2': 'Automated Programming Interface',
            'option3': 'Advanced Programming Interface',
            'option4': 'Application Process Interface',
            'correct_option': 1
        },
        {
            'question': 'Which database is commonly used with Python web frameworks?',
            'option1': 'MongoDB',
            'option2': 'PostgreSQL',
            'option3': 'MySQL',
            'option4': 'All of the above',
            'correct_option': 4
        }
    ]

# ---------- FETCH RANDOM 10 QUESTIONS ----------
def fetch_random_questions():
    all_questions = get_sample_questions()
    return random.sample(all_questions, min(10, len(all_questions)))

# ---------- RUN QUIZ ----------
def run_quiz(name):
    if 'questions' not in st.session_state:
        st.session_state.score = 0
        st.session_state.current_q = 0
        st.session_state.questions = fetch_random_questions()
        st.session_state.incorrect_questions = []

    st.markdown(f"### Question {st.session_state.current_q + 1}")
    q = st.session_state.questions[st.session_state.current_q]
    st.markdown(f"**{q['question']}**")

    options = [q['option1'], q['option2'], q['option3'], q['option4']]
    answer = st.radio("Select your answer:", options, key=st.session_state.current_q)

    if st.button("Submit Answer"):
        correct_index = q['correct_option'] - 1
        correct_answer = options[correct_index]

        if answer == correct_answer:
            st.success("✅ Correct!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Incorrect! The correct answer was: {correct_answer}")
            st.session_state.incorrect_questions.append({
                "question": q['question'],
                "your_answer": answer,
                "correct_answer": correct_answer
            })

        st.session_state.current_q += 1

        if st.session_state.current_q >= 10:
            st.balloons()
            percentage = (st.session_state.score / 10) * 100
            
            if percentage >= 80:
                st.success(f"🎉 Excellent, {name}! You scored {st.session_state.score}/10 ({percentage}%)!")
            elif percentage >= 60:
                st.success(f"👍 Good job, {name}! You scored {st.session_state.score}/10 ({percentage}%)!")
            else:
                st.info(f"📚 Keep studying, {name}! You scored {st.session_state.score}/10 ({percentage}%)!")

            if st.session_state.incorrect_questions:
                st.markdown("---")
                st.markdown("### ❌ Review of Incorrect Questions")
                for idx, item in enumerate(st.session_state.incorrect_questions, 1):
                    st.markdown(f"**{idx}. {item['question']}**")
                    st.markdown(f"- Your Answer: `{item['your_answer']}`")
                    st.markdown(f"- Correct Answer: `{item['correct_answer']}`")

            st.markdown("---")
            if st.button("🔄 Take Another Quiz"):
                st.session_state.clear()
                st.rerun()
        else:
            st.rerun()

# ---------- MAIN ----------
def main():
    set_custom_css()
    
    # Initialize all session state variables
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'current_q' not in st.session_state:
        st.session_state.current_q = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = []
    if 'quiz_completed' not in st.session_state:
        st.session_state.quiz_completed = False
    if 'incorrect_questions' not in st.session_state:
        st.session_state.incorrect_questions = []

    st.title("🧠 Quiz Master")
    st.markdown("Welcome to the *Online Quiz System*. Enter your details to begin!")

    with st.sidebar:
        st.header("📘 Quiz Info")
        st.markdown("""
        - 10 Random Questions  
        - 1 Point per Correct Answer  
        - Instant Feedback  
        - Final Score at the End 🎯
        - Review Incorrect Answers
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
        progress = st.session_state.current_q / 10
        st.progress(progress)
        st.markdown(f"**Current Score: {st.session_state.score}/10**")
        run_quiz(st.session_state.username)

if __name__ == "__main__":
    main()