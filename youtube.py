#!/usr/bin/env python3

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import os
import re
import datetime
import csv
load_dotenv()

directory = os.environ.get("DIRECTORY_PATH")
formatter = TextFormatter()


def get_video_title(video_url):
    try:
        # Send request to YouTube
        response = requests.get(video_url)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # First try to get the title from meta tags (more reliable)
        meta_title = soup.find('meta', property='og:title')
        if meta_title and meta_title.get('content'):
            return meta_title['content']

        # Fallback: try to get the title from the title tag
        title_tag = soup.find('title')
        if title_tag:
            # Remove the " - YouTube" suffix if present
            title = title_tag.string.replace(' - YouTube', '')
            return title.strip()

        raise Exception("Could not find video title")
    except Exception as e:
        print(f"Error fetching video title: {e}")
        return None


def to_camel_case(s):
    parts = s.split('-')
    # Capitalize the first letter of each part except the first one
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])


def clean_string(input_string):
    # Replace all non-alphanumeric characters with dashes
    cleaned_string = re.sub(r'[^a-zA-Z0-9]+', '-',
                            input_string).strip('-').lower()
    # Convert to camelCase
    camel_case_string = to_camel_case(cleaned_string)
    return camel_case_string


def write_transcript_to_file(title, transcript, url):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    video_title = clean_string(title)
    file_name = f"{video_title}.txt"

    folder_path = os.path.join(directory, current_date)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Update the file path to include the folder
    file_path = os.path.join(folder_path, file_name)

    with open(file_path, "w") as file:
        file.write(f"{title}\n\n")
        file.write(f"{url}\n\n")
        file.write(transcript)

    print(f"Transcript saved to {file_name}")
    return file_path


def get_youtube_transcript(video_url):
    id = video_url.split("v=")[1]
    try:
        transcript = YouTubeTranscriptApi.get_transcript(id)
        print("transcript unformatted")
        print(transcript)
        formatted = formatter.format_transcript(transcript)
        print("formatted")
        print(formatted)
        file = " ".join([entry['text'] for entry in transcript])
        return file
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None


def generate_transcript(url):
    name = get_video_title(url)
    print(name)
    file = get_youtube_transcript(url)
    file_path = write_transcript_to_file(name, file, url)
    return file_path


def parse_file_and_generate_transcript(file_path):
    items = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(row)
            url = row['url']
            print(url)
            print("generating transcript: ")
            file_path = generate_transcript(url)
            items.append(file_path)
    return items
