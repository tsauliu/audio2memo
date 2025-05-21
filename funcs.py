#%%
import os
from env import groq_key
from groq import Groq

def groq_transcribe(audio_filepath,transcript_filepath,input_model):
    client = Groq(api_key=groq_key)
    with open(audio_filepath, "rb") as file:
        transcription = client.audio.transcriptions.create(
        file=(audio_filepath, file.read()),
        model=input_model, #whisper-large-v3,whisper-large-v3-turbo
        response_format="verbose_json",
        temperature=0,
        )

    with open(transcript_filepath, "w", encoding="utf-8") as f:
        for segment in transcription.segments:
            f.write(segment['text']+'\n')

# %%
from openai import OpenAI
from env import keysecret


def openai_transcribe(audio_filepath,transcript_filepath,input_model):
    client = OpenAI(
        api_key=keysecret
    )

    with open(audio_filepath, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model=input_model, #gpt-4o-mini-transcribe / gpt-4o-transcribe / whisper-1
            file=audio_file,
            # temperature=0.2
        )
            
    with open(transcript_filepath, "w", encoding="utf-8") as f:
        f.write(transcript.text)



import os
import tiktoken

def combine_transcripts(filename):
    # 查找并合并所有相关的转录文件
    combined_transcript = ""
    transcript_files = sorted(
        [f for f in os.listdir(f'./1_transcript/{filename}') if f.endswith('.txt')],
        reverse=False
    )
    print(transcript_files)

    for file in transcript_files:
        with open(f'./1_transcript/{filename}/{file}', 'r', encoding='utf-8') as f:
            combined_transcript += f.read() + "\n\n"
    return combined_transcript

# %%
def count_tokens(text):
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


from openai import OpenAI
from env import api_key_deepseek,model_id_deepseek

client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3/bots",
    api_key=api_key_deepseek
)

def deepseek_model(prompt,content):
    def summary(content):
        completion = client.chat.completions.create(
            model=model_id_deepseek,
            messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": content},
        ],
        )
        return completion.choices[0].message.content
    return summary(content)

from google import genai
from google.genai import types
from env import gemini_key
client = genai.Client(api_key=gemini_key)

def gemini_model(prompt,content):
    modelname="gemini-2.5-pro-preview-05-06" #gemini-2.5-pro-preview-05-06，gemini-2.5-pro-preview-03-25，gemini-2.5-flash-preview-05-20
    print(f'{modelname} is used')
    response = client.models.generate_content(
        model=modelname,
        config=types.GenerateContentConfig(
        temperature=0.3
        ) , 
        contents=prompt+'\n -- \n'+content 
    )
    return response.text

def feishu_bot(message):
    import requests
    import json
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    payload_message = {
        "msg_type": "text",
        "content": {
            "text": message+f'\n {timestamp}'
            }
        }
    headers = {
        'Content-Type': 'application/json'
    }

    # 定义飞书机器人 URL
    url = "https://open.feishu.cn/open-apis/bot/v2/hook/36473a8e-3bf1-40bd-9115-3385e314bf74"  # 替换为你的飞书机器人 URL
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload_message))
    return response.text


import boto3
from env import oss_key,oss_access,bucket_name

def save_transcript_to_oss(filepath,filename):
    # try:
    if True:
        # 设置腾讯云COS的连接信息
        s3_client = boto3.client(
            's3',
            region_name='ap-beijing',  # 替换为您的存储桶所在地区
            aws_access_key_id=oss_key,  # 替换为您的access key
            aws_secret_access_key=oss_access,  # 替换为您的secret key
            config=boto3.session.Config(s3={'addressing_style': 'virtual'}),
            endpoint_url='https://cos.ap-beijing.myqcloud.com'  # 替换为对应地区的endpoint
        )

        # 上传文件
        s3_client.upload_file(
            Filename=f'{filepath}',
            Bucket=bucket_name,
            Key=f'/CallNotes/{filename}'
        )
        
    # except Exception as e:
    #     print(e)

if __name__ == '__main__':
    combine_transcripts(filename='catl jpm')
