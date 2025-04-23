# main.py

import re
import os
import json
import logging
from dotenv import load_dotenv

# ----------------------------------------
# Load environment variables
# ----------------------------------------
load_dotenv()

PROVIDER = os.getenv("PROVIDER", "google").lower()
API_KEY = os.getenv("API_KEY")
# Choose defaults per provider
DEFAULT_MODEL_GOOGLE = "gemini-2.0-flash"
DEFAULT_MODEL_OPENAI = "gpt-3.5-turbo"
MODEL = os.getenv("MODEL") or (
    DEFAULT_MODEL_GOOGLE if PROVIDER == "google" else DEFAULT_MODEL_OPENAI
)

if not API_KEY:
    raise ValueError("Missing API_KEY environment variable.")

# ----------------------------------------
# Provider clients setup
# ----------------------------------------
if PROVIDER == "google":
    # Google Gen AI SDK client for the Gemini Developer API
    from google import genai

    google_client = genai.Client(
        vertexai=False,  # developer endpoint (not Vertex AI)
        api_key=API_KEY
    )
elif PROVIDER == "openai":
    # OpenAI Python library client
    from openai import OpenAI

    openai_client = OpenAI(api_key=API_KEY)
else:
    raise ValueError(f"Unsupported provider: {PROVIDER}")


# ----------------------------------------
# Unified generation function
# ----------------------------------------
def generate_response(prompt: str) -> str:
    """
    Send the prompt to the configured provider and return the generated text.
    """
    if PROVIDER == "google":
        try:
            resp = google_client.models.generate_content(
                model=MODEL,
                contents=prompt
            )
            return resp.text.strip()
        except Exception as e:
            logging.error(f"Google Gen AI error: {e}")
            raise

    else:  # openai
        try:
            resp = openai_client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}]
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            logging.error(f"OpenAI error: {e}")
            raise


# ----------------------------
# Few-shot Prompting
# ----------------------------
def few_shot_prompt(query: str, examples: list[dict]) -> str:
    """
    Demonstrates few-shot prompting using provided examples.
    """
    prompt = ""
    for ex in examples:
        prompt += f"Q: {ex['question']}\nA: {ex['answer']}\n"
    prompt += f"Q: {query}\nA:"
    return generate_response(prompt)


# ----------------------------
# Structured Output (JSON Mode)
# ----------------------------
def structured_json_response(query: str) -> dict:
    prompt = (
        "Answer the following question in JSON format "
        "'{\"answer\": \"Your answer here\"}'. "
        f"Question: {query}"
    )
    result = generate_response(prompt)
    # Strip any ```json or ``` fences that the model may emit
    clean = result.strip()
    # Remove leading ``` or ```json
    clean = re.sub(r"^```(?:json)?\s*", "", clean)
    # Remove trailing ```
    clean = re.sub(r"\s*```$", "", clean)
    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        logging.error(f"JSON parse error: {clean!r}")
        return {"error": "Failed to parse JSON", "raw_response": result}


# ----------------------------
# Retrieval‑Augmented Generation (RAG)
# ----------------------------
def retrieval_augmented_generation(context: str, question: str) -> str:
    """
    Uses provided context to augment generation for accuracy.
    """
    prompt = f"Context: {context}\nQuestion: {question}\nAnswer:"
    return generate_response(prompt)


# ----------------------------
# Function Calling
# ----------------------------
class Calculator:
    """Simple calculator functions."""

    @staticmethod
    def add(a: float, b: float) -> float:
        return a + b

    @staticmethod
    def multiply(a: float, b: float) -> float:
        return a * b


def function_call(function_name: str, *args: float) -> float:
    """
    Dynamic function calling based on the function_name.
    """
    functions = {"add": Calculator.add, "multiply": Calculator.multiply}
    if function_name not in functions:
        raise ValueError(f"Function '{function_name}' not supported.")
    return functions[function_name](*args)


# ----------------------------
# Main Demonstration
# ----------------------------
def main():
    examples = [
        {"question": "What is the capital of France?", "answer": "Paris"},
        {"question": "Who wrote Hamlet?", "answer": "William Shakespeare"}
    ]

    print("Few‑shot Prompting:\n",
          few_shot_prompt("What is the tallest mountain on Earth?", examples))

    print("\nStructured JSON Response:\n",
          structured_json_response("Who discovered penicillin?"))

    context = "Albert Einstein developed the theory of relativity, E=mc^2."
    print("\nRetrieval‑Augmented Generation:\n",
          retrieval_augmented_generation(context, "What is Einstein famous for?"))

    print("\nFunction Calling (multiply 5 x 3):\n",
          function_call("multiply", 5, 3))


if __name__ == "__main__":
    main()
