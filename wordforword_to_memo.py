#%%
import datetime
from funcs import combine_transcripts,count_tokens,deepseek_model,gemini_model



def wordforword_to_memo(project,contextfile):
    combined_transcript=combine_transcripts(project)
    prompt=open('./prompt/prompt_highlevelsummary.md','r',encoding='utf-8').read()
    context=open(contextfile,'r',encoding='utf-8').read()
    
    print(prompt+context)
    print(f"Memo Total input tokens: {count_tokens(prompt)+count_tokens(combined_transcript)}")
    print(project)
    
    summarytext=gemini_model(prompt+context,combined_transcript)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"./3_memo/{project}_{timestamp}.txt"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(summarytext)

if __name__ == '__main__':
    project='pony 1q25'
    contextfile='context/auto.md'
    wordforword_to_memo(project,contextfile)