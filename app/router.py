from flask import jsonify
from app.services.youtube_service import get_video_transcript, get_youtube_video, get_all_youtube_videos
from app.services.summary_service import summarize_transcript, generate_blog_post
from . import app

@app.route('/')
def index():
    return "Welcome to the YouTube Summary App!"

# Route to get a summary of a video
@app.route('/video_summary/<video_id>', methods=['GET'])
def video_summary(video_id):
    video_info = get_youtube_video(video_id, withAPIKey=True)
    transcript = get_video_transcript(video_id)
    video_info["transcript"] = transcript

    summary = summarize_transcript(transcript, video_info["title"], video_info["description"])

    return jsonify({"video_info": video_info, "summary": summary})

# Route to get all YouTube videos
@app.route('/all_videos', methods=['GET'])
def all_videos():
    videos = get_all_youtube_videos()
    return jsonify(videos)


# Route to get a blog post of a video
@app.route('/blog_post/<video_id>', methods=['GET'])
def blog_post(video_id):
    video_info = get_youtube_video(video_id, withAPIKey=True)
    transcript = get_video_transcript(video_id)
    video_info["transcript"] = transcript
    blog_post = generate_blog_post(transcript, video_info["title"], video_info["description"])

    return jsonify({"video_info": video_info, "blog_post": blog_post})
