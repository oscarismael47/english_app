from data_helper import DataHelper
from llm_helper import evaluate_paragraph
from audio_to_text_helper import transcribe_audio_with_groq
import streamlit as st

FILE_PATH = "english_business.xlsx"
words_per_section = {"Verbs":1, "Connectors":1, "Nouns":1, "Questions":1, "Phrases":1, "Times":1, "Misc":1}

st.set_page_config(layout="wide")

@st.dialog("No more available exercises. Try another section")
def no_more_exercises():
    pass

if "data_helper" not in st.session_state:
    st.session_state.data_helper = DataHelper(FILE_PATH)

if "selected_words" not in st.session_state:
    st.session_state.selected_words = {}

if "question" not in st.session_state:
    st.session_state.question = ""

if "verb_tense" not in st.session_state:
    st.session_state.verb_tense = ""

if "user_paragraph" not in st.session_state:
    st.session_state.user_paragraph = ""

if "words" not in st.session_state:
    st.session_state.words = [] 

if "feedback" not in st.session_state:
    st.session_state.feedback = ""

if "used_words" not in st.session_state:
    st.session_state.used_words = []

if "not_used_words" not in st.session_state:
    st.session_state.not_used_words = []

if "corrected_paragraph" not in st.session_state:
    st.session_state.corrected_paragraph = ""

if "corrected_paragraph_analysis" not in st.session_state:
    st.session_state.corrected_paragraph_analysis = ""


with st.sidebar:
    next_column, analyze_column = st.columns(2)

    with next_column:
        if st.button("Next", use_container_width=True):
            st.session_state.selected_words = st.session_state.data_helper.get_words(words_per_section)

            if st.session_state.selected_words == {}:
                print("no_more_exercises")
                no_more_exercises()
            else:
                st.session_state.question = st.session_state.selected_words["Questions"][0]
                st.session_state.verb_tense = st.session_state.selected_words["Times"][0]
                st.session_state.words = []
                for section, words in st.session_state.selected_words.items():
                    if section == "Questions": 
                        continue
                    if section == "Times":
                        continue
                    for word in words:
                        st.session_state.words.append(f"{section}: {word}")
                st.session_state.user_paragraph = ""
                st.session_state.feedback = ""
                st.session_state.corrected_paragraph = ""
                st.session_state.corrected_paragraph_analysis = ""
                st.session_state.used_words = []
                st.session_state.not_used_words = []

    with analyze_column:
        if st.button("Analyze", use_container_width=True):
            print(st.session_state.question)
            print(st.session_state.words)
            print(st.session_state.user_paragraph)
            response = evaluate_paragraph(  st.session_state.question,
                                            st.session_state.verb_tense,
                                            st.session_state.words,
                                            st.session_state.user_paragraph)

            st.session_state.feedback = response["feedback"]
            st.session_state.used_words = response["used_words"]
            st.session_state.not_used_words = response["not_used_words"]
            st.session_state.corrected_paragraph = response["corrected_paragraph"]
            st.session_state.corrected_paragraph_analysis = response["corrected_paragraph_analysis"]

            print(st.session_state.feedback )
            print(st.session_state.used_words )
            print(st.session_state.not_used_words )
            print(st.session_state.corrected_paragraph )
            print(st.session_state.corrected_paragraph_analysis ) 

st.markdown(f"Answer Question: **{st.session_state.question}**")
st.markdown(f"Use this verb tense: **{st.session_state.verb_tense}**")

selection = st.pills("Use the followings words", st.session_state.words, selection_mode="multi")



with st.container(border=True):
    col_1, col_2 = st.columns(2)

    with col_1:
        user_paragraph_audio = st.audio_input("Record paragraph audio to analyze")
        if user_paragraph_audio:
            with open("recorded_audio.wav", "wb") as f:
                f.write(user_paragraph_audio.getbuffer())
            st.session_state.user_paragraph = transcribe_audio_with_groq("recorded_audio.wav")
        st.session_state.user_paragraph = st.text_area("Or Write paragraph to analyze",
                                               value = st.session_state.user_paragraph,
                                               placeholder="")

    with col_2:
        st.markdown("**Feedback**")
        st.markdown(st.session_state.feedback)

with st.container(border=True):
    col_1, col_2 = st.columns(2)

    with col_1:
        st.markdown("**Corrected Paragraph**")
        st.markdown(st.session_state.corrected_paragraph)
    
    with col_2:
        st.markdown("**Corrected Paragraph Analysis**")
        st.markdown(st.session_state.corrected_paragraph_analysis)

st.pills("Used words", st.session_state.used_words, key="used_words", selection_mode="multi")
st.pills("Not Used words", st.session_state.not_used_words , key="not_used_words", selection_mode="multi")
