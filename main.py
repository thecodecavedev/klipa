import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai._gaos.types.interactions import model
from pydantic import config
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
transcript = []


def main():
    ytt_api = YouTubeTranscriptApi()
    client = genai.Client()
    T = ytt_api.fetch("YjVuJjmgclU")
    """
    snippet = {
    text:"this is some text",
    start:08:10,
    end:08:15
    }
    """
    for s in T:
        snippet = {"text": s.text, "start": s.start, "end": s.duration}
        transcript.append(snippet)

    PROMPT = f"You are a seasoned clipper with years of experience in analyzing youtube videos and identifying best part from the vvideos and grabbing them to create clips that go viral on tiktok and youtube shorts. You also have analyzed millions of videos and understand what makes a trending video and what make for a best clip from a video. Use you understanding and take this video's transcript {transcript} and identify the best parts to clip. return 5 videos in this range (30 to 60 seconds) in json formart that has (name,start,end,duration,reason why video will trend, trend score out of 10). make sure the times are in minutes and seconds not just seconds. the expected output is just the json an that is all no text explaining anything just the json export only"

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=PROMPT,
        config=types.GenerateContentConfig(
            temperature=0,
        ),
    )

    print(response.text)


if __name__ == "__main__":
    main()
