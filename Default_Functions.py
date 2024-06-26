##################################################
# Main Function for Launching Lucy AI ChatBot    #
# Version 1.0.1.12 - Released 2024-05-07         #
# Author - Lawrence Lutton                       #
##################################################

# Importing libraries
import csv
import logging
import os
import os.path
import re
import sys
from datetime import datetime
# import psutil # type: ignore
from typing import Literal, get_args
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import pandas as pd
import requests
import speech_recognition as sr
from PyQt5.QtWidgets import *
from bs4 import BeautifulSoup
from gtts import gTTS
import pyttsx3
from selenium import webdriver # to control browser operations
import assistant
import pync
import time
import creds

recognizer = sr.Recognizer()

# Initialize the recognizer
r = sr.Recognizer()

city_names = ["Aberdeen", "Abilene", "Akron", "Albany", "Albuquerque", "Alexandria", "Allentown", "Amarillo", "Anaheim",
              "Anchorage", "Ann Arbor", "Antioch", "Apple Valley", "Appleton", "Arlington", "Arvada", "Asheville",
              "Athens", "Atlanta", "Atlantic City", "Augusta", "Aurora", "Austin", "Bakersfield", "Baltimore",
              "Barnstable", "Baton Rouge", "Beaumont", "Bel Air", "Bellevue", "Berkeley", "Bethlehem", "Billings",
              "Birmingham", "Bloomington", "Boise", "Boise City", "Bonita Springs", "Boston", "Boulder", "Bradenton",
              "Bremerton", "Bridgeport", "Brighton", "Brownsville", "Bryan", "Buffalo", "Burbank", "Burlington",
              "Cambridge", "Canton", "Cape Coral", "Carrollton", "Cary", "Cathedral City", "Cedar Rapids", "Champaign",
              "Chandler", "Charleston", "Charlotte", "Chattanooga", "Chesapeake", "Chicago", "Chula Vista",
              "Cincinnati", "Clarke County", "Clarksville", "Clearwater", "Cleveland", "College Station",
              "Colorado Springs", "Columbia", "Columbus", "Concord", "Coral Springs", "Corona", "Corpus Christi",
              "Costa Mesa", "Dallas", "Daly City", "Danbury", "Davenport", "Davidson County", "Dayton", "Daytona Beach",
              "Deltona", "Denton", "Denver", "Des Moines", "Detroit", "Downey", "Duluth", "Durham", "El Monte",
              "El Paso", "Elizabeth", "Elk Grove", "Elkhart", "Erie", "Escondido", "Eugene", "Evansville", "Fairfield",
              "Fargo", "Fayetteville", "Fitchburg", "Flint", "Fontana", "Fort Collins", "Fort Lauderdale", "Fort Smith",
              "Fort Walton Beach", "Fort Wayne", "Fort Worth", "Frederick", "Fremont", "Fresno", "Fullerton",
              "Gainesville", "Garden Grove", "Garland", "Gastonia", "Gilbert", "Glendale", "Grand Prairie",
              "Grand Rapids", "Grayslake", "Green Bay", "GreenBay", "Greensboro", "Greenville", "Gulfport-Biloxi",
              "Hagerstown", "Hampton", "Harlingen", "Harrisburg", "Hartford", "Havre de Grace", "Hayward", "Hemet",
              "Henderson", "Hesperia", "Hialeah", "Hickory", "High Point", "Hollywood", "Honolulu", "Houma", "Houston",
              "Howell", "Huntington", "Huntington Beach", "Huntsville", "Independence", "Indianapolis", "Inglewood",
              "Irvine", "Irving", "Jackson", "Jacksonville", "Jefferson", "Jersey City", "Johnson City", "Joliet",
              "Kailua", "Kalamazoo", "Kaneohe", "Kansas City", "Kennewick", "Kenosha", "Killeen", "Kissimmee",
              "Knoxville", "Lacey", "Lafayette", "Lake Charles", "Lakeland", "Lakewood", "Lancaster", "Lansing",
              "Laredo", "Las Cruces", "Las Vegas", "Layton", "Leominster", "Lewisville", "Lexington", "Lincoln",
              "Little Rock", "Long Beach", "Lorain", "Los Angeles", "Louisville", "Lowell", "Lubbock", "Macon",
              "Madison", "Manchester", "Marina", "Marysville", "McAllen", "McHenry", "Medford", "Melbourne", "Memphis",
              "Merced", "Mesa", "Mesquite", "Miami", "Milwaukee", "Minneapolis", "Miramar", "Mission Viejo", "Mobile",
              "Modesto", "Monroe", "Monterey", "Montgomery", "Moreno Valley", "Murfreesboro", "Murrieta", "Muskegon",
              "Myrtle Beach", "Naperville", "Naples", "Nashua", "Nashville", "New Bedford", "New Haven", "New London",
              "New Orleans", "New York", "New York City", "Newark", "Newburgh", "Newport News", "Norfolk", "Normal",
              "Norman", "North Charleston", "North Las Vegas", "North Port", "Norwalk", "Norwich", "Oakland", "Ocala",
              "Oceanside", "Odessa", "Ogden", "Oklahoma City", "Olathe", "Olympia", "Omaha", "Ontario", "Orange",
              "Orem", "Orlando", "Overland Park", "Oxnard", "Palm Bay", "Palm Springs", "Palmdale", "Panama City",
              "Pasadena", "Paterson", "Pembroke Pines", "Pensacola", "Peoria", "Philadelphia", "Phoenix", "Pittsburgh",
              "Plano", "Pomona", "Pompano Beach", "Port Arthur", "Port Orange", "Port Saint Lucie", "Port St. Lucie",
              "Portland", "Portsmouth", "Poughkeepsie", "Providence", "Provo", "Pueblo", "Punta Gorda", "Racine",
              "Raleigh", "Rancho Cucamonga", "Reading", "Redding", "Reno", "Richland", "Richmond", "Richmond County",
              "Riverside", "Roanoke", "Rochester", "Rockford", "Roseville", "Round Lake Beach", "Sacramento", "Saginaw",
              "Saint Louis", "Saint Paul", "Saint Petersburg", "Salem", "Salinas", "Salt Lake City", "San Antonio",
              "San Bernardino", "San Buenaventura", "San Diego", "San Francisco", "San Jose", "Santa Ana",
              "Santa Barbara", "Santa Clara", "Santa Clarita", "Santa Cruz", "Santa Maria", "Santa Rosa", "Sarasota",
              "Savannah", "Scottsdale", "Scranton", "Seaside", "Seattle", "Sebastian", "Shreveport", "Simi Valley",
              "Sioux City", "Sioux Falls", "South Bend", "South Lyon", "Spartanburg", "Spokane", "Springdale",
              "Springfield", "St. Louis", "St. Paul", "St. Petersburg", "Stamford", "Sterling Heights", "Stockton",
              "Sunnyvale", "Syracuse", "Tacoma", "Tallahassee", "Tampa", "Temecula", "Tempe", "Thornton",
              "Thousand Oaks", "Toledo", "Topeka", "Torrance", "Trenton", "Tucson", "Tulsa", "Tuscaloosa", "Tyler",
              "Utica", "Vallejo", "Vancouver", "Vero Beach", "Victorville", "Virginia Beach", "Visalia", "Waco",
              "Warren", "Washington", "Waterbury", "Waterloo", "West Covina", "West Valley City", "Westminster",
              "Wichita", "Wilmington", "Winston", "Winter Haven", "Worcester", "Yakima", "Yonkers", "York",
              "Youngstown"]

# Setting up a list for error logging levels.
LogLevel = Literal['Info', 'Error', 'Critical']

# Creating the Main Logging Function

#  Creates a nice Date Stamp for use with Logging.
def DateTimeLog():
    # datetime object containing current date and time
    now = datetime.now()
    # mm/dd/YY H:M:S
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
    return dt_string


# End DateTime Function

def WriteLog(Message, FuncName, ErrorType: LogLevel = "Info"):
    options = get_args(LogLevel)
    assert ErrorType in options, f"'{ErrorType}' is not in {options}"

    TimeStamp: str = DateTimeLog()
    logger = logging.getLogger(FuncName)
    if ErrorType == 'Info':
        logging.basicConfig(filename='events.log', level=logging.INFO)
        logger.info(repr(TimeStamp) + ": " + repr(Message) + '')
    elif ErrorType == 'Error':
        logging.basicConfig(filename='events.log', level=logging.ERROR)
        logger.error(repr(TimeStamp) + ": " + repr(Message) + '')
    elif ErrorType == 'Critical':
        logging.basicConfig(filename='events.log', level=logging.CRITICAL)
        logger.critical(repr(TimeStamp) + ": " + repr(Message) + '')

    """
    TimeStamp = DateTimeLog()

    f = open("events.log", "a")
    f.write(repr(TimeStamp) + " " + repr( ErrorType ) + " " + repr( Message ) + '\n')
    f.close()

    #open and read the file after the appending:
    #f = open("events.log", "r")
    #print(f.read())
    """
# End WriteLog Function


# Had to wait for the correct functions to load before writing eventlog
WriteLog(Message='Starting Default Functions', FuncName='Default_Functions', ErrorType='Info')


def telegram_ai_chatbot():
    WriteLog(Message='Starting telegram_ai_chatbot Functions', FuncName='telegram_ai_chatbot', ErrorType='Info')
    import os
    import telebot

    BOT_TOKEN = f"{creds.BOT_TOKEN}"

    bot = telebot.TeleBot(BOT_TOKEN)

    @bot.message_handler(commands=['start', 'hello'])
    def send_welcome(message):
        bot.reply_to(message, "Howdy, how are you doing?")

    @bot.message_handler(func=lambda msg: True)
    def echo_all(message):

        # bot.reply_to(message, message.text)
        lucy_question = bot.reply_to(message, message.text)
        print(f"{lucy_question.text}")
        lucy_response = lucy_gpt_chat(query=f"{lucy_question.text}")
        bot.reply_to(message, f"{lucy_response}")

    bot.infinity_polling()


# create_csv_file with checks
def create_csv_file():
    # Defining file name
    path = './CPU.csv'

    check_file = os.path.isfile(path)

    if check_file:
        WriteLog(Message='CPU.csv already exist', FuncName='create_csv_file', ErrorType='Info')
        return 0
    else:
        try:
            WriteLog(Message='Creating file CPU.csv', FuncName='create_csv_file', ErrorType='Info')
            with open('CPU.csv', 'a', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=',',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow(["CPU", "AVG Usage", "Number Of Cores"])
            return 0
        except Exception as e:
            WriteLog(Message='Error Creating file ' + str(e), FuncName='create_csv_file', ErrorType='Critical')
        return 2


# Writing to a CSV File with checks
def WriteToCSV(filename, coldata):
    CSVFILE = create_csv_file()

    if CSVFILE == 0:
        try:
            WriteLog(Message='Opening file CPU.csv', FuncName='WriteToCSV', ErrorType='Info')
            with open(f'{filename}', 'a', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=',',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow([f"{coldata}"])
        except Exception as e:
            WriteLog(Message='Error Opening file ' + str(e), FuncName='WriteToCSV', ErrorType='Critical')
    elif CSVFILE == 2:
        WriteLog(Message='Error Opening file ' + str(), FuncName='WriteToCSV', ErrorType='Critical')


def reminder(query):
    pync.notify(title="Reminder", message =f"{query}", timeout=1)
    while True:
        reminder()
    time.sleep(10)


# get weather
def get_weather(city):
    WriteLog(Message='getting weather info', FuncName='get_weather', ErrorType='Info')

    if city is None:
        # enter city name
        city = "Boise"

    # create url
    url = "https://www.google.com/search?q=" + "weather" + city

    # requests instance
    html = requests.get(url).content

    # getting raw data
    soup = BeautifulSoup(html, 'html.parser')

    # get the temperature
    temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text

    # this contains time and sky description
    str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text

    # format the data
    data = str.split('\n')
    time = data[0]
    sky = data[1]
    weather = (f"{data}" + f" {temp}")
    return weather


# End get weather

# Lucy function with Training
def Lucy():
    WriteLog(Message='Starting Lucy Functions', FuncName='Lucy', ErrorType='Info')
    from chatterbot import ChatBot
    from chatterbot.trainers import ListTrainer
    from chatterbot.trainers import ChatterBotCorpusTrainer

    chatbot = ChatBot(
        "Lucy",
        storage_adapter="chatterbot.storage.SQLStorageAdapter",
        # database="Bot1.sqlite3",
        database_uri='sqlite:///site////lucy.sqlite3',
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': 'I am not sure how to respond to that, I am still learning',
                'maximum_similarity_threshold': 0.60
            }
        ]
    )

    # Disabling trainers

    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train("chatterbot.corpus.english")
    trainer = ListTrainer(chatbot)
    trainer.train([
        "Hi",
        "Hello, I am Lucy!!! 🤗",
    ])
    trainer.train([
        "Hi",
        "Hello, what a great day!",
    ])
    trainer.train([
        "Hello, AI",
        "Welcome to Lucy!!! 🤗",
    ])
    trainer.train([
        "Are you a plant?",
        "No, I am Lucy an AI System to help you LOL",
    ])
    trainer.train([
        "What is your purpose?",
        "To Help make your life better!",
    ])
    # Define a list of conversation pairs
    conversation = [
        "Hello",
        "Hi there!",
        "How are you doing?",
        "I'm doing great, thank you! How can I help you today?",
        # ... more conversation pairs
    ]
    conversation2 = [
        "Funny how they have the load I pickup deliver Monday but, I got 13hrs now. I get back 5 tonight, then 2 then 11 lol",
        "I have two like 3 hour days, not sure if I'll be able to actually make this load on time",
        "It's impossibl in their time frame, Cuz I'll get to Portland at least then somewhere between there and Richland I'll be bobtail so... maybe space age or something I can make a spot idk.  Then I'll basically have no time, and only get 5hrs for tomorrow lolllll. Stupid. Can't do 2044 total miles by Monday morning.",
    ]
    conversation3 = [
        "Whats a good allergy med for dogs",
        "Benadryl",
        "Roger that, How much for foxy",
        "According to the Merck Veterinary Manual, the standard dose for Benadryl® is 2 to 4 milligrams per kilogram of body weight, or 0.9 to 1.8 milligrams mg of Benadryl® per pound. Therefore, a simple and practical dose is 1 mg of Benadryl® per pound of your dogs weight, given two to three times a day.",
        "You rock!",
        "Most bendryl is 25 mg. So Id say 1/3-1/2 pill,  You cant OD on benedryl, A pistachio cream, cold brew grande, Haha. Changed my mind. A pistachio latte 12 ounce hot",
        "Roger that.  Be there in a few!",
        "Headed your way",
        "Sweet! See you in a bit, I got the discs from Jen",
        "Serena is coming. But she doesnt want to play. She just wants to get out of the house for a bit.",
        "Headed to Nampa now then your place",
        "See you soon. I have your Lego! And you have my water bottle. 🙃 Also if you bring your camp stove and tanae cover I can work on getting those posted for sale.",
        "I will bring them over today.",
        "It was great seeing you today 🙃🤔",
    ]
    # Train the chatbot with your custom conversation
    trainer.train(conversation)
    trainer.train(conversation2)
    trainer.train(conversation3)

    # Disabling CSV import training

    # Training the AI with a CSV file with standard questions and answers
    # making data frame from csv file
    data = pd.read_csv("dialogs_expanded.csv", index_col="Index")
    i = 0
    for row in data.index:
        # retrieving row by loc method
        first = (data['Question'].values[i])
        second = (data['Answer'].values[i])

        # Adding info from the csv file for training...
        question = (f'{first}')
        answer = (f'{second}')

        print(f"{question}", f"{answer}")
        trainer.train([
            f"{question}",
            f"{answer}",
        ])
        i += 1

    exit_conditions = (":q", "quit", "exit")
    while True:
        # Getting speech instead of having to type to chatpot
        input("Press Enter to continue...")
        audio = record_audio()
        query = recognize_speech(audio)
        # query = input("> ")
        if query is None:

            audio = record_audio()
            query = recognize_speech(audio)
        elif query in exit_conditions:
            speech = (f"Goodbye")

            print(f"🪴 {speech}")
            text_to_speech(text=speech)
            break
        elif 'get weather' in query or 'what is the weather' in query:
            speech = (f"What City would you like me to check for you?")
            print(f"🤪 {speech}")
            text_to_speech(text=speech)
            audio = record_audio()
            checkCity = recognize_speech(audio)

            speech = (f"Getting weather for {checkCity}! Please wait a second...")
            print(f"🤪 {speech}")
            text_to_speech(text=speech)

            weather = get_weather(city=f"{checkCity}")
            print(f"🪴 Here is your weather {weather}")
            speech = (f"Here is your weather {weather}")
            text_to_speech(text=speech)
        else:
            #EmotionsMarker = EmotionsChatMarker(GetEmotion = f"{query}")
            speech = (f"{chatbot.get_response(query)}")
            #print(f"🤪 {speech}" + f"🤔 Your emotional marker is {EmotionsMarker}")
            print(f"🤪 {speech}")
            text_to_speech(text=speech)

    WriteLog(Message='Closing Lucy Functions', FuncName='Lucy', ErrorType='Info')
# End Lucy

# EmotionsChatMarker function
def EmotionsChatMarker(GetEmotion):
    WriteLog(Message='Starting EmotionsChatMarker Functions', FuncName='EmotionsChatMarker', ErrorType='Info')
    # Importing ChatBot functions
    from chatterbot import ChatBot
    #from chatterbot.trainers import ListTrainer
    #from chatterbot.trainers import ChatterBotCorpusTrainer

    # Creating ChatBot
    chatbot = ChatBot(
        "EmotionalMarker",
        storage_adapter="chatterbot.storage.SQLStorageAdapter",
        database_uri='sqlite:///site////EmotionalMarker.sqlite3',
    )

    # Loading and training Chatbot
    #trainer = ChatterBotCorpusTrainer(chatbot)
    #trainer.train("chatterbot.corpus.english")
    #trainer = ListTrainer(chatbot)

    """
    # Trainging the AI with a CSV file
    # making data frame from csv file
    data = pd.read_csv("emotion_sentimen_dataset.csv", index_col ="Index")
    i = 0
    # Creates a loop for every row in the CSV file
    for row in data.index:
        
        # retrieving row by loc method
        first = (data['text'].values[i])
        
        second = (data['Emotion'].values[i])
        
        #Adding info from the csv file for training...
        # Formatting question and answer for the AI Trainer
        question = (f'{first}')
        answer = (f'{second}')
        
        # Using CSV to train
        trainer.train([
            f"{question}",
            f"{answer}",
        ])
        i += 1
    """
    speech = (f"{chatbot.get_response(GetEmotion)}")
    print(f"🤔 {speech}")

    WriteLog(Message='Closing EmotionsChatMarker Functions', FuncName='EmotionsChatMarker', ErrorType='Info')
    return speech
# End EmotionsChatMarker

# Creates mp3 for speech
def text_to_speech(text):
    WriteLog(Message='Starting text_to_speech Functions', FuncName='text_to_speech', ErrorType='Info')
    # Initialize gTTS with the text to convert
    speech = gTTS(text)

    # Save the audio file to a temporary file
    speech_file = 'speech.mp3'
    speech.save(speech_file)

    # Play the audio file
    os.system('afplay ' + speech_file)
    WriteLog(Message='Closing text_to_speech Functions', FuncName='text_to_speech', ErrorType='Info')

def get_cityForWeather(query: object) -> object:
    """

    :param query:
    City Name
    :return:
    """
    WriteLog(Message='Starting get_cityForWeather Functions', FuncName='get_cityForWeather', ErrorType='Info')
    citynames: str = (
        'Aberdeen|Abilene|Akron|Albany|Albuquerque|Alexandria|Allentown|Amarillo|Anaheim|Anchorage|Ann '
        'Arbor|Antioch|Apple Valley|Appleton|Arlington|Arvada|Asheville|Athens|Atlanta|Atlantic '
        'City|Augusta|Aurora|Austin|Bakersfield|Baltimore|Barnstable|Baton Rouge|Beaumont|Bel '
        'Air|Bellevue|Berkeley|Bethlehem|Billings|Birmingham|Bloomington|Boise|Boise City|Bonita '
        'Springs|Boston|Boulder|Bradenton|Bremerton|Bridgeport|Brighton|Brownsville|Bryan|Buffalo|Burbank|Burlington'
        '|Cambridge|Canton|Cape Coral|Carrollton|Cary|Cathedral City|Cedar '
        'Rapids|Champaign|Chandler|Charleston|Charlotte|Chattanooga|Chesapeake|Chicago|Chula Vista|Cincinnati|Clarke '
        'County|Clarksville|Clearwater|Cleveland|College Station|Colorado Springs|Columbia|Columbus|Concord|Coral '
        'Springs|Corona|Corpus Christi|Costa Mesa|Dallas|Daly City|Danbury|Davenport|Davidson County|Dayton|Daytona '
        'Beach|Deltona|Denton|Denver|Des Moines|Detroit|Downey|Duluth|Durham|El Monte|El Paso|Elizabeth|Elk '
        'Grove|Elkhart|Erie|Escondido|Eugene|Evansville|Fairfield|Fargo|Fayetteville|Fitchburg|Flint|Fontana|Fort '
        'Collins|Fort Lauderdale|Fort Smith|Fort Walton Beach|Fort Wayne|Fort '
        'Worth|Frederick|Fremont|Fresno|Fullerton|Gainesville|Garden Grove|Garland|Gastonia|Gilbert|Glendale|Grand '
        'Prairie|Grand Rapids|Grayslake|Green Bay|GreenBay|Greensboro|Greenville|Gulfport-Biloxi|Hagerstown|Hampton'
        '|Harlingen|Harrisburg|Hartford|Havre de Grace|Hayward|Hemet|Henderson|Hesperia|Hialeah|Hickory|High '
        'Point|Hollywood|Honolulu|Houma|Houston|Howell|Huntington|Huntington '
        'Beach|Huntsville|Independence|Indianapolis|Inglewood|Irvine|Irving|Jackson|Jacksonville|Jefferson|Jersey '
        'City|Johnson City|Joliet|Kailua|Kalamazoo|Kaneohe|Kansas '
        'City|Kennewick|Kenosha|Killeen|Kissimmee|Knoxville|Lacey|Lafayette|Lake '
        'Charles|Lakeland|Lakewood|Lancaster|Lansing|Laredo|Las Cruces|Las '
        'Vegas|Layton|Leominster|Lewisville|Lexington|Lincoln|Little Rock|Long Beach|Lorain|Los '
        'Angeles|Louisville|Lowell|Lubbock|Macon|Madison|Manchester|Marina|Marysville|McAllen|McHenry|Medford'
        '|Melbourne|Memphis|Merced|Mesa|Mesquite|Miami|Milwaukee|Minneapolis|Miramar|Mission '
        'Viejo|Mobile|Modesto|Monroe|Monterey|Montgomery|Moreno Valley|Murfreesboro|Murrieta|Muskegon|Myrtle '
        'Beach|Naperville|Naples|Nashua|Nashville|New Bedford|New Haven|New London|New Orleans|New York|New York '
        'City|Newark|Newburgh|Newport News|Norfolk|Normal|Norman|North Charleston|North Las Vegas|North '
        'Port|Norwalk|Norwich|Oakland|Ocala|Oceanside|Odessa|Ogden|Oklahoma '
        'City|Olathe|Olympia|Omaha|Ontario|Orange|Orem|Orlando|Overland Park|Oxnard|Palm Bay|Palm '
        'Springs|Palmdale|Panama City|Pasadena|Paterson|Pembroke '
        'Pines|Pensacola|Peoria|Philadelphia|Phoenix|Pittsburgh|Plano|Pomona|Pompano Beach|Port Arthur|Port '
        'Orange|Port Saint Lucie|Port St. Lucie|Portland|Portsmouth|Poughkeepsie|Providence|Provo|Pueblo|Punta '
        'Gorda|Racine|Raleigh|Rancho Cucamonga|Reading|Redding|Reno|Richland|Richmond|Richmond '
        'County|Riverside|Roanoke|Rochester|Rockford|Roseville|Round Lake Beach|Sacramento|Saginaw|Saint Louis|Saint '
        'Paul|Saint Petersburg|Salem|Salinas|Salt Lake City|San Antonio|San Bernardino|San Buenaventura|San Diego|San '
        'Francisco|San Jose|Santa Ana|Santa Barbara|Santa Clara|Santa Clarita|Santa Cruz|Santa Maria|Santa '
        'Rosa|Sarasota|Savannah|Scottsdale|Scranton|Seaside|Seattle|Sebastian|Shreveport|Simi Valley|Sioux City|Sioux '
        'Falls|South Bend|South Lyon|Spartanburg|Spokane|Springdale|Springfield|St. Louis|St. Paul|St. '
        'Petersburg|Stamford|Sterling Heights|Stockton|Sunnyvale|Syracuse|Tacoma|Tallahassee|Tampa|Temecula|Tempe'
        '|Thornton|Thousand Oaks|Toledo|Topeka|Torrance|Trenton|Tucson|Tulsa|Tuscaloosa|Tyler|Utica|Vallejo|Vancouver'
        '|Vero Beach|Victorville|Virginia Beach|Visalia|Waco|Warren|Washington|Waterbury|Waterloo|West Covina|West '
        'Valley City|Westminster|Wichita|Wilmington|Winston|Winter Haven|Worcester|Yakima|Yonkers|York|Youngstown')
    checkCity = re.findall(citynames, query, flags=re.IGNORECASE)
    checkCityFixed = str(checkCity)[1:-1]
    WriteLog(Message='Closing get_cityForWeather Functions', FuncName='get_cityForWeather', ErrorType='Info')
    return checkCityFixed


def get_ApplicationName(query):
    WriteLog(Message='Starting get_ApplicationName Functions', FuncName='get_ApplicationName', ErrorType='Info')
    application_names = ('Chrome|Notes|')
    checkapplication_names = re.findall(application_names, query, flags=re.IGNORECASE)
    checkapplication_namesFixed = str(application_names)[1:-1]
    WriteLog(Message='Closing get_ApplicationName Functions', FuncName='get_ApplicationName', ErrorType='Info')
    return checkapplication_namesFixed


# testing a different method of getting and speaking text
def SpeechToTextTesting():
    WriteLog(Message='Starting SpeechToTextTesting Functions', FuncName='SpeechToTextTesting', ErrorType='Info')
    """
    recognizer.recognize_google(),
    recognizer.recognize_tensorflow(),
    recognizer.recognize_whisper(),
    recognizer.recognize_sphinx(), 
    recognizer.recognize_google_cloud(), 
    recognizer.recognize_wit(), 
    recognizer.recognize_azure(), 
    recognizer.recognize_bing(), 
    recognizer.recognize_lex(), 
    recognizer.recognize_houndify(), 
    recognizer.recognize_amazon(), 
    recognizer.recognize_assemblyai(), 
    recognizer.recognize_ibm()
    """

    # Python program to translate
    # speech to text and text to speech

    # from speech_recognition import Microphone, RequestError, Recognizer, UnknownValueError

    # Function to convert text to
    # speech
    def SpeakText(command):
        engine = pyttsx3.init()
        voices: object = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.say(command)
        engine.runAndWait()
        # from AppKit import NSSpeechSynthesizer
        # speechSynthesizer = NSSpeechSynthesizer.alloc().initWithVoice_("com.apple.speech.synthesis.voice.Bruce")
        # speechSynthesizer.startSpeakingString('hello')

    # Loop infinitely for user to
    # speak

    while 1:

        # Exception handling to handle
        # exceptions at the runtime
        try:

            # use the microphone as source for input.
            with sr.Microphone() as source2:

                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level

                r.adjust_for_ambient_noise(source=source2, duration=0.2)

                # listens for the user's input
                audio2 = r.listen(source2)

                # Using google to recognize audio
                MyText = sr.recognize(audio2)
                MyText = MyText.lower()

                print("Did you say ", MyText)
                SpeakText(command=MyText)

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("unknown error occurred")
    WriteLog(Message='Closing SpeechToTextTesting Functions', FuncName='SpeechToTextTesting', ErrorType='Info')


def record_audio():
    WriteLog(Message='Starting record_audio Functions', FuncName='record_audio', ErrorType='Info')
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.2)
        print(f"🤪 Listening...")
        text_to_speech(text="I'm Listening...")
        audio = r.listen(source=source)
    WriteLog(Message='Closing record_audio Functions', FuncName='record_audio', ErrorType='Info')
    return audio


def recognize_speech(audio):
    WriteLog(Message='Starting recognize_speech Functions', FuncName='recognize_speech', ErrorType='Info')
    try:
        text = recognizer.recognize_google(audio)
        print(f"🤪 You said: {text}")
        WriteLog(Message='Closing recognize_speech Functions', FuncName='recognize_speech', ErrorType='Info')
        return text
    except sr.UnknownValueError:
        print(f"🤪 Sorry, I couldn't understand that.")
        text = "Sorry, I couldn't understand that."
        WriteLog(Message='Closing recognize_speech Functions', FuncName='recognize_speech', ErrorType='Error')
        return text
    except sr.RequestError:
        print(f"🤪 Sorry, there was an error processing your request.")
        text = "Sorry, there was an error processing your request."
        WriteLog(Message='Closing recognize_speech Functions', FuncName='recognize_speech', ErrorType='Critical')
        return text


def GetSpeech():
    WriteLog(Message='Starting GetSpeech Functions', FuncName='GetSpeech', ErrorType='Info')
    # Getting speech instead of having to type to Lucy
    audio = record_audio()
    query = recognize_speech(audio)
    WriteLog(Message='Closing GetSpeech Functions', FuncName='GetSpeech', ErrorType='Info')
    return query


# Lucy function
def LucyGUI(query):
    WriteLog(Message='Starting Lucy Functions', FuncName='Lucy', ErrorType='Info')
    from chatterbot import ChatBot
    chatbot = ChatBot(
        "Lucy",
        storage_adapter="chatterbot.storage.SQLStorageAdapter",
        database_uri='sqlite:///site////lucy.sqlite3',
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': 'I am not sure how to respond to that, I am still learning',
                'maximum_similarity_threshold': 0.40
            }
        ]
    )

    exit_conditions = (":q", "quit", "exit")

    if query in exit_conditions:
        speech = f"Goodbye"
        print(f"🤪 {speech}")
        text_to_speech(text=speech)
        WriteLog(Message='Closing Lucy Functions', FuncName='Lucy', ErrorType='Info')
        return f"🤪 {speech}"
    elif 'get weather' in query or 'what is the weather' in query:
        checkCityFixed = get_cityForWeather(query=query)

        if checkCityFixed is None:
            speech = f"What City would you like me to check for you?"
            print(f"🤪 {speech}")
            text_to_speech(text=speech)

            checkCityFixed = GetSpeech()

            speech = f"Getting weather for {checkCityFixed}! Please wait a second..."
            print(f"🤪 {speech}")
            text_to_speech(text=speech)

        weather = get_weather(city=f"{checkCityFixed}")
        print(f"🤪 Here is your weather {weather}")
        speech = f"Here is your weather for {checkCityFixed} {weather}"
        text_to_speech(text=speech)
        WriteLog(Message='Closing Lucy Functions', FuncName='Lucy', ErrorType='Info')
        return f"🤪 {speech}"
    elif 'search' in query or 'youtube' in query or 'wikipedia' in query:
        search_web(query)
        print(f"🤪 Here is your web search")
        speech = f"Here is your web search"
        text_to_speech(text=speech)
        WriteLog(Message='Closing Lucy Functions', FuncName='Lucy', ErrorType='Info')
        return f"🤪 {speech}"
    elif 'remind me' in query or 'set reminder' in query:
        reminder(query)
        print(f"🤪 Setting Reminder")
        speech = f"Setting Reminder"
        text_to_speech(text=speech)
        WriteLog(Message='Closing Lucy Functions', FuncName='Lucy', ErrorType='Info')
        return f"🤪 {speech}"
    else:
        # EmotionsMarker = EmotionsChatMarker(GetEmotion = f"{query}")
        speech = f"{chatbot.get_response(query)}"
        # print(f"🤪 {speech}" + f"🤔 Your emotional marker is {EmotionsMarker}")
        print(f"🤪 {speech}")
        text_to_speech(text=speech)
        WriteLog(Message='Closing Lucy Functions', FuncName='Lucy', ErrorType='Info')
        return f"🤪 {speech}"

# End Lucy

def lucy_gpt_chat(query):
    import openai

    openai.api_key = f"{creds.api_key}"
    messages = [{"role": "system", "content":
        "You are a intelligent assistant."}]
    while True:
        message = f"{query}"
        if message:
            messages.append(
                {"role": "user", "content": message},
            )
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages
            )
        reply = chat.choices[0].message.content
        if 'remind' in reply:
            print(f"ChatGPT Reminder: {reply}")
            reminder(query=f"{reply}")
            messages.append({"role": "assistant", "content": reply})
            return reply
        elif 'set reminder' in reply:
            print(f"ChatGPT Reminder: {reply}")
            reminder(query=f"{reply}")
            messages.append({"role": "assistant", "content": reply})
            return reply
        else:
            print(f"ChatGPT: {reply}")
            messages.append({"role": "assistant", "content": reply})
            return reply



    # Import the necessary libraries
    # import os
    # import openai
    # Set API key with one of these options

    # Set the role or context of the assistant
    # messages = [{"role": "system", "content": "You are a assistant"}]
    # messages.append({"role": "assistant", "content": f"{query}"})
    # messages.append({"role": "user", "content": "answer with a single sentence. "})
    # Make an API call with default settings
    # answers = openai.ChatCompletion.create(
        # model="gpt-3.5-turbo",
        # These are parameters that can be adjusted
        # temperature = 0.7,
        # max_tokens = 100,
        # top_p=1,
        # frequency_penalty = 0,
        # presence_penalty = 0,
        # messages=messages
    # )
    # Print the response
    # telagram_response = (answers['choices'][0]['message']['content'])
    # print(answers['choices'][0]['message']['content'])
    # return telagram_response

# Creating GUI parameters
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lucy UI 1.0.1.8")
        self.setFixedWidth(600)
        self.setFixedHeight(450)
        self.left = 10
        self.top = 10
        self.width = 1000
        self.height = 1000
        # self.initUI()

        # def initUI(self):
        self.label = QLabel()
        self.TextBox = QTextBrowser()

        self.Button = QPushButton("Submit Text Question")
        self.Button.setCheckable(True)
        self.Button.setDefault(True)
        self.Button.clicked.connect(self.the_button_was_clicked)
        self.Button2 = QPushButton("Submit Spoken Question")
        self.Button2.setCheckable(True)
        self.Button2.setDefault(False)
        self.Button2.clicked.connect(self.speech)
        self.input = QLineEdit()
        self.input.returnPressed.connect(self.Button.click)
        self.input.textChanged.connect(self.label.setText)

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.label)
        layout.addWidget(self.TextBox)
        layout.addWidget(self.Button)
        layout.addWidget(self.Button2)

        container = QWidget()
        container.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)

    def the_button_was_clicked(self):
        textboxValue = self.input.text()
        # print(f"Clicked! {textboxValue}")
        self.TextBox.append(f"🤓 {textboxValue}")
        response = LucyGUI(query=f"{textboxValue}")
        self.TextBox.append(f"{response}")
        self.input.clear()
        if 'Goodbye' in response:
            sys.exit()

    def speech(self):
        # print("Getting speech to text")
        query = GetSpeech()
        self.TextBox.append(f"🤓 {query}")
        response = LucyGUI(query=f"{query}")
        self.TextBox.append(f"{response}")
        if 'Goodbye' in response:
            sys.exit()

def GUI():
    # TODO need to change this to pygame for better response within the app
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    # Start the event loop
    app.exec()


WriteLog(Message='Finished loading all Default Functions Successfully', FuncName='Default_Functions', ErrorType='Info')