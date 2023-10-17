#---------------------------------------Main IPA Folder---------------------------------------#
#-----------------------------------Iris Personal Assistant-----------------------------------#
#-------------------------------------------V 1.0.1-------------------------------------------#

import kivy                                                         #to create Personal Assistant GUI
from kivy.app import App
from kivy.config import Config
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle


import speech_recognition as sr                                     #to capture the user voice
import pyaudio                                                      #to use computer microphone
import playsound                                                    #to play created MP3 audio directly from folder
import pyttsx3                                                      #Text-to-Speech library to convert responses to speech (works offline)
from time import ctime, strftime                                    #to get date and time data
import time                                                         #to continuously listen
import webbrowser                                                   #to open web browsers
import os                                                           #to manage operating system interfaces (remove generated audio file)
import random                                                       #to randomize responds by Iris
from multiprocessing import Process                                 #to simultaneously record audio at all time

from keyword_lists import *                                         #importing another python file from folder to use keywords for user requests

#calculate how old is Iris
iris_age = int(time.strftime("%j")) - 301 if time.strftime("%Y") == "2020" else 65 + int(time.strftime("%j"))

#get app directories
directory_main = os.path.dirname(os.path.abspath(__file__))
directory_local = directory_main[0:-4]
directory_resources = directory_local+"resources/"


#---------------------------------------Main IPA Engine---------------------------------------#

#user speech capture
r = sr.Recognizer()
mic = sr.Microphone(sample_rate=20000)
    
#text to speech engine initialization
tts = pyttsx3.init()
tts.setProperty("rate", 250)
tts.setProperty("voice", [1])   

#record user speech
def record_audio(ask = False):
    voice_data = ""
    if ask:
        speak(ask)
    with mic as source:
        audio = r.listen(source, timeout=None, phrase_time_limit=None, snowboy_configuration=None)
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            speak("Sorry I can't understand what you are saying.")
        except sr.RequestError as e:
            speak("Sorry there had been an error: {}".format(e))
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




    """
    elif voice_data in exit_assistant:
        speak("Goodbye, {}".format(write_read()))
        MainLayout.listen(, "outside_exit", "normal")
        exit()
    """

#convert response to audio for user
def speak(text):
    print(text)
    tts.say(text)
    tts.runAndWait()

#greet the user
greeting = random.choice(seq = ["How can I help you?", "Hey, how can I help you?", "Can I help you?", "What can I help you with?", "Hello, do you have any requests?"])

#create loop for listening
def listen_loop():
    while True:
        voice_data = record_audio()
        respond(voice_data)
        print(voice_data)

#initiate Iris
def initiate_iris():
    speak(greeting)
    global main_process
    main_process = Process(target=listen_loop)
    main_process.start()

#turn off Iris
def disable_iris():
    speak("Goodbye, {}".format(write_read()))
    main_process.terminate()

#define path to save user data
user_data_path = os.path.join(directory_local, "user_data.txt")

#save user infromation into user_data.txt
def write_read(text = ""):
    if text != "":
        with open(user_data_path, "w+") as file:
            file.write("-------------------")
            file.write("\n#username:")
            file.write("\n\n"+text)
    
    with open(user_data_path, "r") as file:
        line = file.readlines()
    
    try:
        return line[3]
    except:
        return ""


#-------------------------------------------IPA GUI-------------------------------------------#

#background adjuster
class LabelBackground(Label):
    def on_pos(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.13, 0.498, 0.58, 0.6)
            Rectangle(pos=self.pos, size=self.size)


#main app layout class
class MainLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)

        #add background image
        self.background_image = Image(source=directory_resources+"background1.png", size_hint=(1,1))
        self.add_widget(self.background_image)

        #add button to listen
        self.listen_button = ToggleButton(background_normal=directory_resources+"listen_button1.png", 
                                          background_down=directory_resources+"listen_button2.png",
                                          #border = (30,30,30,30),
                                          size_hint=(0.0625, 0.0833),
                                          pos_hint={"center_x":0.5, "center_y":0.25})
        self.add_widget(self.listen_button)
        self.listen_button.bind(state=self.listen)
             
        #add animation after pressing button
        self.button_animation = Image(source=directory_resources+"button_animation1.gif",                                     
                                      size_hint=(0.125, 0.166),
                                      pos_hint={"center_x":0.5, "center_y":0.25})
        self.add_widget(self.button_animation)
        self.button_animation.anim_delay = -1

        #add animation for listening
        self.listen_animation = Image(source=directory_resources+"voice_recognition2.gif",
                                      size_hint=(0.2, 0.2),
                                      pos_hint={"center_x":0.82, "center_y":0.94})
        self.add_widget(self.listen_animation)
        self.listen_animation.anim_delay = -1
    
        #add icon image
        self.image_icon = Image(source=directory_resources+"image_logo1.png",
                                      size_hint=(0.1, 0.1),
                                      pos_hint={"center_x":0.96, "center_y":0.94})
        self.add_widget(self.image_icon)

        #name of user (label + text input)
        self.text_label = LabelBackground(text="[b]Username (confirm with enter):[/b]", markup = True, font_size = 11.5,
                                          size_hint=(0.2,0.05),
                                          pos_hint={"center_x":0.88, "center_y":0.85},
                                          color=(0,0,0,1))

        self.add_widget(self.text_label)


        self.text_input = TextInput(text=write_read(), multiline=False,
                                    size_hint=(0.2,0.05),
                                    pos_hint={"center_x":0.88, "center_y":0.78},
                                    background_color=(0.13,0.498,0.58,0.6))
        self.add_widget(self.text_input)
        self.text_input.bind(on_text_validate=lambda x:write_read(self.text_input.text))

    

    #define method for button press
    def listen(self, instance, state):      #instance here represents object to which this function was passed (bound)
        if state == "normal":
            print("Button isn't pressed")
            self.button_animation.anim_loop = 1
            self.listen_animation.anim_loop = 1

            disable_iris()


        if state == "down":
            print("Button is pressed")
            self.button_animation._coreimage.anim_reset(True)
            self.button_animation.anim_loop = 0
            self.button_animation.anim_delay = 0.14
            self.listen_animation._coreimage.anim_reset(True)
            self.listen_animation.anim_loop = 0
            self.listen_animation.anim_delay = 0.14

            initiate_iris()
    
    
#main window
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

    





