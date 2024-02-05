import speech_recognition as sr
from gtts import gTTS
import transformers
import os
import time
import datetime
import numpy as np

class ChatBot():
    def __init__(self, name):
        print("----- Starting up", name, "-----")
        self.name = name

    def speech_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as mic:
            print("Listening...")
            audio = recognizer.listen(mic)
            self.text = "ERROR"
        try:
            self.text = recognizer.recognize_google(audio)
            print("Me  --> ", self.text)
        except:
            print("Me  -->  ERROR")

    @staticmethod
    def text_to_speech(text):
        print("Dev --> ", text)
        speaker = gTTS(text=text, lang="en", slow=False)
        speaker.save("res.mp3")
        statbuf = os.stat("res.mp3")
        mbytes = statbuf.st_size / 1024
        duration = mbytes / 200
        os.system('start res.mp3')
        time.sleep(int(50 * duration))
        os.remove("res.mp3")

    def wake_up(self, text):
        return True if self.name in text.lower() else False

    @staticmethod
    def action_time():
        return datetime.datetime.now().time().strftime('%H:%M')

if __name__ == "__main__":
    ai = ChatBot(name="dev")
    nlp = transformers.pipeline("conversational", model="microsoft/DialoGPT-medium")
    os.environ["TOKENIZERS_PARALLELISM"] = "true"
    ex = True
    while ex:
        ai.speech_to_text()
        if any(i in ai.text for i in ["hello", "hi"]):
            res = "Hello, I am Dave the AI. How can I assist you?"
        elif "passport" in ai.text:
            res = "Please scan your passport."
        elif "scanned it" in ai.text:
            res = "Please go to counter 5 to be processed by security."
        elif "ticket" in ai.text:
            res = "Please scan your ticket."
        elif "scanned it" in ai.text:
            res = "Put your luggage on the scale to be weighed."
        elif "done" in ai.text:
            res = "Your luggage ticket has been printed. Your flight is at gate 3."
        elif any(i in ai.text for i in ["gate 3", "Gate 3", "3"]):
            res = "Follow me."
        elif "hotel" in ai.text:
            res = "The nearest hotel to the airport is Clarion Hotel Jeddah Airport (4.4 stars, 6.3km away) and Areen Airport Hotel (4 stars, 6.8km away)."
        elif any(i in ai.text for i in ["thank", "thanks"]):
            res = np.random.choice(["You're welcome!", "Anytime!", "No problem!", "I'm here if you need me!", "Mention not."])
        elif any(i in ai.text for i in ["exit", "close", "bye"]):
            res = np.random.choice(["Have a safe flight", "Bye", "Goodbye", "Hope to meet soon"])
            ex = False
        else:
            if ai.text == "ERROR":
                res = "Sorry, come again?"
            else:
                chat = nlp([{"role": "system", "content": "user"}, {"role": "user", "content": ai.text}])
                res = chat[0]["message"]["content"]

        ai.text_to_speech(res)
    print("----- Closing down Dev -----")
