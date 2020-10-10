#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import render_template
import os
from os import path
app = Flask(__name__)
import speech_recognition as sr
from datetime import datetime
audioRecog = 0
import time
global messageList
messageList = []

global messageCounter
messageCounter = 0
@app.route("/", methods=['POST', 'GET'])

def index():
    global audioRecog
    if request.method == "POST":
        f = request.files['audio_data']
        with open('audio.wav', 'wb') as audio:
            f.save(audio)
        print('file uploaded successfully')
        audioFile = path.join(path.dirname(path.realpath(__file__)), "audio.wav")
        r = sr.Recognizer()
        with sr.AudioFile(audioFile) as source:
            audio = r.record(source)  # read the entire audio file
        try:
            print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
            audioRecog = r.recognize_google(audio)
            audioRecogList = audioRecog.split()
            print(audioRecogList)
            if audioRecogList[0] + audioRecogList[1] == "goforward":
                messageList.append("Google Speech Recognition thinks you said '" + audioRecog + "' so the robot went forward for " + audioRecogList[2] + " seconds.")
                print("Go forward for " + audioRecogList[2] + " seconds")
                os.system('sudo python2 leftf.py ' + audioRecogList[2] + ' &')
                os.system('sudo python2 right.py ' + audioRecogList[2] + ' &')
            if audioRecogList[0] + audioRecogList[1] == "goback":
                messageList.append("Google Speech Recognition thinks you said '" + audioRecog + "' so the robot went backwards for " + audioRecogList[2] + " seconds.")
                print("Go back for " + audioRecogList[2] + " seconds")
                os.system('sudo python2 leftb.py ' + audioRecogList[2] + ' &')
                os.system('sudo python2 rightb.py ' + audioRecogList[2] + ' &')
            if audioRecogList[0] + audioRecogList[1] == "turnleft":
                messageList.append("Google Speech Recognition thinks you said '" + audioRecog + "' so the robot turned left.")
                print("turn left")
                os.system('sudo python2 right.py 5 &')
            if audioRecogList[0] + audioRecogList[1] == "turnright":
                messageList.append("Google Speech Recognition thinks you said '" + audioRecog + "' so the robot turned right.")
                print("turn right")
                os.system('sudo python2 leftf.py 5 &')
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            audioRecog = "Audio could not be understood."
            mesageList.append(audioRecog)
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            audioRecog = "Error!"
            messageList.append(audioRecog)
        return render_template('index.html', request="POST")
    else:
        return render_template("index.html")
@app.route('/text_stream')
def stream():
    def generate():
        while True:
            global messageCounter
            if not messageList:
                continue
            if len(messageList) == messageCounter:
                continue
            if len(messageList) != messageCounter:
                print(len(messageList), messageCounter)
                messageCounter = messageCounter + 1
                yield '{}\n'.format(messageList[-1])
            

    return app.response_class(generate(), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True, ssl_context='adhoc')
