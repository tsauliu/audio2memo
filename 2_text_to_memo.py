#%%
from openai import OpenAI
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

summarytext=summary(transcript)
print(summarytext)

with open("memo.txt", "w", encoding="utf-8") as f:
    f.write(summarytext)