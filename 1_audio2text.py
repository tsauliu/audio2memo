#%%
from openai import OpenAI
from env import keysecret
import json

client = OpenAI(
    api_key=keysecret
)

audio_file = open("test.m4a", "rb")
transcript = client.audio.transcriptions.create(
  model="gpt-4o-transcribe",
  file=audio_file
)

print(transcript.text)
# Save the transcript to a text file
with open("transcript.txt", "w", encoding="utf-8") as f:
    f.write(transcript.text)

print("Transcript saved to transcript.txt")

