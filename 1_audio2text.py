
#%%
from openai import OpenAI
from env import keysecret
import os
import datetime

timestart=datetime.datetime.now()
print(f'start time: {timestart}')

client = OpenAI(
    api_key=keysecret
)

filename='hype 交接1_part2'
audio_file = open(f"./0_processed_audio/{filename}.m4a", "rb")

transcript = client.audio.transcriptions.create(
  model="gpt-4o-transcribe", #gpt-4o-mini-transcribe / gpt-4o-transcribe
  file=audio_file
)

print(transcript.text)
# Save the transcript to a text file
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
with open(f"./1_transcript/{filename}_{timestamp}.txt", "w", encoding="utf-8") as f:
    f.write(transcript.text)

print("Transcript saved to transcript.txt")
timeend=datetime.datetime.now()
print(f'end time: {timeend}')
print(f'total time: {timeend-timestart}')

