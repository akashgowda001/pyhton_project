import os
import json
from pathlib import Path

import yt_dlp
import ffmpeg
import openai


def set_openai_key(key: str):
    openai.api_key = key


def download_video(url: str, out_dir: str = "downloads") -> str:
    os.makedirs(out_dir, exist_ok=True)

    options = {
        "outtmpl": os.path.join(out_dir, "%(id)s.%(ext)s"),
        "format": "bestvideo+bestaudio/best",
        "quiet": True
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)


def extract_audio(video_path: str, out_dir: str = "audio") -> str:
    os.makedirs(out_dir, exist_ok=True)

    output_path = os.path.join(out_dir, Path(video_path).stem + ".wav")

    ffmpeg.input(video_path).output(
        output_path, ac=1, ar="16000", format="wav"
    ).overwrite_output().run(quiet=True)

    return output_path


def transcribe_with_openai(audio_path: str, model="whisper-1") -> str:
    with open(audio_path, "rb") as audio:
        response = openai.Audio.transcribe(model=model, file=audio)
        return response["text"]


def analyze_transcript_with_llm(text: str) -> dict:
    prompt = f"""
Analyze the following transcript and respond in JSON format:

{text}

Return output as:
{{
  "clarity_score": number,
  "communication_focus": "string",
  "speaking_wpm": number,
  "explanation": "string"
}}
"""

    response = openai.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except:
        return {
            "clarity_score": None,
            "communication_focus": "",
            "speaking_wpm": None,
            "explanation": "Invalid JSON"
        }
