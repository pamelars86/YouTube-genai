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
            f"Tarea: Escribe un resumen en inglés sobre el siguiente video. El resumen debe tener un máximo de 500 palabras, "
            "ser conciso y claro. Estructúralo de la siguiente manera: \n"
            "1. **Introducción**: Breve presentación del tema y su importancia, mencionar brevemente a las personas involucradas del video.\n"
            "2. **Puntos clave**: Expande los puntos más relevantes del transcript.\n"
            "3. **Conclusión**: Resumen de lo aprendido en el video y relevancia del tema.\n\n"
            f"**Contexto del video**:\n{context}\n\n"
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
        context += f"Título del video: {title}\n"
    if description:
        context += f"Descripción del video: {description}\n"

    prompt = (
        f"Tarea: Escribe un artículo técnico en inglés para mi blog técnico en Medium basado en el contexto del video y el transcript proporcionados. "
        "El artículo debe tener entre 1500 y 1800 palabras, manteniendo un tono claro, preciso y cercano, ideal para desarrolladores y empresas de tecnología. "
        "Asegúrate de que el contenido sea comprensible para una audiencia externa, proporcionando el contexto necesario"
        "Verifica la exactitud técnica, explica conceptos complejos de manera coherente y añade ejemplos prácticos para inspirar a los lectores. "
        "Haz ajustes que mejoren la fluidez y conexión del texto con la audiencia, manteniendo un enfoque profesional e informativo. "
        "Incluye un call to action que ofrezca valor al lector, invitándolo a reflexionar, participar o aplicar los conocimientos adquiridos. "
        "Sugiere referencias o enlaces adicionales si encuentras afirmaciones sin respaldo o datos que necesitan contexto. "
        "Sigue la siguiente estructura: \n\n"
        "- **Introducción**: Presenta el tema del artículo, destacando qué encontrará el lector. Utiliza preguntas para interpelar al lector.\n"
        "- **Definición del problema**: Explica en detalle el problema que enfrentaron.\n"
        "- **¿Cómo solucionaron ese problema?**: Describe con precisión cómo lograron resolver el problema, incluyendo detalles clave.\n"
        "- **Desafíos y lecciones aprendidas**: Expón los retos encontrados durante el proceso y los aprendizajes obtenidos.\n"
        "- **¿Cómo esto puede ayudar al lector?**: Relaciona el caso con situaciones que los lectores podrían enfrentar.\n"
        "- **Conclusión y próximos pasos**: Resume lo discutido y lleva al lector a reflexionar sobre el impacto del tema.\n"
        "- **Artículos relacionados o próximos artículos**: Menciona artículos publicados o temas que serán tratados en el futuro.\n\n"
        "- **IDIOMA DEL BLOG TÉCNICO: INGLÉS.\n\n"

        f"**Contexto del video**:\n{context}\n\n"
        f"**Transcript**:\n{cleaned_transcript}\n\n"
    )

    logger.info(f"prompt para blog: {prompt[:1000]}")
    stream = ollama.chat(
        model="deepseek-r1",
        messages=[{'role': 'user', 'content': prompt}],
        stream=True,
    )
    response_text = extract_response_text(stream)

    return response_text