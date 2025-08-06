import json
from pydantic import BaseModel, Field
from typing import List
import streamlit as st
from langchain_groq import ChatGroq
if __name__ == "__main__":
    import prompts 
else:
    import prompts as prompts

class WordsUsage(BaseModel):
    used: List[str] = Field(description="List of words that were used in the paragraph.")
    not_used: List[str] = Field(description="List of words that were not used in the paragraph.")


# Load secrets from Streamlit's secrets management
GROQ_API = st.secrets["LLM"]["API"]
GROQ_MODEL = st.secrets["LLM"]["MODEL"]


LLM = ChatGroq(model=GROQ_MODEL,api_key=GROQ_API)

def evaluate_paragraph(question, words_list, user_paragraph):
    prompt = prompts.EVALUATE_PARAGRAPH.format(question = question,
                                               words = words_list,
                                               user_paragraph = user_paragraph)
    llm_response = LLM.invoke(prompt)
    grammar_response = json.loads(llm_response.content)

    prompt = prompts.WORDS_USAGE.format(words = words_list,
                                        user_paragraph = user_paragraph)
    llm_response = LLM.invoke(prompt)
    words_usage_response = json.loads(llm_response.content)

    return grammar_response, words_usage_response


def generate_sentence(words, verb_tense,  length = "short"):
    prompt = prompts.GENERATE_SENTENCE_FROM_WORDS.format(words = words, verb_tense = verb_tense, length = length)
    llm_response = LLM.invoke(prompt)
    sentence_response = json.loads(llm_response.content)
    return sentence_response

def evaluate_sentence_variation(original_sentence, user_variation):
    prompt = prompts.EVALUATE_SENTENCE_VARIATION.format(original_sentence = original_sentence, user_variation = user_variation)
    llm_response = LLM.invoke(prompt)
    evaluation_response = json.loads(llm_response.content)
    return evaluation_response



if __name__ == "__main__":
    #response = evaluate_paragraph("What’s your current priority?", 
    #                              ['Verbs: handle', 'Connectors: in order to test', 'Nouns: schema', 'Phrases: It turned out that …', 'Misc: a lot of'], 
    #                              "In order to test the schema i wrote some unit test. It turned out that i need to handle a lot of errors. This is my priority now.")
    words = ['Verbs: handle', 'Connectors: in order to test', 'Nouns: schema', 'Phrases: It turned out that …', 'Misc: a lot of']
    sentence_response = generate_sentence(words, verb_tense="Simple past",  length = "long")
    print(sentence_response)

