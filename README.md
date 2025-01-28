# YouTube Summary and Blog Generator

This project leverages Generative AI (GenAI) to perform two main functionalities:

1. **Video Summary**: Generates a concise summary of a YouTube video based on its transcript, description, and title.
2. **Medium-style Blog Post**: Creates a detailed blog post in the style of Medium articles using the same input data.

The application is fully containerized with Docker for easy setup and deployment.

---

## Prerequisites

Before starting, ensure you have the following installed:
- Docker and Docker Compose
- A Google Cloud service account with access to YouTube Data API
- The following files ready in the project directory:
  - `.env`: Contains your API key
  - `client_secrets.json`: Configured for your service account

---

## Setup

### 1. Create the `.env` File
In the root of the project, create a `.env` file with the following variable:  YOUTUBE_API_KEY=<Your_YouTube_Data_API_Key>

Replace `<Your_YouTube_Data_API_Key>` with your actual API key from the Google Cloud Console.

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
### 3. Build and Run the Dockerized App

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
**Description**: Creates a Medium-style blog post based on the video’s title, description, and transcript.

**Example**:
```bash
curl http://localhost:5000/video_blog/VIDEO_ID_YOUTUBE
```