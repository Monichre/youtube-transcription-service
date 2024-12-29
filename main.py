#!/usr/bin/env python3

import sys
from youtube import generate_transcript, parse_file_and_generate_transcript
import argparse
import os
from openai_upload import upload_file_to_openai


def main():
    parser = argparse.ArgumentParser(
        description="Generate transcripts from YouTube videos.")
    parser.add_argument('--url', help="URL of the YouTube video")
    # parser.add_argument('name', nargs='?', default=None, help="Name of the output file (optional, defaults to the URL if not provided)")
    parser.add_argument('--upload', action='store_true',
                        help="Upload the transcript to OpenAI")
    parser.add_argument('--file', action='store_true')
    parser.add_argument('--urls',
                        help="Provide path to the urls file")
    args = parser.parse_args()

    print(f"URL received: {args.url}")
    print(f"Input file path received: {args.file}")

    if args.urls:
        file_paths = parse_file_and_generate_transcript(args.urls)
        print(file_paths)
        if args.upload:
            for transcript_path in file_paths:
                upload_transcript = upload_file_to_openai(transcript_path)
                print(upload_transcript)
        return file_paths
    else:
        file_path = generate_transcript(args.url)

        if args.upload:
            if os.path.exists(file_path):
                upload = upload_file_to_openai(file_path)
                print(upload)
                return upload
        else:
            print(f"The youtube video was transcribed but not uploaded")


# if __name__ == "__main__":
main()
