import os
import streamlit as st
from utils import (
    set_openai_key,
    download_video,
    extract_audio,
    transcribe_with_openai,
    analyze_transcript_with_llm,
)

st.set_page_config(page_title="Video Insights", layout="centered")
st.title("🎥 AI Video Communication Insights")

st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("OpenAI API Key", type="password")

if api_key:
    set_openai_key(api_key)
elif os.getenv("OPENAI_API_KEY"):
    set_openai_key(os.getenv("OPENAI_API_KEY"))

url = st.text_input("Paste public video URL (YouTube/Loom/mp4)")

if st.button("Analyze"):
    if not url:
        st.error("⚠ Please enter a URL before continuing.")
        st.stop()

    st.write("🔄 Processing... Please wait.")

    try:
        video_path = download_video(url)
        st.success("✔ Video downloaded")
    except Exception as e:
        st.error(f"❌ Download failed: {e}")
        st.stop()

    try:
        audio_path = extract_audio(video_path)
        st.success("✔ Audio extracted")
    except Exception as e:
        st.error(f"❌ Audio extraction failed: {e}")
        st.stop()

    try:
        transcript = transcribe_with_openai(audio_path)
        st.text_area("📄 Transcript (Preview)", transcript[:5000], height=250)
    except Exception as e:
        st.error(f"❌ Transcription failed: {e}")
        st.stop()

    try:
        report = analyze_transcript_with_llm(transcript)
        st.success("✔ AI Analysis Completed")
    except Exception as e:
        st.error(f"❌ Analysis failed: {e}")
        st.stop()

    st.header("📌 Communication Insights")
    st.metric("Clarity Score", f"{report.get('clarity_score', 'N/A')} / 100")
    st.metric("Speaking Pace", f"{report.get('speaking_wpm', 'N/A')} WPM")

    st.subheader("🧠 Communication Focus")
    st.write(report.get("communication_focus", "No data"))

    if report.get("explanation"):
        st.info(f"💡 Note: {report.get('explanation')}")

if st.button("Clear Results"):
    st.experimental_rerun()
