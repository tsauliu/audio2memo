#%%
import datetime
from funcs import combine_transcripts,count_tokens,deepseek_model,gemini_model

prompt=open('./prompt/prompt_word2memo.md','r',encoding='utf-8').read()

filename='hype 交接1'
combined_transcript=combine_transcripts(filename)

print(f"Total input tokens: {count_tokens(prompt)+count_tokens(combined_transcript)}")

summarytext=gemini_model(prompt,combined_transcript)
print(summarytext)

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f"./3_memo/{filename}_{timestamp}.txt"

with open(output_file, "w", encoding="utf-8") as f:
    f.write(summarytext)