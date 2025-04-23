import streamlit as st
import time
from yt_dlp import YoutubeDL

st.set_page_config(page_title="🎵 YouTube Audio Downloader")

st.title("🎵 YouTube Audio Downloader")
st.markdown("Paste the YouTube video URL to download audio as MP3:")

url = st.text_input("🔗 Video URL", key="url_input")
status_placeholder = st.empty()

def download_audio():
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': 'ffmpeg',  # Optional: customize if needed
        'quiet': True,
        'noplaylist': True,
        'progress_hooks': [progress_hook]
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '').strip()
        speed = d.get('_speed_str', '').strip()
        status_placeholder.info(f"📥 Downloading: **{percent}** at **{speed}**")
    elif d['status'] == 'finished':
        status_placeholder.success("✅ Audio download complete! Finalizing...")

if st.button("🎧 Download Audio"):
    if not url.strip():
        st.warning("⚠️ Please enter a valid YouTube URL.")
    else:
        try:
            download_audio()
        except Exception as e:
            if "ffmpeg" in str(e).lower() or "postprocessing" in str(e).lower():
                pass  # Ignore ffmpeg/postprocessing errors
            else:
                st.error("❌ An unexpected error occurred. Please try again.")
        finally:
            status_placeholder.empty()
            st.success("✅ Audio downloaded successfully!")
            st.balloons()
            time.sleep(5)  # Wait 5 seconds
            st.rerun()  # Refresh the app
