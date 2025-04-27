import os
from groq import Groq

GROQ_API_KEY = "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"

# Initialize the Groq client
client = Groq(
    api_key =  GROQ_API_KEY
)

# Specify the path to the audio file
filename = os.path.dirname(__file__) + "/Homo Deus A Brief History of Tomorrow - 08 (mp3cut.net).mp3" # Replace with your audio file!

# Open the audio file
# with open(filename, "rb") as file:
#     # Create a transcription of the audio file
#     transcription = client.audio.transcriptions.create(
#       file=(filename, file.read()), # Required audio file
#       model="whisper-large-v3-turbo", # Required model to use for transcription
#       prompt="Specify context or spelling",  # Optional
#       response_format="json",  # Optional
#       language="en",  # Optional
#       temperature=0.0  # Optional
#     )
#     # Print the transcription text
#     print(transcription.text)


# # Open the audio file
with open(filename, "rb") as file:
    # Create a translation of the audio file
    translation = client.audio.translations.create(
      file=(filename, file.read()), # Required audio file
      model="whisper-large-v3", # Required model to use for translation
      prompt="Specify context or spelling",  # Optional
      response_format="json",  # Optional
      temperature=0.0  # Optional
    )
    # Print the translation text
    print(translation.text)