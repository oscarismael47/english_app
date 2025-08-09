import json
from utils.llm_helper import LLMHandler

# Choose your backend: "openai" or "groq"
handler = LLMHandler(provider="openai")  # or LLMHandler(provider="groq")

question = "What’s your current priority?"
verb_tense = "Simple past"
words = ['Verbs: handle', 'Connectors: in order to test', 'Nouns: schema', 'Phrases: It turned out that …', 'Misc: a lot of']
user_paragraph = "In order to test the schema i wrote some unit test. It turned out that i need to handle a lot of errors. This is my priority now."
length = "short"

# 1) Evaluate paragraph
result = handler.evaluate_paragraph(question, verb_tense, words, user_paragraph)
print(json.dumps(result, indent=2, ensure_ascii=False))

# 2) Generate sentence
gen = handler.generate_sentence(words=words, verb_tense=verb_tense, length=length)
print(json.dumps(gen, indent=2, ensure_ascii=False))

# 3) Evaluate sentence variation
original_sentence = gen["generated_sentence"]
user_variation = input("\nYour variation: ")
eval_var = handler.evaluate_sentence_variation(original_sentence, user_variation)
print(json.dumps(eval_var, indent=2, ensure_ascii=False))
