#%%
from openai import OpenAI
from env import keysecret
import os
import datetime
client = OpenAI(
    api_key=keysecret
)

def audio2text(filename, project, client):
    audio_filepath = os.path.join("./0_processed_audio", project, filename)
    transcript_dir = os.path.join("./1_transcript", project)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    transcript_filepath = os.path.join(transcript_dir, f"{filename}_{timestamp}.txt")

    try:
        with open(audio_filepath, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="gpt-4o-transcribe", #gpt-4o-mini-transcribe / gpt-4o-transcribe
                file=audio_file
            )
        
        with open(transcript_filepath, "w", encoding="utf-8") as f:
            f.write(transcript.text)
        print(f"Processed: {filename}")
    except FileNotFoundError:
        print(f"Error: Audio file not found at {audio_filepath}")
    except Exception as e:
        print(f"An error occurred while processing {filename}: {e}")


def process_audio_files(project):
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
        audio2text(filename, project, client) # Pass client if needed

    timeend = datetime.datetime.now()
    print(f'End time: {timeend}')
    print(f'Total time: {timeend - timestart}')

# Example usage:
if __name__ == "__main__":
    project_name = 'hype 交接2' 
    process_audio_files(project_name)