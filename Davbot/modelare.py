import nltk
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()


import numpy
import tflearn
import tensorflow
import random


import json
import pickle
from gtts import gTTS
import os
import speech_recognition as sr
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from playsound import playsound
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QPixmap
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"





r = sr.Recognizer()
limba = 'ro'

with open("intents.json") as file:
    file = open("intents.json", "r", encoding='utf-8')
    data = json.load(file)

try:
    with open("Model/data.pickle", "rb") as f:
        words, labels, antrenament, output = pickle.load(f)

except:

    words = []
    labels = []
    docs_x = []
    docs_y = []


    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            cuv = nltk.wordpunct_tokenize(pattern)
            words.extend(cuv)
            docs_x.append(cuv)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w !="?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    antrenament = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x , doc in enumerate(docs_x):
        bag = []

        cuv = [stemmer.stem(w) for w in doc]

        for w in words:
            if w in cuv:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        antrenament.append(bag)
        output.append(output_row)

    antrenament = numpy.array(antrenament)
    output = numpy.array(output)

    with open("Model/data.pickle", "wb") as f:
        pickle.dump((words, labels, antrenament , output), f)



tensorflow.reset_default_graph()

net = tflearn.input_data(shape =[None, len(antrenament[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)



try:
    model = tflearn.DNN(net)
    model.load("Model/model.tflearn")


except:

    model = tflearn.DNN(net)
    model.fit(antrenament, output, n_epoch= 5000, batch_size=8, show_metric=True)
    model.save("Model/model.tflearn")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i,w in enumerate(words):

            if w == se:
                bag[i] = 1

    return numpy.array(bag)



def diacritice(cuvant):

    cuvant = cuvant.replace("Ä‚", "Ă")
    cuvant = cuvant.replace("Äƒ", "ă")
    cuvant = cuvant.replace("Ã‚", "Â")
    cuvant = cuvant.replace("Ã¢", "â")
    cuvant = cuvant.replace("ÃŽ", "Î")
    cuvant = cuvant.replace("Ã®", "î")
    cuvant = cuvant.replace("Åž", "Ş")
    cuvant = cuvant.replace("ÅŸ", "ş")
    cuvant = cuvant.replace("Èš", "Ț")
    cuvant = cuvant.replace("È›", "ț")

    return cuvant






