# Lucy AI ChatBot 1.0.1.14 - 2024-05-16
## Change Log info
- x.x.x.y Y is the currently active build, once complete Y will be dropped and the version locked in.
### ChangeLog started in ver. 1.0.1.x
#### Current Dev build 1.0.1.14
- Fixed AI training
- Added Text to Speech
- Added Speech to Text
- Added Get_Weather
- Added Emotional Marker Bot (beta)
- Cleaned up Default Functions and MainApp scripts
- Cleaning up function names and var names to meet standards
- Added Telegram Chat bot
- Reminder Function (beta partially working)
- Added write_reminder_file
- Added check_create_reminder_file
- Added Search_Web.py
- Added Image Reorganization
 
# How to run the app
## Running the app
- Once you install all the requirements launch MainApplication.py

## Setup Guide in progress
- You will need to create a creds.py file with these two variables
  - openai.api_key = f"{creds.api_key}"
  - BOT_TOKEN = f"{creds.BOT_TOKEN}"
- Use project requirements file for all packages.
- for psutil to work you will need to install it first
- pip3 install psutil
- Need to install chattbot lib - pip3 install chatterbot
- pip3 install chatterbot==1.0.4 pytz ---> This is the one that worked...
- Need to install pandas lib - pip install pandas
- pip3 install pandas
- need to install pip3 install gTTS
- install speech pip3 install PyAudio
- brew install portaudio
- pip3 install --upgrade pip setuptools wheel
- /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
- pip3 install SpeechRecognition
- pip3 install requests
- pip3 install beautifulsoup4
- brew install flac
## This file contains main functions as well as test functions
### Includes
- write_log
- CSV File operations
- System info
- ChatPot AI 
- Text to Speech
- Speech to Text
- Weather
- and more to come...
## Issue List
01 - Need to fix reminder function
## Project Road Map
- Reminder and Notifier Apps (work in progress)
- Consolidated web searches
- Web / Mobile app frontend
- Add image recognition (work in progress) [1.0.14]