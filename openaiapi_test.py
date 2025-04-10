#%%
from openai import OpenAI
from env import keysecret

client = OpenAI(
    api_key=keysecret
)

response = client.responses.create(
    model="gpt-4o",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)
