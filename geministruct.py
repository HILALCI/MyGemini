
import os
from dotenv import dotenv_values
import google.generativeai as genai

api_key = dotenv_values(".env")["API_key"]

genai.configure(api_key=api_key)

generation_config = {
  "temperature": 0.5,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
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

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)


girdi = input("Lutfen Prompt giriniz : ")
cikti = input("Lutfen Ciktinin nasil olmasi gerektigini giriniz : ")
aciklama = input("Lutfen ek aciklama giriniz (opsiyonel): ")

prompt_parts = [
    f"{aciklama}", 
    f"input: {girdi}",
    f"output: {cikti}"
]

response = model.generate_content(prompt_parts)
print(response.text)