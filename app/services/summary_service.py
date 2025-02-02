import os
from app import logger
import ollama
import tempfile
import re
from dotenv import load_dotenv
from openai import OpenAI


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
    logger.info(f"Full text received: {response_text[:1000]}")
    return response_text

def generate_prompt(context, transcript):
    """Genera el prompt para la IA basado en el contexto y el transcript."""
    return (
        "Write a **technical blog post in English** for Medium based on the provided video context and transcript. "
        "The transcript and context are provided in **English, Spanish, or Portuguese**. **First, translate them into English**, "
        "then write the article based on that. "
        "The article should be **clear, concise, and engaging** for developers and tech companies, ensuring technical accuracy "
        "while explaining complex concepts in an accessible way. The post must be between **1000 and 1500 words**. "
        "Use a structured, logical flow with practical examples where relevant. Include a **call to action** to encourage reader engagement. "
        "Keep it **professional yet approachable**.\n\n"
        "Structure:\n"
        "- **Introduction**: Briefly introduce the topic and why it matters.\n"
        "- **Problem Statement**: Describe the issue faced.\n"
        "- **Solution**: Explain how it was resolved with key details.\n"
        "- **Challenges & Learnings**: Highlight obstacles and takeaways.\n"
        "- **Relevance to the Reader**: Connect the topic to real-world applications.\n"
        "- **Conclusion & Next Steps**: Summarize key points and suggest further reading.\n\n"
        f"**Video Context**:\n{context}\n\n"
        f"*Transcript:\n{transcript}\n\n"
        "Do not include the transcript in the final blog post. Use the transcript for reference only to generate the article."
    )


def generate_with_openai(prompt):
    logger.info(f"[BLOG_POST]: Using OpenAI model: {OLLAMA_MODEL}")

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

        prompt = generate_prompt(context, transcript)

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


