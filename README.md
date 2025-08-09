# 📘 English Practice App

An interactive English learning tool built with **Streamlit** that helps users improve their vocabulary, grammar, and sentence fluency using **AI**. The app offers both **speaking** and **writing** modes, providing real-time feedback and corrections through a **Large Language Model (LLM)**.

---

## 🔧 Features

### 📝 1. One Word Exercise
Practice using specific vocabulary by answering guided questions. Categories include:
- **Verbs**
- **Connectors**
- **Nouns**
- **Phrases**
- **Miscellaneous**

🔍 **AI Evaluation Includes:**
- Grammar and sentence structure
- Correct usage of target words (used vs. not used)
- Input can be **text** or **audio**

---

### ✏️ 2. Sentence Variation
Paraphrase AI-generated sentences while using specific vocabulary.

🧠 **AI Feedback Includes:**
- Whether the meaning is preserved
- Grammar, tone, and fluency analysis
- Suggested correction and explanation
- Works with both **typed** and **spoken** input

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/english-practice-app.git
cd english-practice-app
2. Install Dependencies
Make sure you have Python 3.9+ installed.

bash
Copy
Edit
pip install -r requirements.txt
3. Set Up API Credentials
Create a file at .streamlit/secrets.toml and add the following:

toml
Copy
Edit
[LLM]
API_KEY = "your_GROQ_KEY_key"
MODEL = "your_groq_model_name"  # e.g., "mixtral-8x7b-32768"
4. Run the App
bash
Copy
Edit
streamlit run Home.py
Then open your browser at: http://localhost:8501

📂 Project Structure
Copy
Edit
english-practice-app/
│
├── utils/
│   ├── data_helper.py
│   ├── llm_helper.py
│   ├── audio_to_text_helper.py
│   └── prompts.py
│
├── 1_Word_Exercise.py
├── 2_Variation.py
├── Home.py
├── requirements.txt
└── README.md
💡 Technologies Used
Streamlit – interactive web interface

LangChain – prompt management and LLM integration

Groq LLMs – real-time evaluation and correction

Pydantic – data validation

OpenAI Chat Format – compatible message format

🎙️ Audio Support
Supports audio input via microphone

Audio is transcribed using transcribe_audio_with_groq()

Temporary file saved as recorded_audio.wav

📌 Notes
Exercises rely on the Excel file: english_business.xlsx – ensure it’s available in the root directory

Prompts are optimized for clarity, consistency, and high-quality LLM responses

🧠 Example Use Cases
ESL (English as a Second Language) learners

Business English practice

Improving speaking fluency

Writing refinement through guided paraphrasing

📬 Feedback & Contributions
Contributions are welcome!
Feel free to:

⭐ Star the repository

🐞 Report issues

📥 Submit pull requests

