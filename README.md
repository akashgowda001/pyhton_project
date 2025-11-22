# Video Communication Insights

Simple Streamlit app for the November 2025 Python Assessment.

## What it does
- Accepts a public video URL (YouTube/Loom/MP4).
- Downloads video, extracts audio, transcribes via OpenAI Whisper.
- Uses an LLM to produce:
  - **Clarity Score** (0-100)
  - **Communication Focus** (one sentence)
  - **Speaking Pace** (WPM)

## Setup (local)
1. Install Python 3.10+ and ffmpeg.
2. Create and activate a virtualenv:
