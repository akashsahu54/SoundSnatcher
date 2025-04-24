import streamlit as st
from yt_dlp import YoutubeDL
import os

st.title("🎵 YouTube Audio Downloader")
st.write("Paste the YouTube video URL to download audio as MP3:")

video_url = st.text_input("🔗 Video URL")

if video_url:
    try:
        # Output directory
        output_dir = "downloads"
        os.makedirs(output_dir, exist_ok=True)

        # Set up the downloader options
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
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
                file_path = os.path.join(output_dir, filename)

                if os.path.exists(file_path):
                    st.success("✅ Audio downloaded successfully!")
                    st.write(f"**Saved as:** `{file_path}`")

                    # Show download button
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
        st.error(f"❌ An unexpected error occurred: {e}")
