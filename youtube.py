#!/usr/bin/env python3

from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import os
import re
load_dotenv()

# client = OpenAI(
#     api_key=os.environ.get("OPENAI_API_KEY"),
# )
directory = os.environ.get("DIRECTORY_PATH")
print(directory)

def to_camel_case(s):
    parts = s.split('-')
    # Capitalize the first letter of each part except the first one
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

def clean_string(input_string):
    # Replace all non-alphanumeric characters with dashes
    cleaned_string = re.sub(r'[^a-zA-Z0-9]+', '-', input_string).strip('-').lower()
    # Convert to camelCase
    camel_case_string = to_camel_case(cleaned_string)
    return camel_case_string


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
    return youtube_transcript



def generate_transcript(url, name):
    print(url)
    print(name)
    transcript = generate_openai_transcript(url)
    write_transcript_to_file(name, transcript)
        
