from dotenv import dotenv_values
import google.generativeai as genai
import gradio as gr


def get_apikey():
    try:
        api_key = dotenv_values(".env")["API_key"]

        if api_key == None or api_key == "":
            print("API key bulunamadi.")

    except KeyError:
        print(".env dosyasi bos veya API key eklenmemis.")
    except FileNotFoundError:
        print(".env dosyasi bulunamadi.")

    return api_key


genai.configure(api_key=get_apikey())

# Set up the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_LOW_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings,
)


def answerme(message, history):
    response = model.generate_content(message)
    return response.text


chat = gr.ChatInterface(
    fn=answerme, examples=["Google", "Bard", "Gemini"], title="Gemini ChatBot"
)
chat.launch()
