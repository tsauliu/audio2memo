#%%
from openai import OpenAI
import tiktoken
from env import api_key_deepseek,model_id_deepseek

client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3/bots",
    api_key=api_key_deepseek
)

prompt=open('prompt_auto2memo.md','r',encoding='utf-8').read()

def summary(content):
    completion = client.chat.completions.create(
        model=model_id_deepseek,
        messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": content},
    ],
    )
    return completion.choices[0].message.content

transcript=open('transcript.txt','r',encoding='utf-8').read()

# Calculate token count
encoding = tiktoken.get_encoding("cl100k_base")
prompt_tokens = encoding.encode(prompt)
transcript_tokens = encoding.encode(transcript)
total_tokens = len(prompt_tokens) + len(transcript_tokens)
print(f"Total input tokens: {total_tokens}")

summarytext=summary(transcript)
print(summarytext)

with open("memo.txt", "w", encoding="utf-8") as f:
    f.write(summarytext)