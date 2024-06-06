##################################################
# Main Application for Launching Lucy AI ChatBot #
# Version 1.0.1.14 - Released 2024-06-04         #
# Author - Lawrence Lutton                       #
##################################################

from Default_Functions import *
import ImageReconition

write_log(Message='Starting Main Application', FuncName='Main', ErrorType='Info')

# lucy()
# gui()
# lucy_gpt_chat()
# search_google()
# ImageReconition.learning_video_cap()
# ImageReconition.stop_sign_recognition(image=f"{image}")

telegram_ai_chatbot()

write_log(Message='Closing Main Application', FuncName='Main', ErrorType='Info')
