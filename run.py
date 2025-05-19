#%%
from process_audio import split_audio
from funcs import feishu_bot
import os
import shutil

base_path=f'~/audio2memo/'
base_path=os.path.expanduser(base_path)

allfiles=os.listdir(os.path.expanduser(f'~/Dropbox/VoiceMemos/'))
# 按照修改时间排序文件，过滤掉.docx文件
allfiles = [f for f in allfiles if not f.endswith('.docx')]
allfiles.sort(key=lambda f: os.path.getmtime(os.path.join(os.path.expanduser('~/Dropbox/VoiceMemos/'), f)), reverse=True)
for i in range(len(allfiles)):
    print(f'{i+1}. {allfiles[i]}')

input_filename = input("Enter the number (e.g., '1'): ")

if input_filename=='':
    input_filename=1

filename=allfiles[int(input_filename)-1]
print(f'processing {filename}')
project = filename.rsplit('.', 1)[0]
filetype = filename.rsplit('.', 1)[1]

# Input context
input_context = input("Enter context (press Enter to skip): ")
context_dir = f'{base_path}/context/'
os.makedirs(context_dir, exist_ok=True)
context_file = f'{context_dir}/{project}.md'

with open(context_file, 'w', encoding='utf-8') as f:
    f.write(f'## 上下文信息：录音中出现的名称（人名、地名、组织名）、地点、时间、事件等\n\n')
    f.write(input_context)

feishu_bot(f'Context markdown for {project} generated at {context_file}')

#%%



# input_refresh=input('refresh? (y/n): ')
# if input_refresh=='y':
#     input_refresh=True
# else:
#     input_refresh=False

input_refresh=True
input_model_num=input('model? (1.GPT-4o-transcribe (default), 2.GPT-4o-mini-transcribe, 3.Whisper-1): ')

if input_model_num=='':
    input_model_num=1
else:
    input_model_num=int(input_model_num)

if input_model_num==1:
    input_model='gpt-4o-transcribe'
elif input_model_num==2:
    input_model='gpt-4o-mini-transcribe'
elif input_model_num==3:
    input_model='whisper-1'
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
    # feishu_bot(f'split files for {project}.{filetype} processed')
# audio to text

from audio2text import process_audio_files
if input_refresh and os.path.exists(f'{base_path}/1_transcript/{project}'):
    shutil.rmtree(f'{base_path}/1_transcript/{project}')
    # feishu_bot(f'transcript for {project}.{filetype} removed')

if not os.path.exists(f'{base_path}/1_transcript/{project}'):
    process_audio_files(project, input_model)
    # feishu_bot(f'transcript for {project}.{filetype} processed')

# text to wordforword
from text_to_wordforword import text_to_wordforword
os.makedirs('./2_wordforword/', exist_ok=True)
current_files=[f for f in os.listdir('./2_wordforword/') if f.startswith(project)]
if not len(current_files)==0 or input_refresh:
    text_to_wordforword(project)
    # feishu_bot(f'wordforword for {project}.{filetype} processed')

# wordforword to memo
from wordforword_to_memo import wordforword_to_memo
os.makedirs(f'{base_path}/3_memo/', exist_ok=True)
current_files=[f for f in os.listdir(f'{base_path}/3_memo/') if f.startswith(project)]

if len(current_files)==0 or input_refresh:
    wordforword_to_memo(project)
    # feishu_bot(f'memo for {project}.{filetype} processed')

# combine to docx
from combine_to_docx import combine_to_docx
os.makedirs(f'{base_path}/4_docx/', exist_ok=True)
current_files=[f for f in os.listdir(f'{base_path}/4_docx/') if f.startswith(project)]
if len(current_files)==0 or input_refresh:
    combine_to_docx(project)
    feishu_bot(f'docx for {project}.{filetype} processed')