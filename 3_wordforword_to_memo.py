#%%
from openai import OpenAI
from env import api_key_deepseek,model_id_deepseek
import datetime
from funcs import combine_transcripts,count_tokens

client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3/bots",
    api_key=api_key_deepseek
)

prompt=open('./prompt/prompt_word2memo.md','r',encoding='utf-8').read()

def summary(content):
    completion = client.chat.completions.create(
        model=model_id_deepseek,
        messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": content},
    ],
    )
    return completion.choices[0].message.content

filename='hype 交接1'
combined_transcript=combine_transcripts(filename)

print(f"Total input tokens: {count_tokens(prompt)+count_tokens(combined_transcript)}")

summarytext=summary(combined_transcript)
print(summarytext)

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f"./3_memo/{filename}_{timestamp}.txt"

with open(output_file, "w", encoding="utf-8") as f:
    f.write(summarytext)