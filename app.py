import streamlit as st  # type: ignore
from yt_dlp import YoutubeDL  # type: ignore
import os
import tempfile
import requests    

# 🔑 Add your YouTube Data API key here
API_KEY = "AIzaSyBqnLbn8m8hmbOorgc2rGFfOaYl7BCfZz4"

# Set page config
st.set_page_config(page_title="MediaSnatcher", page_icon="🎬")
st.title("🎬 Media Snatcher")
st.write("Download your favorite audio and video files easily!")

# Sidebar - Download Options
st.sidebar.header("📥 Download Settings")

video_url = st.text_input("🔗 Enter Video URL:")

download_type = st.sidebar.radio("What do you want to download?", ("Audio (MP3)", "Video (MP4)"))

if download_type == "Audio (MP3)":
    audio_quality = st.sidebar.selectbox("Select Audio Quality:", ("128", "192", "320"))
else:
    video_quality = st.sidebar.selectbox("Select Video Resolution:", ("360p", "480p", "720p", "1080p"))

# Extract thumbnail via YouTube Data API (if applicable)
def get_youtube_thumbnail(video_url):
    try:
        if "youtube.com" in video_url or "youtu.be" in video_url:
            video_id = ""
            if "youtu.be" in video_url:
                video_id = video_url.split("/")[-1].split("?")[0]
            elif "v=" in video_url:
                video_id = video_url.split("v=")[1].split("&")[0]
            elif "shorts" in video_url:
                video_id = video_url.split("shorts/")[-1].split("?")[0]

            api_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={API_KEY}"
            response = requests.get(api_url)
            data = response.json()
            if "items" in data and len(data["items"]) > 0:
                return data["items"][0]["snippet"]["thumbnails"]["high"]["url"]
    except:
        return None
    return None

# Main action button
if st.button("🚀 Prepare Download"):
    if video_url:
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                # FFmpeg detection
                ffmpeg_path = "C:/ffmpeg/ffmpeg-7.1.1-essentials_build/bin/ffmpeg.exe"
                ffmpeg_location = ffmpeg_path if os.path.exists(ffmpeg_path) else None

                # Basic options
                ydl_opts = {
                    'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                    'forceipv4': True,
                    'cookiefile': 'cookies.txt',
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                }

                # Customizing based on choice
                if download_type == "Audio (MP3)":
                    ydl_opts.update({
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': audio_quality,
                        }]
                    })
                else:  # Video
                    format_map = {
                        "360p": "bestvideo[height<=360]+bestaudio/best[height<=360]",
                        "480p": "bestvideo[height<=480]+bestaudio/best[height<=480]",
                        "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
                        "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
                    }
                    ydl_opts['format'] = format_map.get(video_quality, 'best')

                if ffmpeg_location:
                    ydl_opts['ffmpeg_location'] = ffmpeg_location

                # Start Download
                with YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(video_url, download=True)
                    thumbnail_url = info_dict.get("thumbnail") or get_youtube_thumbnail(video_url)

                    if thumbnail_url:
                        st.image(thumbnail_url, caption="Thumbnail", use_container_width=True)

                    downloaded_filename = ydl.prepare_filename(info_dict)
                    base, ext = os.path.splitext(downloaded_filename)

                    if download_type == "Audio (MP3)":
                        final_filename = base + '.mp3'
                        mime_type = 'audio/mpeg'
                    else:
                        final_filename = downloaded_filename
                        mime_type = 'video/mp4'

                    if os.path.exists(final_filename):
                        st.success(f"✅ {download_type} ready! Click below to download.")
                        st.balloons()

                        with open(final_filename, "rb") as f:
                            st.download_button(
                                label=f"⬇️ Download {download_type}",
                                data=f,
                                file_name=os.path.basename(final_filename),
                                mime=mime_type
                            )
                    else:
                        st.error("❌ Error: File not found.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
    else:
        st.error("❗ Please enter a valid URL.")
