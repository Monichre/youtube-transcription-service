#!/usr/bin/env python3

import sys
from youtube import generate_transcript
import argparse
import os
from openai_upload import upload_file_to_openai 
def main():
    parser = argparse.ArgumentParser(description="Generate transcripts from YouTube videos.")
    parser.add_argument('url', help="URL of the YouTube video")
    parser.add_argument('name', help="Name of the output file")
    parser.add_argument('--upload', action='store_true', help="Upload the transcript to OpenAI")
    args = parser.parse_args()
    
    print(f"URL received: {args.url}")
    print(f"Output file name received: {args.name}")
    
    file_path = generate_transcript(args.url, args.name)
    
    if args.upload:
        if os.path.exists(file_path):
            upload = upload_file_to_openai(file_path)
            print(upload)
            return upload
    else:
        print(f"The youtube video was transcribed but not uploaded")

if __name__ == "__main__":
    main()
    
    