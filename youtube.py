from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import os
import re
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)
directory = os.environ.get("DIRECTORY_PATH")

def clean_string(input_string):
    # Remove all non-alphanumeric characters
    cleaned_string = re.sub(r'[^a-zA-Z0-9]', '', input_string).lower()
    return cleaned_string


def write_transcript_to_file(title, transcript):
  video_title = clean_string(title)
  file_name = f"{video_title}.txt"
  file_path = os.path.join(directory, file_name)
  
  with open(file_path, "w") as file:
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
    print(url)
    print(name)
    transcript = generate_openai_transcript(url)
    print(transcript)
    write_transcript_to_file(name, transcript)
        
