import os
from app import logger
import ollama
import tempfile
import re
from dotenv import load_dotenv
from openai import OpenAI
import yaml


load_dotenv()
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

transcript_dir = '/app/transcripts'


def extract_response_text(stream):
    response_text = ""
    for chunk in stream:
        if 'message' in chunk and hasattr(chunk['message'], 'content'):
            response_text += chunk['message'].content
        else:
            logger.info(f"The chunk does not have the expected format: {chunk}")
    return response_text


def load_prompt_template(file_path="prompt.yaml"):
    with open(file_path, "r") as file:
        config = yaml.safe_load(file)
    return config.get("prompt_template")


def generate_prompt(context, transcript, prompt_template):
    return prompt_template.format(context=context, transcript=transcript)


def generate_with_openai(prompt):
    logger.info(f"[BLOG_POST]: Using OpenAI model: {OPENAI_MODEL}")

    client = OpenAI(api_key=OPENAI_API_KEY)
    chat_completion = client.chat.completions.create(
        messages=[{'role': 'user', 'content': prompt}],
        model=OPENAI_MODEL,
    )
    return chat_completion.choices[0].message.content


def generate_with_ollama(prompt):
    logger.info(f"[BLOG_POST]: Using Ollama model: {OLLAMA_MODEL}")
    stream = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[{'role': 'user', 'content': prompt}],
        stream=True,
    )
    return extract_response_text(stream)


def clean_response(response_text):
    return re.sub(r'<think>.*?</think>', '', response_text, flags=re.DOTALL)


def generate_blog_post(transcript, title=None, description=None, use_openai=False):

    logger.info(f"[BLOG_POST]: Starting process to generate blog post")
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

        prompt_template = load_prompt_template()
        prompt = generate_prompt(context, transcript, prompt_template)
        logger.info(f"[BLOG_POST]: Prompt generated (preview): {prompt[:100]}")

        if use_openai:
            response_text = generate_with_openai(prompt)
        else:
            response_text = generate_with_ollama(prompt)

        logger.info(f"[BLOG_POST]: Ending process to generate blog post")

        return clean_response(response_text)


    except Exception as e:
        logger.error(f"Error generating blog post: {e}")
        return "Error: Failed to generate a blog post. Please try again later."

    finally:
        if temp_path:
            os.remove(temp_path)


