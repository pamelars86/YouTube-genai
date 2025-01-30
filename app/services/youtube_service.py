import os
import google.auth
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from dotenv import load_dotenv
from app import logger

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_youtube_service():
    creds = None
    if os.path.exists('token.json'):
        creds = google.auth.load_credentials_from_file('token.json')[0]
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', ['https://www.googleapis.com/auth/youtube.force-ssl'])
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('youtube', 'v3', credentials=creds)


def get_youtube_service_with_api_key():
    return build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def get_youtube_video(video_id, withAPIKey=False):
    try:
        if withAPIKey:
            youtube = get_youtube_service_with_api_key()
        else:
            youtube = get_youtube_service()

        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        )
        response = request.execute()

        if "items" not in response or len(response["items"]) == 0:
            return {"error": "Video no encontrado"}

        video_info = response["items"][0]["snippet"]
        statistics = response["items"][0]["statistics"]
        content_details = response["items"][0]["contentDetails"]

        return {
            "title": video_info["title"],
            "description": video_info["description"],
            "channelTitle": video_info["channelTitle"],
            "publishedAt": video_info["publishedAt"],
            "viewCount": statistics.get("viewCount", 0),
            "likeCount": statistics.get("likeCount", 0),
            "duration": content_details["duration"],  # Duration in ISO 8601 format
        }

    except Exception as e:
        logger.error(f"Error retrieving video information: {e}")
        return {"error": str(e)}

def get_all_youtube_videos():
    youtube = get_youtube_service()
    request = youtube.videos().list(part="snippet", mine=True)
    response = request.execute()
    return response['items']


def get_video_transcript(video_id):
    languages_to_try = ['en', 'es', 'pt']
    formatter = TextFormatter()

    for lang in languages_to_try:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])

            formatted_transcript = formatter.format_transcript(transcript)

            return formatted_transcript
        except Exception as e:
            logger.error(f"Could not retrieve transcript in '{lang}'. Error: {e}")

    logger.error("No transcript found in any of the specified languages.")
    return None