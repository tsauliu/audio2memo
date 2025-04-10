from process_audio import split_audio
import os

project='grab交接.m4a'

# process audio
input_file=f'./0_raw_audio/{project}.m4a'
output_dir=f'./0_processed_audio/{project}'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
max_size=25
max_duration=1500
split_audio(input_file, output_dir, max_size, max_duration)

