#%%
import datetime
from funcs import combine_transcripts,count_tokens,deepseek_model,gemini_model
import os

def text_to_wordforword(project):
    combined_transcript=combine_transcripts(project)
    transcript_length=len(combined_transcript)
    wordcountmin=round(transcript_length/1.5/1000)*1000
    wordcountmax=round(transcript_length/1000)*1000
    prompt=open('prompt/prompt_audio2word.md','r',encoding='utf-8').read()
    prompt=prompt.replace('{wordcountmin}',str(wordcountmin)).replace('{wordcountmax}',str(wordcountmax))
    print(f"Wordforword Total input tokens: {count_tokens(prompt)+transcript_length}")
    # summarytext=deepseek_model(prompt,combined_transcript)
    summarytext=gemini_model(prompt,combined_transcript)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"./2_wordforword/{project}_{timestamp}.txt"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(summarytext)

if __name__ == '__main__':
    project='grab交接'
    text_to_wordforword(project)
