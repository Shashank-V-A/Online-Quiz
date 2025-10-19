import streamlit as st

st.set_page_config(page_title="Quiz App", page_icon="🧠", layout="centered")

st.title("🧠 Quiz Master")
st.write("Welcome to the Online Quiz System!")

name = st.text_input("Enter your name:")
if st.button("Start Quiz"):
    st.success(f"Hello {name}! Quiz functionality coming soon!")