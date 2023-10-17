#---------------------------------------Main IPA Folder---------------------------------------#
#-----------------------------------Iris Personal Assistant-----------------------------------#

import kivy                             #to create Personal Assistant GUI
from kivy.app import App
from kivy.config import Config
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout

import time
import os

"""
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
"""

#calculate how old is Iris
iris_age = int(time.strftime("%j")) - 301 if time.strftime("%Y") == "2020" else 65 + int(time.strftime("%j"))


#get app directories
directory_main = os.path.dirname(os.path.abspath(__file__))
directory_local = directory_main[0:-4]
directory_resources = directory_local+"resources/"


#-------------------------------------------IPA GUI-------------------------------------------#

class MainLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)

        self.background_image = Image(source=directory_resources+"background1.png", allow_stretch=True, keep_ratio=False , size_hint=(1,1))
        self.add_widget(self.background_image)

        #self.my_label = Label(text="Label", pos=(200,200), size_hint=(0.3,0.3))
        #self.add_widget(self.my_label)

        #add button to listen
        self.listen_button = Button(background_normal=directory_resources+"listen_button1.png", 
                                    background_down=directory_resources+"listen_button1.png",
                                    #border = (30,30,30,30),
                                    size_hint=(0.0625, 0.0833),
                                    pos_hint={"center_x":0.5, "center_y":0.25})
        self.add_widget(self.listen_button)
        self.listen_button.bind(on_press=self.listen)
        
        
        #add animation after pressing button
        self.button_animation = Image(source=directory_resources+"button_animation1.gif", 
                                      allow_stretch=True,
                                      keep_ratio=False,
                                      size_hint=(0.125, 0.166),
                                      pos_hint={"center_x":0.5, "center_y":0.25})
        self.add_widget(self.button_animation)
        self.button_animation.anim_delay = -1
        self.button_animation.anim_loop = 2

        #add animation for listening
        self.listen_animation = Image(source=directory_resources+"voice_recognition2.gif",
                                      allow_stretch=True,
                                      keep_ratio=False,
                                      size_hint=(0.5, 0.5),
                                      pos_hint={"center_x":0.5, "center_y":0.4})
        self.add_widget(self.listen_animation)
        self.listen_animation.anim_delay = -1
        self.listen_animation.anim_loop = 1
    
        #add icon image
        self.image_icon = Image(source=directory_resources+"image_logo1.png",
                                      allow_stretch=True,
                                      keep_ratio=False,
                                      size_hint=(0.1, 0.1),
                                      pos_hint={"center_x":0.96, "center_y":0.94})
        self.add_widget(self.image_icon)



    #define method for button press
    def listen(self, instance):
        self.button_animation.anim_delay = 0.14
        self.button_animation._coreimage.anim_reset(True)

        self.listen_animation.anim_delay = 0.14
        self.listen_animation._coreimage.anim_reset(True)

        print("Hurá")
    

#create main window
class Window(App):
    def build(self):

        #setting up window size
        Config.set("graphics", "width", 800)
        Config.set("graphics", "height", 600)
        Config.set("graphics", "resizable", False)
        Config.write()

        self.title = "Iris Personal Assistant"
        self.icon = directory_resources + "listen_button1.png"
        return MainLayout()





if __name__ == "__main__":
    Window().run()


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

"""