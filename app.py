import streamlit as st # type: ignore
from yt_dlp import YoutubeDL # type: ignore
import os
import tempfile

st.title("🎵 Sounds Snatcher")
st.write("Paste the video URL from any social media platform to download audio as MP3:")

video_url = st.text_input("🔗 Video URL")

if video_url:
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # FFmpeg detection
            ffmpeg_path = "C:/ffmpeg/ffmpeg-7.1.1-essentials_build/bin/ffmpeg.exe"
            ffmpeg_location = ffmpeg_path if os.path.exists(ffmpeg_path) else None

            # YDL options
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'forceipv4': True,
                'cookiefile': 'cookies.txt',
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            }

            if ffmpeg_location:
                ydl_opts['ffmpeg_location'] = ffmpeg_location

            if st.button("Prepare Audio"):
                with YoutubeDL(ydl_opts) as ydl:
                    # Extract video info
                    info_dict = ydl.extract_info(video_url, download=True)
                    thumbnail_url = info_dict.get("thumbnail", None)

                    # Display thumbnail if available
                    if thumbnail_url:
                        st.image(thumbnail_url, caption="Video Thumbnail", use_container_width=True)

                    downloaded_filename = ydl.prepare_filename(info_dict)
                    base, _ = os.path.splitext(downloaded_filename)
                    mp3_filename = base + '.mp3'

                    if os.path.exists(mp3_filename):
                        st.success("✅ Audio prepared successfully!")
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
