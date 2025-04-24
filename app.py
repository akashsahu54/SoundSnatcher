import streamlit as st
from yt_dlp import YoutubeDL
import os

st.title("🎵 YouTube Audio Downloader")
st.write("Paste the YouTube video URL to download audio as MP3:")

video_url = st.text_input("🔗 Video URL")

if video_url:
    try:
        # Set up the downloader options
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',  # Directly save the file in the current directory
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        # Download when user clicks button
        if st.button("Download Audio"):
            with YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(video_url, download=True)
                title = info_dict.get('title', 'audio')
                filename = f"{title}.mp3"
                
                # Check if file exists in the current directory
                if os.path.exists(filename):
                    st.success("✅ Audio downloaded successfully!")
                    st.write(f"**Saved as:** `{filename}`")

                    # Show download button
                    with open(filename, "rb") as f:
                        st.download_button(
                            label="⬇️ Download MP3",
                            data=f,
                            file_name=filename,
                            mime="audio/mpeg"
                        )
                else:
                    st.error("❌ File was not found after download.")
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {e}")
