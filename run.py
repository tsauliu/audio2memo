#%%
from process_audio import split_audio
from funcs import feishu_bot
import os
import shutil

project='catl 4 21 发布会'
filetype='mp3'

#copyfile
dropbox_path=f'~/Dropbox/VoiceMemos/{project}.{filetype}'
dropbox_path=os.path.expanduser(dropbox_path)
raw_audio_path=f'./0_raw_audio/{project}.{filetype}'
os.makedirs(os.path.dirname('./0_raw_audio/'), exist_ok=True)
if os.path.exists(dropbox_path) and not os.path.exists(raw_audio_path):
    shutil.copyfile(dropbox_path, raw_audio_path)
    print(f'{project}.{filetype} copied to {raw_audio_path}')
    feishu_bot(f'{project}.{filetype} copied to {raw_audio_path}')
else:
    print(f'{project}.{filetype} already exists in {raw_audio_path}')
    feishu_bot(f'{project}.{filetype} already exists in {raw_audio_path}')
#%%
# process audio
input_file=f'./0_raw_audio/{project}.{filetype}'
output_dir=f'./0_processed_audio/{project}'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    max_size=25
    max_duration=1500
    split_audio(input_file, output_dir, max_size, max_duration)
    feishu_bot(f'split files for {project}.{filetype} processed')
# audio to text

from audio2text import process_audio_files
if not os.path.exists(f'./1_transcript/{project}'):
    process_audio_files(project)
    feishu_bot(f'transcript for {project}.{filetype} processed')
# text to wordforword
from text_to_wordforword import text_to_wordforword
os.makedirs('./2_wordforword/', exist_ok=True)
current_files=[f for f in os.listdir('./2_wordforword/') if f.startswith(project)]
if len(current_files)==0:
    text_to_wordforword(project)
    feishu_bot(f'wordforword for {project}.{filetype} processed')

# wordforword to memo
from wordforword_to_memo import wordforword_to_memo
os.makedirs('./3_memo/', exist_ok=True)
current_files=[f for f in os.listdir('./3_memo/') if f.startswith(project)]
if len(current_files)==0:
    wordforword_to_memo(project)
    feishu_bot(f'memo for {project}.{filetype} processed')

# combine to docx
from combine_to_docx import combine_to_docx
os.makedirs('./4_docx/', exist_ok=True)
current_files=[f for f in os.listdir('./4_docx/') if f.startswith(project)]
if len(current_files)==0:
    combine_to_docx(project)
    feishu_bot(f'docx for {project}.{filetype} processed')