#!/usr/bin/env python3

import sys

from youtube import generate_transcript

def main():
    if len(sys.argv) > 1:
        print(f"Arguments received: {', '.join(sys.argv[1:])}")
        print(f"Arguments received: {', '.join(sys.argv[2:])}")
        
        url = ', '.join(sys.argv[1:]) #sys.argv[1:]
        name =', '.join(sys.argv[2:]) # sys.argv[2:]
        print(url)
        print(name)
        generate_transcript(url, name)
    else:
        print("No arguments provided.")

if __name__ == "__main__":
    main()
    
    