import streamlit as st
import random

st.title("Guess the Number Game")

st.write("I'm thinking of a number between 1 and 100.")
number = random.randint(1, 100)

if 'guess' not in st.session_state:
    st.session_state.guess = None

guess = st.number_input("Enter your guess:", min_value=1, max_value=100, step=1)

if st.button("Submit"):
    st.session_state.guess = guess
    if guess < number:
        st.write("Too low! Try again.")
    elif guess > number:
        st.write("Too high! Try again.")
    else:
        st.write("Congratulations! You guessed the number.")

if st.session_state.guess == number:
    if st.button("Play Again"):
        st.session_state.guess = None
        number = random.randint(1, 100)