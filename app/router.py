from flask import jsonify
from flask import request

from app import logger

from app.services.youtube_service import get_video_transcript, get_youtube_video, get_all_youtube_videos
from app.services.summary_service import generate_blog_post
from . import app
import time

@app.route('/')
def index():
    return "Welcome to the YouTube Summary App!"

# Route to get all YouTube videos
@app.route('/all_videos', methods=['GET'])
def all_videos():
    videos = get_all_youtube_videos()
    return jsonify(videos)


# Route to get a blog post of a video
@app.route('/blog_post/<video_id>', methods=['GET'])
def blog_post(video_id):
    start_time = time.time()

    use_openai = request.args.get('use_openai', 'false').lower() == 'true'


    video_info = get_youtube_video(video_id, withAPIKey=True)
    transcript = get_video_transcript(video_id)

    blog_post = generate_blog_post(transcript, title=video_info["title"], description=video_info["description"], use_openai=use_openai)


    execution_time_sec = round(time.time() - start_time,3)
    execution_time_min = round(execution_time_sec / 60,3)

    logger.info(f"[blog_post] Execution time: {execution_time_sec} seconds")
    logger.info(f"[blog_post] Execution time: {execution_time_min} minutes")

    return jsonify({"video_info": video_info, "transcript": transcript, "blog_post": blog_post, "use_openai": use_openai, "execution_time_sec": execution_time_sec})