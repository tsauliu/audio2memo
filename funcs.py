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