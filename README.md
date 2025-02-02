# YouTube Summary and Blog Generator

This project leverages Generative AI (GenAI) to perform two main functionalities:

1. **Video Summary**: Generates a concise summary of a YouTube video based on its transcript, description, and title.
2. **Style Blog Post**: Creates a detailed blog post using the same input data.

The application is fully containerized with Docker for easy setup and deployment.

---

## Prerequisites

Before starting, ensure you have the following installed:
- **Docker** and **Docker Compose**.
- A **Google Cloud service account** with access to the **YouTube Data API**.

Make sure the following files are available in your project directory:
- `.env`: Contains your **API key**.
- `client_secrets.json`: Configured for your **Google Cloud service account**.
- **Downloaded model**: Ensure you have the required model, such as `deepseek-r1` or `llama3.1` , available in the correct directory. To download the model, use the following command:

```bash
docker exec -it ollama ollama pull deepseek-r1
docker exec -it ollama ollama pull llama3.1
```


## Setting Up the Models

To ensure the correct models are available in your Docker container, follow these steps:

1. **Start the Docker container** with Ollama running:

    ```bash
    docker-compose up
    ```

2. **Download the required models** inside the Docker container. You can pull multiple, such as `deepseek-r1` and `llama3.1`, using the following command:

    ```bash
    docker exec -it ollama ollama pull deepseek-r1
    docker exec -it ollama ollama pull llama3.1
    ```

    This will download the specified models into the Ollama container.

## Verifying Available Models

Once your Docker container is running, you can verify the models that are installed in the Ollama container with the following command:

```bash
docker exec -it ollama ollama list
```
This will list all the models available in your Ollama container, and you should see something similar to:
```
NAME                  ID       SIZE      MODIFIED
deepseek-r1:latest    0a8cX    4.7 GB    4 minutes ago
llama3.1:latest       46e0X    4.9 GB    2 hours ago
```
---

## Setup

### 1. Create the `.env` File
In the root of the project, create a `.env` file with the following variables:

YOUTUBE_API_KEY=<Your_YouTube_Data_API_Key>
Replace `<Your_YouTube_Data_API_Key>` with your actual API key from the Google Cloud Console.

MODEL_TO_USE=<model_name>
Replace `<model_name>` with the LLM that you want to test

---

### 2. `client_secrets.json` File
Ensure you have the `client_secrets.json` file in the root directory. If you don’t have it:
1. Log in to your [Google Cloud Console](https://console.cloud.google.com/).
2. Navigate to **APIs & Services > Credentials**.
3. Create a **Service Account** and download the credentials file.
4. Save it as `client_secrets.json` in the root of your project.

Example `client_secrets.json` format:
```json
{
    "web": {
        "client_id": "",
        "project_id": "YOUR_PROJECT_ID",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "YOUR_CLIENT_SECRET"
    }
}
```

### 3. Install dependencies: If you’re using Python-based dependencies, run:
```bash
poetry install
```
### 4. Build and Run the Dockerized App

Run the following commands to build and start the application:

```bash
# Build the Docker image
docker-compose build

# Start the application
docker-compose up
```
The application will be accessible at http://localhost:5000.

## Endpoints

### 1. Video Summary
**Endpoint**: `/video_summary/<video_id_youtube>`
**Method**: `GET`
**Description**: Generates a concise summary of a YouTube video using its title, description, and transcript.

**Example**:
```bash
curl http://localhost:5000/video_summary/VIDEO_ID_YOUTUBE
```

### 2. Blog Post Generator
**Endpoint**: `/video_blog/<video_id_youtube>`
**Method**: `GET`
**Description**: Creates a blog post based on the video’s title, description, and transcript.

**Example**:
```bash
curl http://localhost:5000/video_blog/VIDEO_ID_YOUTUBE
```
