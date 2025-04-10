import os
import tiktoken

def combine_transcripts(filename):
    # 查找并合并所有相关的转录文件
    combined_transcript = ""
    transcript_files = sorted(
        [f for f in os.listdir(f'./1_transcript/{filename}') if f.endswith('.txt')],
        key=lambda x: int(x.split('_part')[1].split('_')[0]) if '_part' in x else 0
    )

    for file in transcript_files:
        with open(f'./1_transcript/{filename}/{file}', 'r', encoding='utf-8') as f:
            combined_transcript += f.read() + "\n\n"
    return combined_transcript

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
from env import gemini_key
client = genai.Client(api_key=gemini_key)

def gemini_model(prompt,content):
    response = client.models.generate_content(
        model="gemini-2.5-pro-preview-03-25", contents=prompt+'/'+content
    )
    return response.text