import streamlit as st

st.set_page_config(
    page_title="English Practice App",
    page_icon="📘",
)

st.title("📘 English Practice App")

st.markdown(
    """
    Welcome to your personal English learning assistant! This app is designed to help you practice grammar, vocabulary, and sentence fluency through guided exercises powered by AI.

    ### 🚀 What can you do here?

    #### 📝 1. One Word Exercise
    Practice writing full paragraphs using specific vocabulary. You'll:
    - Be given a set of target words from categories like Verbs, Nouns, Phrases, etc.
    - Answer a given question using those words.
    - Receive AI-powered feedback and a corrected version of your writing.
    - Optionally record your answer via audio.

    #### ✏️ 2. Sentence Variation
    Practice rewriting sentences in different ways. You'll:
    - Be shown an AI-generated sentence using key vocabulary.
    - Try to express the same idea with your own variation.
    - Get instant feedback on accuracy, grammar, and how well you preserved the original meaning.
    - Optionally use audio input for practice.

    ---

    ### 📍 How to get started?
    👉 Use the sidebar to select one of the exercises:
    - **"1_Word_Exercise"** for paragraph practice.
    - **"2_Variation"** for sentence rewriting.

    ---
    ### 💡 Tips
    - Speak or write — both modes are supported!
    - Make sure to use as many of the suggested words as possible.
    - Review the feedback carefully to improve your grammar and vocabulary.

    Happy learning! 🎓
    """
)

st.sidebar.success("Choose an exercise from the menu.")
