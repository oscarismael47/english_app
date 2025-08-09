from __future__ import annotations

import json
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
import streamlit as st
import prompts

from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

# ---------- Pydantic Schemas ----------
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


# ---------- Handler ----------
class LLMHandler:
    """
    Unified handler for LLM operations using LangChain with structured outputs.
    Supports OpenAI and Groq backends.
    """

    def __init__(
        self,
        provider: Literal["openai", "groq"] = "openai",
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        temperature: float = 0.2,
        timeout: Optional[int] = 120,
    ):
        """
        Parameters:
            provider: "openai" or "groq".
            model: Model name. If None, taken from Streamlit secrets.
            api_key: API key. If None, taken from Streamlit secrets.
            temperature: Sampling temperature.
            timeout: Request timeout in seconds.
        """
        self.provider = provider

        # Secrets fallback
        if provider == "openai":
            model = model or st.secrets.get("OPENAI_MODEL")
            api_key = api_key or st.secrets.get("OPENAI_KEY")
            if not (model and api_key):
                raise ValueError("Missing OPENAI_MODEL or OPENAI_KEY in secrets or init params.")
            self.llm = ChatOpenAI(model=model, api_key=api_key, temperature=temperature, timeout=timeout)

        elif provider == "groq":
            model = model or st.secrets.get("GROQ_MODEL", "llama-3.1-70b-versatile")
            api_key = api_key or st.secrets.get("GROQ_KEY")
            if not api_key:
                raise ValueError("Missing GROQ_KEY in secrets or init params.")
            self.llm = ChatGroq(model=model, groq_api_key=api_key, temperature=temperature, timeout=timeout)

        else:
            raise ValueError("provider must be 'openai' or 'groq'")

        self.model_name = model

    # ---- Core invoke helper (structured output) ----
    def _invoke_structured(self, schema: BaseModel, prompt: str) -> dict:
        """
        Invokes the underlying LLM with structured output defined by `schema`.
        Returns dict via .model_dump().
        """
        try:
            resp = self.llm.with_structured_output(schema).invoke(prompt)
            return resp.model_dump()
        except Exception as e:
            raise RuntimeError(f"LLM invocation failed ({self.provider}:{self.model_name}): {e}")

    # ---------- Ops ----------
    def evaluate_paragraph(self, question: str, verb_tense: str, words, user_paragraph: str) -> dict:
        """
        Evaluates and improves a user's paragraph based on grammar, vocabulary usage, and relevance.
        """
        prompt = prompts.EVALUATE_PARAGRAPH.format(
            question=question,
            verb_tense=verb_tense,
            words=words,
            user_paragraph=user_paragraph,
        )
        return self._invoke_structured(ParagraphEvaluation, prompt)

    def generate_sentence(self, words, verb_tense: str, length: str = "short") -> dict:
        """
        Generates a grammatical, natural sentence/paragraph using the given words.
        """
        prompt = prompts.GENERATE_SENTENCE_FROM_WORDS.format(
            words=words,
            verb_tense=verb_tense,
            length=length,
        )
        return self._invoke_structured(GenerateSentence, prompt)

    def evaluate_sentence_variation(self, original_sentence: str, user_variation: str) -> dict:
        """
        Evaluates whether the user's variation preserves meaning and is correct; returns feedback/corrections.
        """
        prompt = prompts.EVALUATE_SENTENCE_VARIATION.format(
            original_sentence=original_sentence,
            user_variation=user_variation,
        )
        return self._invoke_structured(SentenceVariationEvaluation, prompt)
