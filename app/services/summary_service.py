import os
from app import logger
import ollama
import tempfile
import re
from dotenv import load_dotenv


transcript_dir = '/app/transcripts'
load_dotenv()
MODEL_TO_USE = os.getenv("MODEL_TO_USE")

def extract_response_text(stream):
    response_text = ""
    for chunk in stream:
        if 'message' in chunk and hasattr(chunk['message'], 'content'):
            response_text += chunk['message'].content
        else:
            logger.info(f"The chunk does not have the expected format: {chunk}")
    logger.info(f"Full text received: {response_text[:1000]}")
    return response_text


def generate_blog_post(transcript, title=None, description=None):

    try:
        # Create a temporary file to save the transcript
        with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as temp:
            temp.write(transcript)
            temp_path = temp.name

        context = ""
        if title:
            context += f"Video title: {title}\n"
        if description:
            context += f"Video description: {description}\n"

        prompt = (
            "Write a **technical blog post in English** for Medium based on the provided video context and transcript. "
            "The transcript and context is provided in **English, Spanish, or Portuguese**. **First, translate them into English**, "
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
        )

        logger.info(f"Prompt for blog: {prompt[:1000]}")
        stream = ollama.chat(
            model=MODEL_TO_USE,
            messages=[{'role': 'user', 'content': prompt}],
            stream=True,
        )
        response_text = extract_response_text(stream)
        response_text = re.sub(r'<think>.*?</think>', '', response_text, flags=re.DOTALL)

    except Exception as e:
        logger.error(f"Error generating blog post: {e}")
        return "Error: Failed to generate a blog post. Please try again later."
    finally:
        # Delete the temporary file
        os.remove(temp_path)

    return response_text