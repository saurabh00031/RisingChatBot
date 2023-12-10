import numpy as np
import pickle
import json
import random
import threading
import pyttsx3
from colorama import init, Fore
from utils import clean_pattern, define_network, bag_of_words
import nltk
nltk.download('punkt')
import openai
import os
import pyttsx3
import speech_recognition as sr
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')



# with open("z.py") as f:
#     exec(f.read())


# you can use print(voices) to see how many voices you have installed
# print(voices[0].id)a
# print(voices[1].id)
# print(voices[2].id)
# print(voices)
for v in voices :
	print("voice : ",v.id)
	
engine.setProperty('voices', voices[1].id)

openai.api_key =""

def speak(audio):
    engine.say(audio)
    print("Speak activated1")
    try:
        if engine._inLoop:
            engine.endLoop()
        engine.runAndWait()
        print("Speak activated2")
        if engine._inLoop:
            engine.endLoop()
        print("Speak activated3")
    except Exception as e :
        print("Error: " , e)
    return

	


def generate_text(prompt):
    model_engine = "text-davinci-002"
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    print("stopped..")
    message = response.choices[0].text.strip()
    print(message)
    speak(message)
    return



with open('saved_variables.pickle', 'rb') as file:
    stemmed_words, tags, ignore_words, X, y = pickle.load(file) 

with open('intents.json') as file:
    data = json.load(file)

init(autoreset=True)
engine = pyttsx3.init()
model = define_network(X, y)
model.load("chatbot_model.tflearn")

# to handle previous context and give advantage to results of that context
def context_func(context, user_input):
	model_input = [bag_of_words(user_input, stemmed_words, ignore_words)]
	results = model.predict(model_input)[0]
	for intent in data['intents']:
		if 'context_filter' in intent:
			if intent['context_filter'] == context:
				# looping through tags and their indices
				for tg_index, tg in enumerate(tags):
					if tg == intent['tag']:
						results[tg_index] += 0.5 
	return results


#######################################################

	

import speech_recognition as sr
import pyttsx3

# Initialize the recognizer
# r = sr.Recognizer()

# Function to convert text to
# speech
def SpeakText(command):
	engine = pyttsx3.init()
	engine.say(command)
	if engine._inLoop:
		engine.endLoop()
	engine.runAndWait()
	if engine._inLoop:
		engine.endLoop()
	return
 

light_on = False




def chat(show_tags_probability= True):
	probability_threshold = 1
	context = ""
	print("Welcome to the intents based chatbot. You can start chatting! (enter 'q' to quit)")
	print("Entered into open")

	y=1
	
	if y==1:
		MyText=""
		r = sr.Recognizer()
		fl=0
		try:
		# use the microphone as source for input.
			with sr.Microphone() as source2:
				print("Hey ask for NLP.... :")

				
				# wait for a second to let the recognizer
				# adjust the energy threshold based on
				# the surrounding noise level
				r.adjust_for_ambient_noise(source2, duration=0.2)
				
				#listens for the user's input
				audio2 = r.listen(source2)
				
				# Using google to recognize audio
				MyText = r.recognize_google(audio2)
				MyText = MyText.lower()

				
				#SpeakText(MyText)
			
		except sr.RequestError as e:
			print("Could not request results; {0}".format(e))
			
		except sr.UnknownValueError:
			print("unknown error occurred")

		user_input = MyText
		print(user_input)
		user_input = user_input.lower()
		if user_input == 'q':
			return 'break'
		# if context from previous response is there, results of that context gets advantage
		if context:
			results = context_func(context, user_input)
		else:
			model_input = [bag_of_words(user_input, stemmed_words, ignore_words)] #as model is trained on 2d array
			results = model.predict(model_input)[0] #gives array of probabilities for all tags
		# to show probabilities given by model for each tags
		if show_tags_probability:
			probability_dict = {}
			for i, j in zip(tags, results):
				probability_dict[i] = j
			print(Fore.GREEN + 'tags_probabilities: {}'.format(probability_dict))
			probability_dict.clear()
		context = "" #reset the context
		result_index = np.argmax(results) #to get index of max probability
		#to filter out predictions below threshold
		print(results[result_index])

		if results[result_index] > probability_threshold: 
			print('hii')
			tag = tags[result_index] #tag associated with user_input according to model predicition
			for intent in data['intents']:
				if intent['tag'] == tag:
					response = random.choice(intent['responses'])
					# check if context is set for current intent
				

					print("nlp response.........................")
					print(response)
					

					if 'context_set' in intent:
						context = intent['context_set']
					break
		else:
			# response = "I didn't understand! Maybe try rephrasing..."
			print("open ai Mode...............................")
			# r = sr.Recognizer()
			# with sr.Microphone() as source:
			# 	print("Hey ask for open ai.... :")
			# 	audio = r.listen(source)
			try:
			# 		text = r.recognize_google(audio)
			# 		print(format(text))
			# 		user_input = format(text)
				prompt = f"Me: {user_input}\nYou:"
				generate_text(prompt)
			
			except Exception as e:
				print(e)
				print("Sorry could not recognize what you said")
				# print("Chatbot: {}".format(response))


chat(True)	
