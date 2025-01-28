import os
import requests
from app import logger


llama_host = os.getenv("LLAMA_HOST", "http://localhost:8000")  # Default a localhost
endpoint = f"{llama_host}/api/chat"  # Endpoint de tu API Llama local


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
            f"Tarea: Escribe un resumen en español sobre el siguiente video. El resumen debe tener un máximo de 500 palabras, "
            "ser conciso y claro. Estructúralo de la siguiente manera: \n"
            "1. **Introducción**: Breve presentación del tema y su importancia, mencionar brevemente a las personas involucradas del video.\n"
            "2. **Puntos clave**: Expande los puntos más relevantes del transcript.\n"
            "3. **Conclusión**: Resumen de lo aprendido en el video y relevancia del tema.\n\n"
            f"**Contexto del video**:\n{context}\n\n"
            f"**Transcript**:\n{cleaned_transcript}\n\n"
        )
    logger.info(f"prompt para resumen: {prompt[:1000]}")

    return None


def generate_blog_post(transcript, title=None, description=None):

    cleaned_transcript = transcript.replace("\n", " ")
    cleaned_transcript = " ".join(cleaned_transcript.splitlines())
    context = ""
    if title:
        context += f"Título del video: {title}\n"
    if description:
        context += f"Descripción del video: {description}\n"

    prompt = (
        f"Tarea: Escribe un artículo técnico en inglés para el blog de Medium de Mercado Libre basado en el contexto del video y el transcript proporcionados. "
        "El artículo debe tener entre 1500 y 1800 palabras, manteniendo un tono claro, preciso y cercano, ideal para desarrolladores y empresas de tecnología. "
        "Asegúrate de que el contenido sea comprensible para una audiencia externa a Mercado Libre, proporcionando el contexto necesario sobre nuestras soluciones. "
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
        f"**Contexto del video**:\n{context}\n\n"
        f"**Transcript**:\n{cleaned_transcript}\n\n"
    )

    logger.info(f"prompt para blog: {prompt[:1000]}")
    return None