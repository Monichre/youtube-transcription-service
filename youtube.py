from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi
import os
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)



def write_transcript_to_file(title, transcript):
  video_title = title.replace(" ", "-").replace(":", "-").replace("#", "-").lower()
  file_name = f"{video_title}.txt"
  
  with open(file_name, "w") as file:
    file.write(transcript)
  
  print(f"Transcript saved to {file_name}")

def get_youtube_transcript(id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(id)
        return " ".join([entry['text'] for entry in transcript])
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None

def generate_openai_transcript(video_url):
    video_id = video_url.split("v=")[1]
    youtube_transcript = get_youtube_transcript(video_id)
    print(youtube_transcript)
    return youtube_transcript



def generate_transcript(url, name):
  for video in videos:
    print(url)
    print(name)
    transcript = generate_openai_transcript(url)
    print(transcript)
    write_transcript_to_file(name, transcript)
        
