import os
from dotenv import dotenv_values
import google.generativeai as genai
from pathlib import Path

api_key = dotenv_values(".env")["API_key"]

genai.configure(api_key=api_key)

# Set up the model
generation_config = {
  "temperature": 0.4,
  "top_p": 1,
  "top_k": 32,
  "max_output_tokens": 4096,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_LOW_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_LOW_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_LOW_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_LOW_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-pro-vision",
                              generation_config=generation_config,
                              safety_settings=safety_settings)


resim = input("Lutfen resim dosyalarinin ismini giriniz(Ornek resim.png): ")

# Validate that an image is present
if not (img := Path(f"{resim}")).exists():
  raise FileNotFoundError(f"Could not find image: {img}")

image_parts = [
  {
    "mime_type": f"image/{resim.split('.')[-1]}",
    "data": Path(f"{resim}").read_bytes()
  }
]

prompt = input("Lutfen Prompt giriniz : ")

prompt_parts = [
  f"{prompt}",
  image_parts[0]
]

response = model.generate_content(prompt_parts)
print(response.text)