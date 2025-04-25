import streamlit as st
from yt_dlp import YoutubeDL
import os
import tempfile

st.title("🎵 Sounds Snatcher")
st.write("Paste the video URL from any social media platform to download audio as MP3:")

video_url = st.text_input("🔗 Video URL")

if video_url:
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            if st.button("Download Audio"):
                with YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(video_url, download=True)
                    # ✅ Use yt-dlp's internal filename detection
                    downloaded_filename = ydl.prepare_filename(info_dict)
                    base, _ = os.path.splitext(downloaded_filename)
                    mp3_filename = base + '.mp3'

                    if os.path.exists(mp3_filename):
                        st.success("✅ Audio downloaded successfully!")
                        with open(mp3_filename, "rb") as f:
                            st.download_button(
                                label="⬇️ Download MP3",
                                data=f,
                                file_name=os.path.basename(mp3_filename),
                                mime="audio/mpeg"
                            )
                    else:
                        st.error("❌ File was not found after download.")
    except Exception as e:
        st.error(f"❌ Error: {e}")
