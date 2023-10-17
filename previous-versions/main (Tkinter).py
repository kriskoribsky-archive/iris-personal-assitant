#---------------------------------------Main IPA Folder---------------------------------------#
#-----------------------------------Iris Personal Assistant-----------------------------------#

import tkinter as tk                    #to create Personal Assistant GUI
import os


import speech_recognition as sr         #to recognize user voice
import pyaudio                          #to use computer microphone
import playsound                        #to play created MP3 audio directly from folder
from gtts import gTTS                   #Google Text-to-Speech API to convert responses to speech 
from time import ctime, strftime        #to get date and time data
import time                             #to continuously listen
import webbrowser                       #to open web browsers
import os                               #to manage operating system interfaces (remove generated audio file)
import random                           #to randomize responds by Iris

from keyword_lists import *             #importing another python file from folder to use keywords for user requests

#calculate how old is Iris
iris_age = int(time.strftime("%j")) - 301 if time.strftime("%Y") == "2020" else 65 + int(time.strftime("%j"))
"""

#get app directory
directory_main = os.path.dirname(os.path.abspath(__file__))
directory_local = directory_main[0:-4]


#-------------------------------------------IPA GUI-------------------------------------------#

#create main window
WIDTH = 800
HEIGHT = 600

main_window = tk.Tk(screenName="Iris Personal Assistant", baseName="Iris Personal Assistant")
main_window.title("Iris Personal Assistant")
main_window.resizable(height = False, width = False)


#create main frame (800x600)
main_frame = tk.Frame(main_window, width=WIDTH, height=HEIGHT, bg="black", bd=0)
main_frame.pack()

#add background image (label with main_frame parent)
main_label_image = tk.PhotoImage(file=directory_local+"resources/background1.png")
main_label = tk.Label(main_frame, image=main_label_image)
main_label.place(relx=-0.001, relwidth=1, relheight=1)

#setting up listen button
listen_button_image = tk.PhotoImage(file=directory_local+"resources/listen_button1.png")
listen_button = tk.Button(main_frame, bg ="#0d1114", activebackground="#0d1114", command=lambda: print("Hurá"), bd=0, image=listen_button_image)
listen_button.place(relx=0.5, rely=0.75, relwidth=0.066, relheight=0.089, anchor="c")

#add listen button animation after pressing the button
photo = tk.PhotoImage(file=directory_local+"resources/button_animation1.gif", format="gif -index 1")
listen_animation = tk.Label(main_label, image=photo)
listen_animation.place(relx=0.5, rely=0.75, width=100, height=100, anchor="c")

main_window.mainloop()
"""

#---------------------------------------Main IPA Engine---------------------------------------#


#user speech regonition
r = sr.Recognizer()

def record_audio(ask = False):
    if ask:
        speak(ask)
    with sr.Microphone(sample_rate=20000) as source:
        voice_data = ""
        audio = r.listen(source, timeout=None, phrase_time_limit=None, snowboy_configuration=None)
        try:
            voice_data = r.recognize_google(audio)#, language="en-US")
        except sr.UnknownValueError:
            speak("Sorry I can't understand what you are saying.")
        except sr.RequestError:
            speak("Sorry, speech recognition operation failed. API key isn't valid or your internet connection may be down.")
        return voice_data

#respond to user requests
def respond(voice_data):
    if voice_data in user_name:
        speak("Your name is NotRareOne.")  #work in progress
    elif voice_data in user_age:           #work in progress
        speak("You are 17 years old.")
    elif voice_data in speech_assistant_name:
        speak("My name is Iris. But my whole name is IPA which stands for Iris Personal Assistant.")
    elif voice_data in speech_assistant_age:
        speak("I am " + str(iris_age) + " days old. I was created on Tuesday, October 27th 2020.")
    elif voice_data in tell_time:
        speak(strftime("%H:%M:%S"))
    elif voice_data in tell_date:
        speak(ctime())
    elif voice_data in find_location:
        location = record_audio("What location do you want to search for.")
        url = "https://google.nl/maps/place/" + location + "/&amp;"
        webbrowser.open_new_tab(url = url)
        speak("Here is the location of " + location + ".")
    elif voice_data in search_google:
        search = record_audio("What do you want to search for.")
        url = "https://google.com/search?q=" + search
        webbrowser.open_new_tab(url = url)
        speak("Here is what I found for " + search + ".")
    


    elif voice_data in exit_assistant:
        speak("Goodbye, NotRareOne")
        exit()

#convert response to audio for user
def speak(text):
    print(text)
    tts = gTTS(text, lang = "en")
    tts.save("audio_speak.mp3")
    playsound.playsound("audio_speak.mp3")
    os.remove("audio_speak.mp3")

#greet the user
greeting = random.choice(seq = ["How can I help you?", "Hey, how can I help you?", "Can I help you?", "What can I help you with?", "Hello, do you have any requests?"])
speak(greeting)

#loop the program to continously listen
time.sleep(1)
while 1:
    voice_data = record_audio()
    respond(voice_data)
    

