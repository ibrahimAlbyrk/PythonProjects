import os
import json
import pickle
import Memory
import random
import numpy as np

from Alarm import Alarm
from MessageBox import MessageBox
from Mail import Mail

import speech_recognition as sr

import nltk
from nltk.stem import WordNetLemmatizer

from Network import Network

from tensorflow.keras.models import load_model

from playsound import playsound
from termcolor import colored
from gtts import gTTS

lemmatizer = WordNetLemmatizer()
intents = json.loads(open("Data/Brain/Intents/intents.json", encoding="utf-8").read())

words = pickle.load(open("Data/Brain/words.pkl", "rb"))
classes = pickle.load(open("Data/Brain/classes.pkl", "rb"))
model = load_model("Data/Brain/Models/AIAssistant_model.model")

r = sr.Recognizer()

isClosing = False


def clean_up_sentece(sentence):
    sentece_words = nltk.word_tokenize(sentence)
    sentece_words = [lemmatizer.lemmatize(word) for word in sentece_words]
    return sentece_words


def bag_of_words(sentence):
    sentence_words = clean_up_sentece(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)


def predict_class(sentence):
    bow = bag_of_words(sentence)
    _res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, rs] for i, rs in enumerate(_res) if rs > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for rs in results:
        return_list.append({"intent": classes[rs[0]], "probability": str(rs[1])})
    return return_list


def get_response(inttents_list, intents_json):
    result = ""
    tag = inttents_list[0]["intent"]
    list_of_intents = intents_json["intents"]
    for i in list_of_intents:
        if i["tag"] == tag:
            result = random.choice(i["responses"])
            break
    return result


def LoadName():
    with open(Memory.playerNamePath, "r", encoding="utf-8") as f:
        Memory.playerName = f.read()
    with open(Memory.assistantNamePath, "r", encoding="utf-8") as f:
        Memory.assistantName = f.read()


def Write(write_word):
    print(colored(f"{Memory.assistantName} => {write_word}", "blue"))


def RecordMic():
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            voice = r.recognize_google(audio, language="tr-TR")
            return voice
        except Exception:
            return ""


def Response(word, lang="tr"):
    if word.split() == "":
        return
    _word = gTTS(text=word, lang=lang, slow=False)
    _word.save(Memory.audioPath)
    playsound(Memory.audioPath)
    Write(word)
    os.remove(Memory.audioPath)


def Detects(player_input):
    global isClosing
    ints = predict_class(player_input)
    res = get_response(ints, intents)
    Response(res, "tr")

    CloseDetect(res)
    NetworkDetect(res, player_input)
    AlarmDetect(res)
    MailDetect(res)


def AlarmDetect(assistant_output):
    alarm = Alarm()
    alarm.CheckAlarm()
    for word in intents["intents"]:
        if word["tag"] == "alarm kur":
            if assistant_output in word["responses"]:
                alarm = Alarm()
                alarm.SetAlarm()
                Response("Alarm oluşturuldu")
        if word["tag"] == "alarm kontrol":
            if assistant_output in word["responses"]:
                alarm = Alarm()
                alarm.ShowAlarm()


def MailDetect(assistant_output):
    for word in intents["intents"]:
        if word["tag"] == "mail":
            if assistant_output in word["responses"]:
                messageBox = MessageBox()
                mail_adress = messageBox.ShowInputBox()
                Response("mesajınızı giriniz")
                messageBox = MessageBox()
                message = messageBox.ShowInputBox()
                mail = Mail(Memory.quinnMail)
                mail.SendMail(message, mail_adress)
                Response("Mail gönderildi")


def CloseDetect(assistant_output):
    for word in intents["intents"]:
        if word["tag"] == "kapatma":
            if assistant_output in word["responses"]:
                quit()


def NetworkDetect(assistant_output, player_input):
    for word in intents["intents"]:
        if word["tag"] == "youtube":
            if assistant_output in word["responses"]:
                input = player_input.split(" ")
                index = input.index("youtube")
                word = ""
                for i in range(0, index):
                    if word == "":
                        word = input[i]
                    else:
                        word = f"{word} {input[i]}"
                Network.youtubeSearch(word)
                return
        if word["tag"] == "net":
            if assistant_output in word["responses"]:
                input = player_input.split(" ")
                index = input.index("google")
                word = ""
                for i in range(0, index):
                    if word == "":
                        word = input[i]
                    else:
                        word = f"{word} {input[i]}"
                Network.netSearch(word)
                return
        if word["tag"] == "indirme":
            if assistant_output in word["responses"]:
                input = player_input.split(" ")
                index = input.index("indir")
                word = ""
                for i in range(0, index):
                    if word == "":
                        word = input[i]
                    else:
                        word = f"{word} {input[i]}"
                Network.Download(word)
                return
        if word["tag"] == "çeviri":
            if assistant_output in word["responses"]:
                input = player_input.split(" ")
                index = input.index("çevir")
                word = ""
                for i in range(0, index - 1):
                    if word == "":
                        word = input[i]
                    else:
                        word = f"{word} {input[i]}"
                Response(Network.Translate(word, "en"), "en")
                return


def playerInput(mic=False):
    if mic:
        return RecordMic().lower()
    else:
        return input(f"{Memory.playerName} => ").lower()


def errorText(ex):
    print(colored(f"HATA! {ex}", "red"))
    Response("anlayamadım lütfen tekrar söyle", "tr")
