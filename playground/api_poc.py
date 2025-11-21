import os
from google import genai

if "GOOGLE_API_KEY" not in os.environ:
    print("Run a new bash instance, or source the .bashrc!")

client = genai.Client()

response = client.models.generate_content(model="gemini-2.5-flash", contents="Explain ai to an israeli grandma")

print(response.text)
