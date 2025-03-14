# YouTube Summary and Blog Generator

This project leverages Generative AI (GenAI) to perform:

1. **Style Blog Post**: Creates a detailed blog post in English using a video from YouTube that could be in Spanish, Portuguese, or English (title, description, and transcript).

2. **Style Slack Post**: Creates a Slack post in English using a video from YouTube that could be in Spanish, Portuguese, or English (title, description, and transcript).

This serves as a base to expedite content generation, and it is suggested to add a more personal/human tone to the results.

The application is fully containerized with Docker for easy setup and deployment.

---

## Prerequisites

Before starting, ensure you have the following installed:
- **Docker** and **Docker Compose**.
- A **Google Cloud service account** with access to the **YouTube Data API**.

Make sure the following files are available in your project directory:
- `.env`: Contains your **API key**.
- `client_secrets.json`: Configured for your **Google Cloud service account**.


## Setting Up the Models (only if you are running Ollama inside the Docker container)
Firstly, you will need to use `docker-compose-ollamadockerized.yml` instead of the content of docker-compose.yml of this repo.

To ensure the correct models are available in your Docker container, follow these steps:

1. **Start the Docker container** with Ollama running:

    ```bash
    docker-compose up
    ```

2. **Download the required models**.

 Then, you can pull multiple, such as `deepseek-r1` and `llama3.1`, using the following command:

    ```bash
    docker exec -it ollama ollama pull deepseek-r1
    docker exec -it ollama ollama pull llama3.1
    ```

    This will download the specified models into the Ollama container.

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
In the root directory of the project, create a `.env` file with the following variables:

```plaintext
YOUTUBE_API_KEY=<Your_YouTube_Data_API_Key>
```
Replace `<Your_YouTube_Data_API_Key>` with your actual API key from the Google Cloud Console.

```plaintext
OLLAMA_MODEL=<model_for_ollama>
```
Replace `<model_for_ollama>` with the LLM that you want to use with Ollama.

(Optional: If you want to use OpenAI)
```plaintext
OPENAI_MODEL=<model_for_openai>
```
Replace `<model_for_openai>` with the LLM that you want to use with OpenAI.

```plaintext
OPENAI_API_KEY=<Your_OpenAI_API_Key>
```
Replace `<Your_OpenAI_API_Key>` with your actual API key from OpenAI.

Alternatively, you can use the `.env-template` file and rename it to `.env`.

---

### 2. `client_secrets.json` File for YouTube Connection

Ensure you have the `client_secrets.json` file in the root directory. If you don’t have it, follow these steps to create one:

1. Log in to your [Google Cloud Console](https://console.cloud.google.com/).
2. Navigate to **APIs & Services > Credentials**.
3. Create a **Service Account** and download the credentials file.
4. Save the file as `client_secrets.json` in the root of your project.

An example `client_secrets.json` file format is shown below:

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
### (Optional) Update `prompt.yaml` for Custom Prompts

If you want to customize the prompt used by `/blog_post` & `/slack_post` endpoints, you can update the `prompt.yaml` file located in the root directory of the project. This file allows you to define the structure and content of the prompt(s).

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

### 1. Blog Post Generator
**Endpoint**: `/blog_post/<video_id_youtube>`
**Method**: `GET`
**Description**: Creates a blog post based on the video’s title, description, and transcript.

### 2. Slack Post Generator
**Endpoint**: `/slack_post/<video_id_youtube>`
**Method**: `GET`
**Description**: Creates a slack post based on the video’s title, description, and transcript.


**Optional Parameter**:
- `use_openai`: If set to `true`, the blog post will be generated using OpenAI. If not provided, the default is `false`, and the blog post will be generated using the local model.

**Example**:
```bash
curl http://localhost:5000/blog_post/VIDEO_ID_YOUTUBE?use_openai=true
```

## Examples of Generated Blog Posts

In the `examples-blog-posts-generated` folder, you will find two main directories: `Ollama` and `OpenAI`. Each of these directories contains subfolders with examples of blog posts generated by the application. Each example is stored in its own folder and includes the following files:

1. `{youtube_video_id}.json`: This file contains the response of the endpoint `/blog_post/`, including metadata about the video, its transcript, and the generated blog post.
2. `blog_post.md`: This file contains the blog post generated from the video in a readable markdown format.

These examples demonstrate the capabilities of the application in generating blog posts from YouTube videos using different models.

### Example Structure
```
examples-blog-posts-generated/
├── video1/
│   ├── info.txt
│   └── blog_post.txt
├── video2/
│   ├── info.txt
│   └── blog_post.txt
```
## Model Performance, Execution Time, and Tokens (personal experience with this project)

When using OpenAI via API, the `/blog_post` endpoint executes in under 10 seconds, delivering consistent and accurate results.

However, when using DeepSeek-R1 or Llama 3.1 models with Ollama, performance can vary depending on the setup. Initially, I experienced very slow response times (over 5 minutes for transcripts of around 1 hour), but this was due to running the Ollama Docker image, which did not utilize my Mac M3’s GPU.

### Explanation:
- **Execution Time:** Execution Time: Local models such as DeepSeek-R1 and Llama 3.1 require more computational resources, and performance depends on how they are run. When running Ollama natively on macOS, it leverages Apple’s Metal API, significantly improving speed. However, when using the Dockerized Ollama image, performance is much slower because Docker cannot access the Mac’s GPU.
- **Recommended Setup:** If you are on a Mac with an M-series chip, it is best to run Ollama natively and have the Flask app communicate with it via API. If you still want to run Ollama inside Docker, use the `docker-compose-ollamadockerized.yml` file available in this repo.

### Tokens:
Models process text in units called "tokens." Longer video transcripts increase the token count, which can impact processing time. Performance varies depending on the model and hardware—local models may experience slower processing or incomplete results if they lack sufficient computational resources.

### Transcript Length and Language:
For video transcripts of about 5 minutes, all models perform well.

For transcripts up to 1 hour, OpenAI (via API) and models run with Ollama (when executed natively on macOS) both provide reliable results in a reasonable time, with OpenAI performing slightly better in my subjective evaluation. However, I did not conduct formal benchmarking. For longer videos or when using local models inside Docker, performance may vary, and further testing or adjustments may be necessary.


