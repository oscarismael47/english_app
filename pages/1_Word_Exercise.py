from utils.data_helper import DataHelper
from utils.llm_helper import evaluate_paragraph
from utils.audio_to_text_helper import transcribe_audio_with_groq
import streamlit as st

FILE_PATH = "english_business.xlsx"
words_per_section = {"Verbs":1, "Connectors":1, "Nouns":1, "Questions":1, "Phrases":1, "Times":1, "Misc":1}

@st.dialog("No more available exercises. Try another section")
def no_more_exercises():
    pass

if "data_helper" not in st.session_state:
    st.session_state.data_helper = DataHelper(FILE_PATH)

if "selected_words" not in st.session_state:
    st.session_state.selected_words = {}

if "question" not in st.session_state:
    st.session_state.question = "None"

if "time" not in st.session_state:
    st.session_state.time = "None"

if "user_paragraph" not in st.session_state:
    st.session_state.user_paragraph = ""

if "words_list" not in st.session_state:
    st.session_state.words_list = []

if "feedback" not in st.session_state:
    st.session_state.feedback = ""

if "corrected_paragraph" not in st.session_state:
    st.session_state.corrected_paragraph = ""

if "used_words_list" not in st.session_state:
    st.session_state.used_words_list = []

if "not_used_words_list" not in st.session_state:
    st.session_state.not_used_words_list = []




with st.sidebar:
    next_column, analyze_column = st.columns(2)

    with next_column:
        if st.button("Next", use_container_width=True):
            st.session_state.selected_words = st.session_state.data_helper .get_words(words_per_section)
            print(st.session_state.selected_words)
            if st.session_state.selected_words == {}:
                print("no_more_exercises")
                print(st.session_state.selected_words)
                no_more_exercises()
            else:
                st.session_state.question = st.session_state.selected_words["Questions"][0]
                st.session_state.time = st.session_state.selected_words["Times"][0]
                st.session_state.words_list = []
                for section, words in st.session_state.selected_words.items():
                    if section == "Questions": 
                        continue
                    if section == "Times":
                        continue
                    for word in words:
                        st.session_state.words_list.append(f"{section}: {word}")
                st.session_state.user_paragraph = ""
                st.session_state.feedback = ""
                st.session_state.corrected_paragraph = ""
                st.session_state.used_words_list = []
                st.session_state.not_used_words_list = []

    with analyze_column:
        if st.button("Analyze", use_container_width=True):
            print(st.session_state.question)
            print(st.session_state.words_list)
            print(st.session_state.user_paragraph)
            grammar_response, words_usage_response = evaluate_paragraph(st.session_state.question, st.session_state.words_list, st.session_state.user_paragraph)
            st.session_state.feedback = grammar_response["feedback"]
            st.session_state.corrected_paragraph = grammar_response["correct_paragraph"]
            st.session_state.used_words_list = words_usage_response["used"]
            st.session_state.not_used_words_list = words_usage_response["not_used"]



st.markdown(f"Answer Question: **{st.session_state.question}**")
st.markdown(f"Use this verb tense: **{st.session_state.time}**")

selection = st.pills("Use the followings words", st.session_state.words_list, selection_mode="multi")

user_paragraph_audio = st.audio_input("Record paragraph audio to analyze")
print(user_paragraph_audio)
if user_paragraph_audio:
    with open("recorded_audio.wav", "wb") as f:
        f.write(user_paragraph_audio.getbuffer())
    #st.audio(user_paragraph_audio)
    st.session_state.user_paragraph = transcribe_audio_with_groq("recorded_audio.wav")

st.session_state.user_paragraph = st.text_area("Or Write paragraph to analyze",
                                               value = st.session_state.user_paragraph,
                                               placeholder="")


with st.container(border=True):
    st.markdown("**Corrected Paragraph**")
    st.markdown(st.session_state.corrected_paragraph)

with st.container(border=True):
    st.markdown("**Feedback**")
    st.markdown(st.session_state.feedback)



st.pills("Used words", st.session_state.used_words_list, key="used_words", selection_mode="multi")
st.pills("Not Used words", st.session_state.not_used_words_list , key="not_used_words", selection_mode="multi")
