import requests
import wikipedia
from pywikihow import search_wikihow
import pyttsx3
import json
import pywhatkit as kit
import pyjokes
from email.message import EmailMessage
import smtplib
from decouple import config
import datetime
import os
import pyjokes
from bs4 import BeautifulSoup
import pyttsx3
import pywhatkit
import wikipedia
import json
import webbrowser as web
import time
import pygame
import main
import requests
from geopy.geocoders import Nominatim
from keyboard import press_and_release
from keyboard import press
from PIL import ImageGrab
import webbrowser
import pyautogui
from time import sleep

engine = pyttsx3.init('sapi5')
engine.setProperty('volume', 1.5)
engine.setProperty('rate', 174)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def play_alarm_sound():
    pygame.mixer.init()
    pygame.mixer.music.load("Pocomobilephone.mp3")
    pygame.mixer.music.play()


def find_my_ip():
    ip_address = requests.get('https://api.ipify.org?format=json').json()
    return ip_address["ip"]


def googlesearch(term):
    query = term.replace("google it", " ")
    print(query)
    query = term.replace("what is", " ")
    print(query)
    query = term.replace("when is", " ")
    print(query)
    query = term.replace("how to", " ")
    print(query)
    query = term.replace("where is", " ")
    print(query)
    query = term.replace("what do you mean", " ")
    print(query)

    Query = str(term)
    pywhatkit.search(Query)

    if 'how to' in Query:
        max_res = 1
        how_to_fun = search_wikihow(query=Query, max_results=max_res, lang="en")
        assert len(how_to_fun) == 1
        how_to_fun[0].print()
        main.speak(how_to_fun[0].summary)

    else:
        search = wikipedia.summary(Query, 2)
        main.speak(f": According to wikipedia : {search} ")


def youtube(video):
    kit.playonyt(video)


EMAIL = config('EMAIL')
PASSWORD = config('PASSWORD')


def send_email(receiver_add, subject, message):
    try:
        email = EmailMessage()
        email['To'] = receiver_add
        email['Subject'] = subject
        email['From'] = EMAIL

        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(email)
        s.close()
        return True
    except Exception as e:
        print(e)
        return False


def get_news():
    api_dict = {
        'business': "https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=f61245cf2ad24b5eb004e28c1a72c76a",
        'entertainment': "https://newsapi.org/v2/top-headlines?country=in&category=entertainment&apiKey=f61245cf2ad24b5eb004e28c1a72c76a",
        'health': "https://newsapi.org/v2/top-headlines?country=in&category=health&apiKey=f61245cf2ad24b5eb004e28c1a72c76a",
        'science': "https://newsapi.org/v2/top-headlines?country=in&category=science&apiKey=f61245cf2ad24b5eb004e28c1a72c76a",
        'sports': "https://newsapi.org/v2/top-headlines?country=in&category=sports&apiKey=f61245cf2ad24b5eb004e28c1a72c76a",
        'technology': "https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey=f61245cf2ad24b5eb004e28c1a72c76a"}

    content = None
    url = None
    speak("Which field news do you want, [business], [health], [technology], [sports], [entertainment], [science]")
    field = input("Type field news that you want: ")

    for key, value in api_dict.items():
        if key.lower() in field.lower():
            url = value
            print(url)
            print("URL was found")
            break

    if url is None:
        print("URL not found")
    else:
        News = requests.get(url).text
        News = json.loads(News)
        speak("Here is the first news.")

        articles = News["articles"]
        for article in articles:
            title = article["title"]
            print(title)
            speak(title)
            news_url = article["url"]
            print(f"For more info, visit: {news_url}")

            a = input("[Press 1 to continue] and [Press 2 to stop]")
            if str(a) == "1":
                pass
            elif str(a) == "2":
                break

        speak("That's all")


def jokes():
    # print(pyjokes.get_joke())
    speak(pyjokes.get_joke())


def alarm(alarm_time):
    try:
        alarm_time_struct = time.strptime(alarm_time, "%H:%M")
        alarm_hour, alarm_minute = alarm_time_struct.tm_hour, alarm_time_struct.tm_min

        while True:
            current_time = time.localtime()
            if current_time.tm_hour == alarm_hour and current_time.tm_min == alarm_minute:
                speak("Time to wake up! The alarm is going off!")
                play_alarm_sound()
                break
            time.sleep(60)  # Check the time every minute

    except ValueError:
        speak("Invalid time format. Please use the format HH:MM, e.g., 07:30.")


def my_location():
    ip_add = requests.get('https://api.ipify.org').text
    url = 'https://get.geojs.io/v1/ip/geo/' + ip_add + '.json'
    geo_q = requests.get(url)
    geo_d = geo_q.json()
    city = geo_d['city']
    country = geo_d['country']
    print(city, country)
    speak(f"now you are in {city, country}.")


def map(place):
    url = "https://www.google.com/maps/place/" + str(place)
    web.open(url=url)
    geoloc = Nominatim(user_agent="myGeocoder")
    location = geoloc.geocode(place, addressdetails=True)
    location = location.raw['address']
    target = {'city': location.get('city', ''),
              'state': location.get('state', ''),
              'country': location.get('country', '')}
    speak(target)


def notepad():
    speak("Tell me the query")
    speak("I'm ready to note down")
    writes = main.takeCommand()
    time = datetime.datetime.now().strftime("%H:%M")
    filename = str(time).replace(":", "-") + "-note.txt"
    with open(filename, "w") as file:
        file.write(writes)
    path1 = "C:\\Users\\HP\\PycharmProjects\\desktopai1\\" + str(filename)
    os.startfile(path1)


def close_note():
    os.system("TASKKILL /F /im Notepad.exe")


def get_weather(city_name):
    base_url = f'https://www.timeanddate.com/weather/india/{city_name}'

    try:
        response = requests.get(base_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as req_err:
        print(f'Request error occurred: {req_err}')
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    location = soup.select_one('h1').text.strip()
    temperature = soup.select_one('.h2').text.strip()
    weather_description = soup.select_one('.h2 + p').text.strip()

    weather_data = {
        'Location': location,
        'Temperature': temperature,
        'Description': weather_description
    }

    return weather_data


def speakWeather(weather_info, city_name):
    if weather_info:
        speak(f'{weather_info["Location"]}:')
        speak(f'Temperature: {weather_info["Temperature"]}')
        speak(f'Description: {weather_info["Description"]}')
    else:
        speak(f'Failed to fetch weather information for {city_name}.')


city_name = 'mangalore'
weather_info = get_weather(city_name)


# speakWeather(weather_info, city_name)

def launch_application(app_name):
    try:
        os.startfile(app_name)
    except FileNotFoundError:
        print(f"Program '{app_name}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def take_screenshot():
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    screenshot_path = f"screenshot_{timestamp}.png"
    ImageGrab.grab().save(screenshot_path)
    return screenshot_path


def generic_question_answer(question):
    responses = {
        "what is your name": "My name is Hazel, I am Assistant, Created by Tushar and Varun.",
        "how are you": "As an A I, I don't have feelings, but I'm here to assist you!",
        "who is the president of the USA": "I don't have real-time data, so I can't provide the current president.",
        "how old are you": "I am just a program, so I don't have an age.",
        "what can you do": "I can answer questions, provide information, and engage in basic conversations.",
        "who created you": "I was created by Tushar and Varun.",
        "what is the meaning of life": "The meaning of life is a philosophical question. There are many interpretations.",
        "where are you from": "I exist in the digital realm and don't have a physical location.",
        "who won the last World Cup": "I don't have real-time data, so I can't provide the latest World Cup winner.",
        "what is the capital of France": "The capital of France is Paris.",
        "what is the square root of 144": "The square root of 144 is 12.",
        "do you have any hobbies": "As an AI, I don't have hobbies, but I love helping users like you!",
        "What can I do for you": "You can ask me any question, and I'll do my best to assist you!",
        "who is your favorite superhero": "I don't have personal preferences, so I don't have a favorite superhero.",
        "what is the answer to life, the universe, and everything": "The answer is 42, according to Douglas Adams' 'Hitchhiker's Guide to the Galaxy.'",
        "where can I find a good restaurant": "I don't have access to real-time data, but you can use online maps and reviews to find restaurants.",
        "what is the current stock price of Google": "I don't have access to real-time financial data.",
        "do you know any riddles": "Sure! Here's one: I speak without a mouth and hear without ears. I have no body, but I come alive with the wind. What am I? Answer: An echo.",
        "what languages do you speak": "I primarily speak and understand English, but I can try to understand other languages too.",
        "what is the meaning of AI": "AI stands for Artificial Intelligence, which refers to the simulation of human intelligence in machines.",
        "can you learn and improve": "As a static model, I don't have the ability to learn or improve over time.",
        "what is the population of China": "As of my last update, the population of China is approximately 1.4 billion.",
        "who wrote Romeo and Juliet": "Romeo and Juliet was written by William Shakespeare.",
        "tell me a fun fact": "A group of flamingos is called a 'flamboyance.'",
        "what is the tallest mountain in the world": "Mount Everest is the tallest mountain in the world.",
        "what is the speed of light": "The speed of light in a vacuum is approximately 299,792,458 meters per second.",
        "what is your favorite book": "As an AI, I don't have personal preferences, so I don't have a favorite book.",
        "who is the founder of Microsoft": "Microsoft was co-founded by Bill Gates and Paul Allen.",
        "what is the boiling point of water": "The boiling point of water at sea level is 100 degrees Celsius.",
        "what is the capital of Japan": "The capital of Japan is Tokyo.",
        "who painted the Mona Lisa": "The Mona Lisa was painted by Leonardo da Vinci.",
        "do you dream": "As an A I language model, I don't have consciousness or the ability to dream.",
        "what is the largest animal on Earth": "The blue whale is the largest animal on Earth.",
        "what is the currency of Japan": "The currency of Japan is the Japanese yen (JPY).",
        "who discovered gravity": "Sir Isaac Newton is credited with discovering the concept of gravity.",
        "what is the color of the sky": "The color of the sky appears blue due to Rayleigh scattering of sunlight.",
        "what is the national flower of England": "The national flower of England is the rose.",
        "who is the author of 'Harry Potter'": "The 'Harry Potter' series was written by J.K. Rowling.",
        "what is the freezing point of water": "The freezing point of water at sea level is 0 degrees Celsius.",
        "what is the capital of Australia": "The capital of Australia is Canberra.",
        "what is the diameter of Earth": "The diameter of Earth is approximately 12,742 kilometers (7,917.5 miles).",
        "who is the CEO of Tesla": "As of my last update, the CEO of Tesla is Elon Musk.",
        "what is the meaning of 'serendipity'": "Serendipity refers to finding valuable or delightful things by chance.",
        "do you like cats or dogs": "As an AI, I don't have a preference between cats and dogs.",
        "who wrote the famous play 'Hamlet'": "The play 'Hamlet' was written by William Shakespeare.",
        "what is the capital of Brazil": "The capital of Brazil is Brasília.",
        "how far is the Moon from Earth": "The average distance is about 384,400 kilometers.",
        "what is the national animal of India": "The national animal of India is the Bengal tiger.",
        "who was the first person in space": "Yuri Gagarin,was the first person to travel to space.",
        "what is the largest ocean in the world": "The largest ocean in the world is the Pacific Ocean.",
        "who is known as the 'Father of Physics'": "Sir Isaac Newton is often referred to as the 'Father of Physics.'",
        "what is the national bird of the United States": "The national bird of the United States is the bald eagle.",
        "what is the capital of China": "The capital of China is Beijing.",
        "who is the author of 'To Kill a Mockingbird'": "The novel 'To Kill a Mockingbird' was written by Harper Lee.",
        "what is the currency of the United Kingdom": "The currency of the United Kingdom is the British pound sterling (GBP).",
        "who is the current CEO of Apple": "As of my last update, the CEO of Apple is Tim Cook."
    }

    if question in responses:
        return responses[question]
    else:
        return "I'm sorry, I don't have an answer for that question."


def playsong(song):
    webbrowser.open(f'https://open.spotify.com/search/{song}')
    sleep(5)
    pyautogui.click(x=1005, y=617)
    speak("Playing" + song)
