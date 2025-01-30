import os
from app import logger
import ollama

# Configuración de la URL base del servidor Ollama
ollama_host = "http://ollama:11434"  # Cambia si usas otro puerto o configuración

def extract_response_text(stream):
    response_text = ""
    for chunk in stream:
        if 'message' in chunk and hasattr(chunk['message'], 'content'):
            response_text += chunk['message'].content
        else:
            logger.info(f"The chunk does not have the expected format: {chunk}")
    logger.info(f"Full text received: {response_text[:1000]}")
    return response_text


def summarize_transcript(transcript, title=None, description=None):
    #tomado de https://docs.anthropic.com/en/prompt-library/meeting-scribe

    if not transcript:
        return "Error: Transcript is unavailable. Cannot generate a summary."

    cleaned_transcript = transcript.replace("\n", " ")
    cleaned_transcript = " ".join(cleaned_transcript.splitlines())

    context = ""
    if title:
        context += f"Título del video: {title}\n"
    if description:
        context += f"Descripción del video: {description}\n"

    prompt = (
            "Summarize the following video in **English**, even if the transcript is in another language. "
            "Translate key points if needed and ensure clarity and coherence. "
            "Keep the summary **concise, structured, and under 500 words**:\n\n"
            "1. **Introduction**: Briefly introduce the topic and its importance.\n"
            "2. **Key Points**: Highlight the main insights.\n"
            "3. **Conclusion**: Summarize key takeaways.\n\n"
            f"**Video Context**:\n{context}\n\n"
            f"**Transcript**:\n{cleaned_transcript}\n\n"
        )
    logger.info(f"prompt para resumen: {prompt[:1000]}")

    stream = ollama.chat(
        model="deepseek-r1",
        messages=[{'role': 'user', 'content': prompt}],
        stream=True,
    )
    response_text = extract_response_text(stream)

    return response_text



def generate_blog_post(transcript, title=None, description=None):

    cleaned_transcript = transcript.replace("\n", " ")
    cleaned_transcript = " ".join(cleaned_transcript.splitlines())
    context = ""
    if title:
        context += f"Video title: {title}\n"
    if description:
        context += f"Video description: {description}\n"

    prompt = (
        "Write a **technical blog post in English** for Medium based on the provided video context and transcript. "
        "If the transcript is in another language, **extract key points and translate them into English** before writing the article. "
        "The article should be **clear, concise, and engaging** for developers and tech companies, ensuring technical accuracy "
        "while explaining complex concepts in an accessible way. Use a structured, logical flow with practical examples where relevant. "
        "Include a **call to action** to encourage reader engagement. Keep it **professional yet approachable**.\n\n"
        "Structure:\n"
        "- **Introduction**: Briefly introduce the topic and why it matters.\n"
        "- **Problem Statement**: Describe the issue faced.\n"
        "- **Solution**: Explain how it was resolved with key details.\n"
        "- **Challenges & Learnings**: Highlight obstacles and takeaways.\n"
        "- **Relevance to the Reader**: Connect the topic to real-world applications.\n"
        "- **Conclusion & Next Steps**: Summarize key points and suggest further reading.\n\n"
        f"**Video Context**:\n{context}\n\n"
        f"**Transcript** (can be in another language):\n{cleaned_transcript}\n\n"
    )

    logger.info(f"Prompt for blog: {prompt[:1000]}")
    stream = ollama.chat(
        model="deepseek-r1",
        messages=[{'role': 'user', 'content': prompt}],
        stream=True,
    )
    response_text = extract_response_text(stream)

    return response_text