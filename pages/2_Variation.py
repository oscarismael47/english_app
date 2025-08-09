from utils.data_helper import DataHelper
from utils.llm_helper import LLMHandler
from utils.groq_helper import GroqHandler
import streamlit as st

FILE_PATH = "english_business.xlsx"
words_per_section = {"Verbs":1, "Connectors":1, "Nouns":1, "Questions":1, "Phrases":1, "Times":1, "Misc":1}


@st.dialog("No more available exercises. Try another section")
def no_more_exercises():
    pass

if "data_helper" not in st.session_state:
    st.session_state.data_helper = DataHelper(FILE_PATH)

if "llm_handler" not in st.session_state:
    st.session_state.llm_handler = LLMHandler(provider="openai") 

if "groq_handler" not in st.session_state:
    st.session_state.groq_handler = GroqHandler() 

if "selected_words" not in st.session_state:
    st.session_state.selected_words = {}

if "verb_tense" not in st.session_state:
    st.session_state.verb_tense = ""

if "genearated_sentence" not in st.session_state:
    st.session_state.generated_sentence = ""

if "user_variation" not in st.session_state:
    st.session_state.user_variation = ""

if "feedback" not in st.session_state:
    st.session_state.feedback = ""

if "corrected_variation" not in st.session_state:
    st.session_state.corrected_variation = ""

if "is_valid" not in st.session_state:
    st.session_state.is_valid = None


with st.sidebar:
    next_column, analyze_column = st.columns(2)

    with next_column:
        if st.button("Generate Sentence", use_container_width=True):
            st.session_state.selected_words = st.session_state.data_helper.get_words(words_per_section)
            if st.session_state.selected_words == {}:
                print("no_more_exercises")
                print(st.session_state.selected_words)
                no_more_exercises()
            else:
                st.session_state.verb_tense = st.session_state.selected_words["Times"][0]
                st.session_state.words = []
                for section, words in st.session_state.selected_words.items():
                    if section == "Questions": 
                        continue
                    if section == "Times":
                        continue
                    for word in words:
                        st.session_state.words.append(f"{section}: {word}")
                
                sentence_response = st.session_state.llm_handler.generate_sentence(  words = st.session_state.words,
                                                        verb_tense= st.session_state.verb_tense,
                                                        length = "short")

                st.session_state.generated_sentence = sentence_response["generated_sentence"]
                st.session_state.user_variation = ""
                st.session_state.is_valid = None
                st.session_state.corrected_variation = ""
                st.session_state.feedback = ""

    with analyze_column:
        if st.button("Analyze", use_container_width=True):
            evaluation_response = st.session_state.llm_handler.evaluate_sentence_variation(st.session_state.generated_sentence,
                                                               st.session_state.user_variation)
            st.session_state.is_valid = evaluation_response["is_valid"]
            st.session_state.corrected_variation = evaluation_response["corrected_sentence"]
            st.session_state.feedback = evaluation_response["feedback"]
   


st.markdown(f"Original Sentence: {st.session_state.generated_sentence}")

user_paragraph_audio = st.audio_input("Record paragraph audio to analyze")
print(user_paragraph_audio)
if user_paragraph_audio:
    with open("recorded_audio.wav", "wb") as f:
        f.write(user_paragraph_audio.getbuffer())
    #st.audio(user_paragraph_audio)
    st.session_state.user_variation = st.session_state.groq_handler.speech_to_text("recorded_audio.wav")
st.session_state.user_variation = st.text_area("Or Write sentence to analyze",
                                               value = st.session_state.user_variation,
                                               placeholder="")


if st.session_state.is_valid is True:
    st.success("The variation is CORRECT!", icon="✅")
elif st.session_state.is_valid is False:
    st.error("The variation is INCORRECT!", icon="🚨")
else:
    st.info("Write a variation", icon="ℹ️")


with st.container(border=True):
    st.markdown("**Corrected Variation**")
    st.markdown(st.session_state.corrected_variation)

with st.container(border=True):
    st.markdown("**Feedback**")
    st.markdown(st.session_state.feedback)

