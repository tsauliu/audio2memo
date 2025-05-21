#%%
from funcs import openai_transcribe,groq_transcribe
import os
import datetime

def audio2text(filename, project,input_model):
    audio_filepath = os.path.join("./0_processed_audio", project, filename)
    transcript_dir = os.path.join("./1_transcript", project)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    transcript_filepath = os.path.join(transcript_dir, f"{filename}_{timestamp}.txt")
    print(f"Processing: {filename}")
    try:
        if 'whisper-large-v3' in input_model:
            groq_transcribe(audio_filepath,transcript_filepath,input_model)
        else:
            openai_transcribe(audio_filepath,transcript_filepath,input_model)
        print(f"Processed: {filename}")
    except FileNotFoundError:
        print(f"Error: Audio file not found at {audio_filepath}")
    except Exception as e:
        print(f"An error occurred while processing {filename}: {e}")


def process_audio_files(project, input_model):
    """
    Processes all .m4a audio files in the specified project's processed_audio folder,
    transcribes them using OpenAI API, and saves the transcriptions.
    """
    timestart = datetime.datetime.now()
    print(f'Start time: {timestart}')

    transcript_dir = os.path.join("./1_transcript", project)
    if not os.path.exists(transcript_dir):
        os.makedirs(transcript_dir)
        print(f"Created directory: {transcript_dir}")

    audio_folder = os.path.join("./0_processed_audio", project)
    if not os.path.isdir(audio_folder):
        print(f"Error: Audio folder not found at {audio_folder}")
        return

    audio_files = [filename for filename in os.listdir(audio_folder)]

    if not audio_files:
        print(f"No .m4a files found in {audio_folder}")
        return
        
    print(f"Found {len(audio_files)} audio files to process.")

    # Process files sequentially
    for filename in audio_files:
        audio2text(filename, project,input_model) # Pass client if needed

    timeend = datetime.datetime.now()
    print(f'End time: {timeend}')
    print(f'Total time: {timeend - timestart}')

# Example usage:
if __name__ == "__main__":
    project_name = 'weride 1q25'
    input_model='whisper-large-v3'
    process_audio_files(project_name, input_model)