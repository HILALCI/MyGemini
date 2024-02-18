import os
from dotenv import dotenv_values
import google.generativeai as genai
from pathlib import Path
from tkinter import (
    Tk,
    messagebox,
    Label,
    Text,
    Entry,
    OptionMenu,
    Button,
    StringVar,
    GROOVE,
    END,
)


def get_apikey():
    try:
        api_key = dotenv_values(".env")["API_key"]

        if api_key == None or api_key == "":
            messagebox.showwarning("Uyarı", "API key bulunamadi.")

    except KeyError:
        messagebox.showwarning("Uyarı", ".env dosyasi bos veya API key eklenmemis.")
    except FileNotFoundError:
        messagebox.showwarning("Uyarı", ".env dosyasi bulunamadi.")

    return api_key


genai.configure(api_key=get_apikey())

# Set up the model
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_LOW_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-pro-vision",
    generation_config=generation_config,
    safety_settings=safety_settings,
)


def basla():
    resim = label_option.get().split("'")[1]

    image_parts = [
        {
            "mime_type": f"image/{resim.split('.')[-1]}",
            "data": Path(f"{resim}").read_bytes(),
        }
    ]

    prompt = ent1.get()

    if prompt == "clear" or prompt == "Clear" or prompt == "CLEAR":
        answer.delete("1.0", END)
        ent1.delete(0, "end")

    else:
        prompt_parts = [f"{prompt}", image_parts[0]]

        answer.delete("1.0", END)
        response = model.generate_content(prompt_parts)
        answer.insert(END, response.text)


main = Tk()
main.title("Gemini Vision")
main.geometry(f"{main.winfo_screenwidth() - 50}x{main.winfo_screenheight() - 50}")
main.resizable(True, True)
main.bind("<Escape>", lambda event: main.destroy())
main.bind("<Return>", lambda event: basla())


Label(main, text="Lütfen Prompt giriniz: ").place(x=40, y=20)

ent1 = Entry(main, width=120)
ent1.place(x=200, y=20)


def get_dosname():
    endwit = ["png", "jpeg", "webp", "heic", "heif"]
    gdosn = list()
    for dosya in os.listdir(path="."):
        if dosya.split(".")[1] in endwit:
            gdosn.append(dosya)

    if len(gdosn) == 0:
        messagebox.showwarning("Uyarı", "Istenilen formatta dosya bulunamadi.")

    return gdosn


label_option = StringVar(main)
label_open_menu = OptionMenu(main, label_option,*get_dosname()).place(
    x=main.winfo_screenwidth() - 190, y=20
)


Button(
    main,
    text="Cevapla",
    padx=5,
    pady=5,
    bd=5,
    activebackground="yellow",
    relief=GROOVE,
    command=basla,
).place(x=main.winfo_screenwidth() - 110, y=20)


Label(main, text="Cevap: ").place(x=50, y=60)
answer = Text(main, width=150, height=35)
answer.place(x=50, y=80)

main.mainloop()
