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
        video_info_id = response["items"][0]["id"]
        statistics = response["items"][0]["statistics"]
        content_details = response["items"][0]["contentDetails"]

        return {
            "url": f"https://www.youtube.com/watch?v={video_info_id}",
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


def get_video_transcript(video_id, title=None, description=None):
    try:

        transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
        available_languages = [t.language_code for t in transcripts]

        languages_to_try = ['en', 'es', 'pt']

        for lang in languages_to_try:
            if lang in available_languages:
                manual_transcript = next((t for t in transcripts if not t.is_generated and lang in t.language_code), None)
                if manual_transcript:
                    logger.info(f"✅ Using manual transcript in {lang}")
                    transcript_data = manual_transcript.fetch()
                else:
                    auto_transcript = next((t for t in transcripts if t.is_generated and lang in t.language_code), None)
                    if auto_transcript:
                        logger.warning(f"⚠️ Using auto-generated transcript in {lang}. It may contain errors.")
                        transcript_data = auto_transcript.fetch()

                if transcript_data:
                    transcript_text = "\n".join([entry['text'] for entry in transcript_data])
                    return transcript_text

        logger.error("❌ No transcript available in the specified languages.")
        return None

    except Exception as e:
        logger.error(f"❌ Error retrieving transcripts: {e}")
        return None