from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi
import os
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

youtube_videos = [
# {"url": "https://www.youtube.com/watch?v=3jCPjlB60L4", "title": "Dave Foley's UFO Adventure : WEAPONIZED : EPISODE #15"},
{"url": "https://www.youtube.com/watch?v=C8Z6IBxC0v0", "title": "Russian Scientists Risked Everything to investigate UFOs : WEAPONIZED : EPISODE #16"},
{"url": "https://www.youtube.com/watch?v=Ds16_9XK1RQ", "title": "Robbie Williams Conquers The World : WEAPONIZED : EPISODE #17"},
{"url": "https://www.youtube.com/watch?v=PpVkN6SaLjw", "title": "The Silent Triangle Of Twentynine Palms : WEAPONIZED : EPISODE #18"},
{"url": "https://www.youtube.com/watch?v=WHIry_C1MTc", "title": "Mystery In The Mojave - Case Closed? : WEAPONIZED : EPISODE #19"},
{"url": "https://www.youtube.com/watch?v=KMRt8dAPJ8Y", "title": "Lord Huron - Life & Death With The Cosmic Cowboys : WEAPONIZED : EPISODE #20"},
{"url": "https://www.youtube.com/watch?v=dc6V0O_OPJ0", "title": "Confessions Of A UFO Insider - The David Grusch Revelations : WEAPONIZED : EPISODE #21"},
{"url": "https://www.youtube.com/watch?v=FeqEPzJHVis", "title": "WHO ARE THE VISITORS & WHY ARE THEY HERE? : WEAPONIZED : EPISODE #23"},
{"url": "https://www.youtube.com/watch?v=D06uQdk2cys", "title": "Allied UFO Reverse-Engineering Programs Confirmed : WEAPONIZED : EPISODE #22"},
{"url": "https://www.youtube.com/watch?v=hR1qPjKQQao", "title": "The End Of UFO Secrecy? : WEAPONIZED : EPISODE #24"},
{"url": "https://www.youtube.com/watch?v=63PHhwglBdo", "title": "The Hunt For Crashed Saucers : WEAPONIZED : EPISODE #25"},
{"url": "https://www.youtube.com/watch?v=nfchje15k00", "title": "UFO Bombs Dropped On Capitol Hill : WEAPONIZED : EPISODE #26"},
{"url": "https://www.youtube.com/watch?v=4opsdH4hY3s", "title": "The Man Who Filmed The TIC TAC UFO : WEAPONIZED : EPISODE #27"},
{"url": "https://www.youtube.com/watch?v=t2xSFMkmWg4", "title": "The UFO Hearing - What Happened? What’s Next? : WEAPONIZED : EPISODE #28"},
{"url": "https://www.youtube.com/watch?v=zRkh3xh5_yU", "title": "CDR David Fravor  -The Best UFO Witness Ever? : WEAPONIZED : EP #29"},
{"url": "https://www.youtube.com/watch?v=kJR_pSZjUdk", "title": "The Empire Strikes Back - The Sliming of David Grusch : WEAPONIZED : EP #30"},
{"url": "https://www.youtube.com/watch?v=oQCRhJ9Yaho", "title": "Fighting Back Against Animal Cruelty : WEAPONIZED : EP #31"},
{"url": "https://www.youtube.com/watch?v=-KN6ixGagHI", "title": "The Godfather Of Conspiracy - John Lear : WEAPONIZED : EP #32"},
{"url": "https://www.youtube.com/watch?v=rvtSHCWqOwc", "title": "The Quest For UFO Transparency : WEAPONIZED : EP #33"},
{"url": "https://www.youtube.com/watch?v=uXiXuhxxpMY", "title": "Fight The Power - UFO Transparency : WEAPONIZED : EP #34"},
{"url": "https://www.youtube.com/watch?v=2bJOiyRm5KA", "title": "Alien Invasion - War Of The Worlds Redux? : WEAPONIZED : EP #35"},
{"url": "https://www.youtube.com/watch?v=KkJHymf8OlA", "title": "Virtual Reality And The Evolution Of Non-Human Intelligence : WEAPONIZED : EP #36"},
{"url": "https://www.youtube.com/watch?v=H9Yr_bflXec", "title": "Psychic Spies & Alien Civilizations - What’s The Connection? : WEAPONIZED : EP #37"},
{"url": "https://www.youtube.com/watch?v=ow7FqiegixQ", "title": "Inside the DIAs Secretive UFO Investigation : WEAPONIZED : EP #38"},
{"url": "https://www.youtube.com/watch?v=Tab3igcWnuE", "title": "UFO Earthquake - Dr. Lacatski's Bombshell & AARO's Shaky Ground : WEAPONIZED : EP #39"},
{"url": "https://www.youtube.com/watch?v=kgm06ChglBo", "title": "Congress Crashes Into Wall Of UFO Secrecy : WEAPONIZED : EP #40"},
{"url": "https://www.youtube.com/watch?v=U6LyHl559qo", "title": "SHOOT THEM DOWN! Military Uses Lethal Force against UFOs : WEAPONIZED : EP #41"},
{"url": "https://www.youtube.com/watch?v=2nw1ySM8eDo", "title": "Cosmic Conspiracies - Breaking the Code of UFO Secrecy! : WEAPONIZED : EP #42"},
{"url": "https://www.youtube.com/watch?v=eyCftd_FHwE", "title": "Saucers, Bodies, Debris - The Lost Tapes Of UFO Whistleblower Col. Corso : WEAPONIZED : EPISODE #43"},
{"url": "https://www.youtube.com/watch?v=TtNFpldgxUM", "title": "The Fight For UFO Disclosure Is Just Beginning : WEAPONIZED : EPISODE #44"},
{"url": "https://www.youtube.com/watch?v=tDROoJTxfPA", "title": "UFOlogy's DARTH VADER Changes His Tune About CRASHED SAUCERS : WEAPONIZED : EPISODE #45"},
{"url": "https://www.youtube.com/watch?v=CTwfySckKUM", "title": "The History Of UFO Disclosure - Can The Public Handle The Truth? : WEAPONIZED : EPISODE #46"},
{"url": "https://www.youtube.com/watch?v=aqsqcJ6DZsg", "title": "THE JELLYFISH UFO - How It Happened & What It Means : WEAPONIZED : EPISODE #47"},
{"url": "https://www.youtube.com/watch?v=E0XzVpGqZNI", "title": "Ernie Cline - The Man Who Saw The Future : WEAPONIZED : EPISODE #48"},
{"url": "https://www.youtube.com/watch?v=mKKoDextN_I", "title": "UFO Propaganda - The Dark Side Unleashes : WEAPONIZED : EPISODE #49"},
{"url": "https://www.youtube.com/watch?v=lovRaL5IEGQ", "title": "What Washington Wants - First Hand UFO Witnesses : WEAPONIZED : EPISODE #50"},
{"url": "https://www.youtube.com/watch?v=i6b4stJk424", "title": "AARO Misses Target - Congress & The Public Are Pissed : WEAPONIZED : EPISODE #52"},
{"url": "https://www.youtube.com/watch?v=hNLHjlHhcTI", "title": "The Battle for UFO Truth - The Michael Corleone Edition : WEAPONIZED : EPISODE #53"},
{"url": "https://www.youtube.com/watch?v=-iOtvh7NZl0", "title": "UFOs and Nukes - The Pantex Incursions : WEAPONIZED : EPISODE #54"}
]

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



def generate_transcripts(videos):
  for video in videos:
    url = video['url']
    title = video['title']
    print(url)
    print(title)
    transcript = generate_openai_transcript(url)
    print(transcript)
    write_transcript_to_file(title, transcript)
        


generate_transcripts(youtube_videos)