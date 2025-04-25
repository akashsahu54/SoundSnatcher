import streamlit as st
from yt_dlp import YoutubeDL
import os
import tempfile
import re

st.title("🎵 Sounds Snatcher")
st.write("Paste the YouTube video URL to download audio as MP3:")

video_url = st.text_input("🔗 Video URL")

def clean_filename(name):
    # Remove any characters not allowed in filenames
    return re.sub(r'[\\/*?:"<>|]', "", name)

if video_url:
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # 🔥 Set your local ffmpeg path (for Windows)
            ffmpeg_path = "C:/ffmpeg/ffmpeg-7.1.1-essentials_build/bin/ffmpeg.exe"  # <-- your path

            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                'ffmpeg_location': ffmpeg_path,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            if st.button("Download Audio"):
                with YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=True)
                    title = info.get("title", "audio")
                    safe_title = clean_filename(title)
                    filename = f"{safe_title}.mp3"
                    file_path = os.path.join(temp_dir, filename)

                    # Since yt-dlp names file before postprocessing, use actual location
                    for file in os.listdir(temp_dir):
                        if file.endswith(".mp3"):
                            file_path = os.path.join(temp_dir, file)
                            filename = file
                            break

                    if os.path.exists(file_path):
                        st.success("✅ Audio downloaded successfully!")
                        with open(file_path, "rb") as f:
                            st.download_button(
                                label="⬇️ Download MP3",
                                data=f,
                                file_name=filename,
                                mime="audio/mpeg"
                            )
                    else:
                        st.error("❌ File was not found after download.")
    except Exception as e:
        st.error(f"❌ Error: {e}")
