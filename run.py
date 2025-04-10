from process_audio import split_audio
import os

project='科辉智药-刘博士'

# process audio
input_file=f'./0_raw_audio/{project}.m4a'
output_dir=f'./0_processed_audio/{project}'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    max_size=25
    max_duration=1500
    split_audio(input_file, output_dir, max_size, max_duration)

# audio to text
from audio2text import process_audio_files
if not os.path.exists(f'./1_transcript/{project}'):
    process_audio_files(project)

# text to wordforword
from text_to_wordforword import text_to_wordforword
current_files=[f for f in os.listdir('./2_wordforword/') if f.startswith(project)]
if len(current_files)==0:
    text_to_wordforword(project)

# wordforword to memo
from wordforword_to_memo import wordforword_to_memo
current_files=[f for f in os.listdir('./3_memo/') if f.startswith(project)]
if len(current_files)==0:
    wordforword_to_memo(project)

# combine to docx
from combine_to_docx import combine_to_docx
current_files=[f for f in os.listdir('./4_docx/') if f.startswith(project)]
if len(current_files)==0:
    combine_to_docx(project)