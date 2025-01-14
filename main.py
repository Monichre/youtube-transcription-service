#!/usr/bin/env python3

import sys
from youtube import generate_transcript, parse_file_and_generate_transcript, write_transcript_to_file
import argparse
import os
from openai_upload import upload_file_to_openai
from web_content_processor import process_url
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(
        description="Generate transcripts from YouTube videos or scrape web content.")
    parser.add_argument('--url', help="URL of the YouTube video or webpage")
    parser.add_argument('--upload', action='store_true',
                        help="Upload the content to OpenAI")
    parser.add_argument('--file', action='store_true')
    parser.add_argument('--urls',
                        help="Provide path to the urls file")
    parser.add_argument('--scrape', action='store_true',
                        help="Scrape the URL instead of processing as YouTube video")
    args = parser.parse_args()

    if args.scrape and args.url:
        print(f"Scraping content from: {args.url}")
        processed_content = process_url(args.url)

        content = processed_content['content']
        metadata = processed_content['metadata']
        markdown = processed_content['markdown']
        summary = processed_content['summary']
        title = metadata['title']
        summary_title = f"{title} Summary"
        url = metadata['url']

        if content and summary:
            file_path = write_transcript_to_file(title, markdown, url, None)
            summary_path = write_transcript_to_file(
                summary_title, summary, url, None)
            print(f"Content saved to: {file_path}")

            if args.upload:
                upload = upload_file_to_openai(file_path)
                summary_upload = upload_file_to_openai(summary_path)
                print(upload)
                print(summary_upload)
                return upload, summary_upload
            return file_path, summary_path
        else:
            print("Failed to scrape content from the URL")
            return None

    elif args.url:
        file_path, summary_path = generate_transcript(args.url)
        if args.upload:
            if os.path.exists(file_path):
                upload = upload_file_to_openai(file_path)
                print(upload)
                return upload
            if os.path.exists(summary_path):
                summary_upload = upload_file_to_openai(summary_path)
                print(summary_upload)
                return summary_upload
        else:
            print(f"The youtube video was transcribed but not uploaded")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
