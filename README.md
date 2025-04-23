# 🧠 GenAI-Playground

A lightweight, modular playground for experimenting with Generative AI features like prompt engineering, few-shot learning, structured JSON output, retrieval-augmented generation (RAG), and simple function calling — powered by **Google Gemini 2** or **OpenAI GPT**.

---

## 🚀 Features

- 🔧 **Prompt Engineering** – Easily craft custom prompts and test model responses  
- 🧪 **Few-shot Learning** – Add examples to guide better answers  
- 📦 **Structured JSON Output** – Get clean, parsable AI responses  
- 📚 **Retrieval-Augmented Generation** – Inject external context into AI prompts  
- 🧮 **Function Calling** – Call Python functions directly from natural language  
- 🔁 **Flexible Provider Support** – Works with OpenAI and Google GenAI

---

## 📁 Project Structure

GenAI-Playground/ ├── main.py / notebook.ipynb ├── .env # API keys and config ├── requirements.txt # Python dependencies └── README.md


---

## ⚙️ Getting Started

1. **Install dependencies:**

```bash
pip install -r requirements.txt

Set environment variables (.env or in notebook):

PROVIDER=google         # or 'openai'
API_KEY=your_api_key
MODEL=gemini-2.0-flash  # or gpt-3.5-turbo

Run the notebook or Python script and start generating!

examples = [
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "Who wrote Hamlet?", "answer": "William Shakespeare"}
]

few_shot_prompt("What is the tallest mountain on Earth?", examples)

