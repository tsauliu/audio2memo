
#%%
from openai import OpenAI
from env import keysecret
import os
import datetime
import concurrent.futures
import threading

timestart=datetime.datetime.now()
print(f'start time: {timestart}')

# 创建线程锁，用于保护API调用
api_lock = threading.Lock()

client = OpenAI(
    api_key=keysecret
)

def audio2text(filename):
    audio_file = open(f"./0_processed_audio/{project}/{filename}", "rb")
    # 使用锁保护API调用，避免并发请求可能的问题
    with api_lock:
        transcript = client.audio.transcriptions.create(
            model="gpt-4o-transcribe", #gpt-4o-mini-transcribe / gpt-4o-transcribe
            file=audio_file
        )
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"./1_transcript/{project}/{filename}_{timestamp}.txt", "w", encoding="utf-8") as f:
        f.write(transcript.text)
    print(f"Processed: {filename}")

project='hype 交接1'
if not os.path.exists(f"./1_transcript/{project}"):
    os.makedirs(f"./1_transcript/{project}")

audio_folder = f"./0_processed_audio/{project}"
audio_files = [filename for filename in os.listdir(audio_folder) if filename.endswith('.m4a')]

# 使用线程池执行多线程处理
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(audio2text, audio_files)

timeend=datetime.datetime.now()
print(f'end time: {timeend}')
print(f'total time: {timeend-timestart}')
