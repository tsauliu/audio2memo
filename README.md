# Audio to Memo Project

This project converts audio recordings into text transcripts and potentially generates memos.

## Setup

1.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Configure any necessary environment variables (refer to `env.py` if it exists).

## How to Run

To process an audio file, run the main script `run.py` and provide the path to the audio file as an argument:

```bash
python run.py <path_to_your_audio_file>
```

For example:
```bash
python run.py 0_raw_audio/meeting_notes.mp3
```

The output files (transcript, word-for-word text, memo, etc.) will be placed in the corresponding numbered directories (e.g., `1_transcript/`, `2_wordforword/`, `3_memo/`). 