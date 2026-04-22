import requests
import speech_recognition as sr
import pyttsx3

SERVER_URL = "https://your-render-url.onrender.com"

engine = pyttsx3.init()

def talk(text):
    print("AI:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            return r.recognize_google(audio).lower()
        except:
            return ""

def ask_cloud(cmd):
    try:
        url = f"{SERVER_URL}/command?cmd={cmd}"
        res = requests.get(url)
        return res.text
    except:
        return "Server error"

while True:
    cmd = listen()

    if cmd:
        print("You:", cmd)

        if "exit" in cmd:
            break

        response = ask_cloud(cmd)
        talk(response)