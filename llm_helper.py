import json
from pydantic import BaseModel, Field
from typing import List
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
if __name__ == "__main__":
    import prompts 
else:
    import prompts as prompts

class ParagraphEvaluation(BaseModel):
    feedback: str = Field(description="Constructive feedback summarizing the strengths and weaknesses of the original paragraph, with suggestions for improvement.")
    used_words: List[str] = Field(description="Words or phrases from the provided list that were used in the user's paragraph.")
    not_used_words: List[str] = Field(description="Words or phrases from the provided list that were not used in the user's paragraph.")
    corrected_paragraph: str = Field(description="The improved version of the paragraph with grammar, vocabulary, and structure corrections.")
    corrected_paragraph_analysis: str = Field(description="Explanation of the changes made in the corrected paragraph and why they were necessary.")

class GenerateSentence(BaseModel):
    generated_sentence: str = Field(description="A fluent, grammatically correct sentence or paragraph using the given words naturally and appropriately.")

class SentenceVariationEvaluation(BaseModel):
    is_valid: bool = Field(description="True if the user's variation preserves the original meaning; otherwise, False.")
    corrected_sentence: str = Field(description="A grammatically correct and natural-sounding version of the user's variation, if correction is needed.")
    feedback: str = Field(description="Constructive feedback explaining whether the variation is valid, how it differs from the original, and how it could be improved.")

OPENAI_API = st.secrets["OPENAI_API"]
OPENAI_MODEL = st.secrets["OPENAI_MODEL"]

LLM = ChatOpenAI(model=OPENAI_MODEL,api_key=OPENAI_API)

def evaluate_paragraph(question, verb_tense, words, user_paragraph):
    """
    Evaluates and improves a user's paragraph based on grammar, vocabulary usage, and relevance to a question.

    Args:
        question (str): The question that the paragraph should answer.
        verb_tense (str): The target verb tense that should be used in the paragraph.
        words (list[str] | str): List or string of words/phrases that should be included in the paragraph.
        user_paragraph (str): The user's original paragraph to be evaluated.

    Returns:
        dict: A dictionary with the corrected paragraph and feedback on grammar, clarity, and vocabulary usage.
    """
    prompt = prompts.EVALUATE_PARAGRAPH.format(question = question,
                                               verb_tense = verb_tense,
                                               words = words,
                                               user_paragraph = user_paragraph)
    llm_response = LLM.with_structured_output(ParagraphEvaluation).invoke(prompt)
    return llm_response.model_dump()

def generate_sentence(words, verb_tense, length="short"):
    """
    Generates a grammatically correct and natural-sounding sentence or paragraph using the given words.

    Args:
        words (list[str] | str): List or string of words/phrases to be used in the output.
        verb_tense (str): The target verb tense for the generated text.
        length (str, optional): Desired length of the output. Defaults to "short".

    Returns:
        dict: A dictionary containing the generated sentence or paragraph.
    """
    prompt = prompts.GENERATE_SENTENCE_FROM_WORDS.format(words = words, 
                                                         verb_tense = verb_tense, 
                                                         length = length)
    llm_response = LLM.with_structured_output(GenerateSentence).invoke(prompt)
    return llm_response.model_dump()

def evaluate_sentence_variation(original_sentence, user_variation):
    """
    Evaluates a user's sentence variation to ensure it preserves meaning, varies structure, and maintains correctness.

    Args:
        original_sentence (str): The original sentence for comparison.
        user_variation (str): The user's rewritten sentence.

    Returns:
        dict: A dictionary containing validation, corrected version (if needed), and feedback on the variation.
    """
    prompt = prompts.EVALUATE_SENTENCE_VARIATION.format(original_sentence = original_sentence,
                                                         user_variation = user_variation)
    llm_response = LLM.with_structured_output(SentenceVariationEvaluation).invoke(prompt)
    return llm_response.model_dump()



if __name__ == "__main__":
    question = "What’s your current priority?"
    verb_tense = "Simple past"
    words=['Verbs: handle', 'Connectors: in order to test', 'Nouns: schema', 'Phrases: It turned out that …', 'Misc: a lot of']
    user_paragraph="In order to test the schema i wrote some unit test. It turned out that i need to handle a lot of errors. This is my priority now."
    length = "short"
    #response = evaluate_paragraph(question=question, 
    #                              verb_tense=verb_tense,
    #                              words=words, 
    #                              user_paragraph=user_paragraph
    #                              )
    #print(response)

    response = generate_sentence(words=words,
                                 verb_tense=verb_tense,
                                 length=length)
    print(response)

    original_sentence = response["generated_sentence"]
    user_variation = input()
    response = evaluate_sentence_variation(original_sentence=original_sentence,
                                 user_variation=user_variation)