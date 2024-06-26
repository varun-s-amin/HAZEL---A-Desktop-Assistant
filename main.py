import pyttsx3
import speech_recognition as sr
import pyaudio
import keyboard
import os
import subprocess as sp
import online
from decouple import config
from datetime import datetime
from convo import random_text
from random import choice
import imdb

engine = pyttsx3.init('sapi5')
engine.setProperty('volume', 1.5)
engine.setProperty('rate', 174)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

USER = config('USER')
HOSTNAME = config('BOT')


def speak(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing....")
        query = r.recognize_google(audio,language='en-in')
        print(query)
        if not 'stop' in query or 'exit' in query:
            speak(choice(random_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                speak(f"Good night {USER}, See you seen!")
            else:
                speak('Have a Great Day!!')
                exit()
    except Exception:
            speak("Sorry, I could not understand. Can you please repeat again?")
            query = 'None'
    return query


def greet_me():
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good morning {USER}")
    elif (hour >= 12) and (hour < 16):
        speak(f"Good afternoon {USER}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Good evening {USER}")
    speak(f"I am {HOSTNAME}. How can i help you today?")

listening = False

def start_listening():
    global listening
    listening = True
    print("started listening")

def pause_listening():
    global listening
    listening = False
    print("stop listening")

keyboard.add_hotkey('ctrl+alt+k',start_listening)
keyboard.add_hotkey('ctrl+alt+p',pause_listening)

if __name__ == '__main__':
    greet_me()
    while True:
        if listening:
            query = takeCommand().lower()
            if "how are you" in query:
                speak("I am absolutely fine. What about you")
            elif "open command prompt" in query:
                speak("Opening command prompt")
                os.system('start cmd')
            elif "open camera" in query:
                speak("opening camera")
                sp.run('start microsoft.windows.camera:', shell=True)

            elif "ip address" in query:
                ip_address = online.find_my_ip()
                speak(f"your ip address is {ip_address}")
                print(f"your ip address is {ip_address}")

            elif "youtube" in query:
                speak(f"what do you want me to play")
                video = takeCommand().lower()
                online.youtube(video)


            elif 'search' in query or 'google search' in query:

                Qquery = query.replace("search", "")

                Query = query.replace("google search", "")

                from online import googlesearch

                if "search" in query:

                    googlesearch(Qquery)

                else:

                    googlesearch(Query)

#error in this function

            elif "send an email" in query:
                speak("on what email address do you want me to send?. Please enter proper email address in terminal")
                receiver_add = input("Email address:")
                speak("what should be the subject sir?")
                subject = takeCommand().capitalize()
                speak("what is the message?")
                message = takeCommand().capitalize()
                if online.send_email(receiver_add,subject,message):
                    speak("the email has been sent")
                else:
                    speak("something went wrong please check the error log")

            elif 'time' in query:
                current_time = datetime.now().strftime('%H:%M')
                speak(f"The time is {current_time}.")

#error
            elif 'alarm' in query:
                from online import alarm
                speak("enter the time")
                alarm_time = input("Enter the alarm time (HH:MM format): ")
                alarm(alarm_time)

            elif 'my location' in query:
                from online import my_location

                my_location()


            elif 'where is' in query:
                place = query.replace("where is", "")
                from online import map

                map(place)

            elif 'write a note' in query or 'make a note' in query:
                from online import notepad

                notepad()

            elif 'close the note' in query:
                from online import close_note

                close_note()

            elif 'tell me a joke' in query:
                from online import jokes

                jokes()



            elif 'weather in' in query or 'temperature in' in query:
                from online import get_weather
                from online import speakWeather

                city_name = query.replace("weather in ", "").replace("temperature in ", "")
                weather_info = get_weather(city_name)
                speakWeather(weather_info, city_name)

#no function
            elif 'news' in query:
                from online import news
                news()


            elif 'launch' in query:
                app_name = query.replace('launch', '').strip()
                from online import launch_application

                launch_application(app_name)


            elif 'screenshot' in query:
                from online import take_screenshot

                take_screenshot()
                speak("Screenshot taken and saved.")

            elif 'song please' in query or 'play some songs' in query:
                speak("Which song do you want me to play")
                song = takeCommand()
                from online import playsong

                playsong(song)
                exit()


            elif "shutdown the system" in query:
                speak("Are You sure you want to shutdown")
                shutdown = input("Do you wish to shutdown your computer? (yes/no)")
                if shutdown == "yes":
                    os.system("shutdown /s /t 1")

                elif shutdown == "no":
                    exit()

            elif "movie" in query:
                movies_db = imdb.IMDb()
                speak("tell me the movie name")
                text =takeCommand()
                movies = movies_db.search_movie(text)
                speak(f"searching for the {text}")
                speak("i found these")
                for movie in movies:
                    title = movie["title"]
                    year = movie["year"]
                    speak(f"{title},{year}")
                    info = movie.getID()
                    movie_info = movies_db.get_movie(info)
                    ratings =movie_info["rating"]
                    cast = movie_info["cast"]
                    actor = cast[0:5]
                    plot = movie_info.get('plot outline','plot summary not available')
                    speak(f"{title} was released in {year} has an IMDB ratings of {ratings}. Consisting a cast of {actor}, The plot summary of the movie is {plot}")


            else:
                print("none")