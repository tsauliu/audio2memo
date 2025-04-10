#%%
import requests
import os
import json
from env import adminkey
def get_audio_transcription_usage(start_time=1730419200, limit=1):
    return requests.get(f"https://api.openai.com/v1/organization/usage/audio_transcriptions", headers={"Authorization": f"Bearer {adminkey}", "Content-Type": "application/json"}, params={"start_time": start_time, "limit": limit}).json()

# print(get_audio_transcription_usage())


# curl "https://api.openai.com/v1/organization/costs?start_time=1730419200&limit=1" \
# -H "Authorization: Bearer $OPENAI_ADMIN_KEY" \
# -H "Content-Type: application/json"
# Generate timestamp for January 1, 2024 (00:00:00 UTC)
import datetime
jan_1_2024_timestamp = int(datetime.datetime(2024, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc).timestamp())



requests.get(f"https://api.openai.com/v1/organization/costs?start_time={jan_1_2024_timestamp}&limit=180", headers={"Authorization": f"Bearer {adminkey}", "Content-Type": "application/json"}).json()
# %%
