import os
from app import logger
import ollama
import tempfile
import re
from dotenv import load_dotenv
from openai import OpenAI
import yaml
import requests


load_dotenv()
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OLLAMA_BASE_URL = "http://host.docker.internal:11434"

transcript_dir = '/app/transcripts'


def extract_response_text(stream):
    response_text = ""
    for chunk in stream:
        if 'message' in chunk and hasattr(chunk['message'], 'content'):
            response_text += chunk['message'].content
        else:
            logger.info(f"The chunk does not have the expected format: {chunk}")
    return response_text


def load_prompt_template(file_path="prompt.yaml", prompt=""):
    with open(file_path, "r") as file:
        config = yaml.safe_load(file)
    return config.get(prompt)


def generate_prompt(context, transcript, prompt_template):
    return prompt_template.format(context=context, transcript=transcript)


def generate_with_openai(prompt):
    logger.info(f"[POST]: Using OpenAI model: {OPENAI_MODEL}")

    client = OpenAI(api_key=OPENAI_API_KEY)
    chat_completion = client.chat.completions.create(
        messages=[{'role': 'user', 'content': prompt}],
        model=OPENAI_MODEL,
    )
    return chat_completion.choices[0].message.content


def generate_with_ollama(prompt):
    logger.info(f"[POST]: Using Ollama model: {OLLAMA_MODEL}")
    stream = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[{'role': 'user', 'content': prompt}],
        stream=True,
    )
    return extract_response_text(stream)


def generate_with_ollama_localhost(prompt):
    logger.info(f"[POST]: Using Ollama model (localhost): {OLLAMA_MODEL}")

    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": "Eres un asistente experto en resumir transcripts de videos. Devuelve un resumen conciso con los puntos clave más importantes."},
            {"role": "user", "content": prompt},
        ],
        "stream": False  # Cambia a True si quieres respuesta en streaming
    }


    response = requests.post(f"{OLLAMA_BASE_URL}/api/chat", json=payload)

    if response.status_code != 200:
        logger.error("Error in Ollama response: %s", response.text)
        return None
    try:
        data = response.json()
        return data.get("message", {}).get("content", "")
    except ValueError:
        logger.error("Failed to parse the response as JSON")
        return None


def clean_response(response_text):
    return re.sub(r'<think>.*?</think>', '', response_text, flags=re.DOTALL)


def generate_post(transcript, title=None, description=None, use_openai=False, prompt_name_template=""):

    logger.info(f"[{prompt_name_template}]: Starting process")
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as temp:
            temp.write(transcript)
            temp_path = temp.name

        context = ""
        if title:
            context += f"Video title: {title}\n"
        if description:
            context += f"Video description: {description}\n"

        prompt_template = load_prompt_template(prompt=prompt_name_template)
        prompt = generate_prompt(context, transcript, prompt_template)
        logger.info(f"[{prompt_name_template}]: Prompt generated (preview): {prompt[:100]}")

        if use_openai:
            response_text = generate_with_openai(prompt)
        else:
            response_text = generate_with_ollama_localhost(prompt)

        logger.info(f"[{prompt_name_template}]: Ending process to generate post")

        return clean_response(response_text)


    except Exception as e:
        logger.error(f"Error generating post: {e}")
        return "Error: Failed to generate post. Please try again later."

    finally:
        if temp_path:
            os.remove(temp_path)


