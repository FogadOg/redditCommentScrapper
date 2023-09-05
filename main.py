from bs4 import BeautifulSoup
from selenium import webdriver
import keyboard 
import requests
import time
import re
import csv


urls=[
    "https://en.wikipedia.org/wiki/United_States",
    "https://en.wikipedia.org/wiki/Reddit",
    "https://en.wikipedia.org/wiki/Internet_culture",
]


class WaitForKeyPress():
    def _waitForKeyPress(self):
        keyboard.wait('esc')


class Scrape(WaitForKeyPress):
    def __init__(self, url) -> None:        
        self.url=url

    def startScrapingWebsite(self):
        page=self._sendRequestToMainPage(self.url)
        text=self._getTextDataFromWebsite(page)
        saveData=CreateCsvData(20,text)
        saveData.CreateTextSequancesWithWindow()

    def _sendRequestToMainPage(self,url):
        response=requests.get(url)
        # dr = webdriver.Chrome()
        # dr.get(url)
        # self._waitForKeyPress()
        page = BeautifulSoup(response.content,"html.parser")
        return page

    def _getTextDataFromWebsite(self,page)->list:
        textDataset=[]
        textData=page.find_all("div","mw-parser-output")

        for sentance in textData:
            for paragraph in sentance.find_all("p"):
                textDataset.append(paragraph.text)
        return "".join(textDataset)


class CreateCsvData():
    def __init__(self, windowSize, textSequance):
        self.windowSize=windowSize
        self.textSequance=textSequance

    def cleanText(self,sen):
        # Remove punctuations and numbers
        sentence = re.sub('[^a-zA-Z]', ' ', sen)

        # Single character removal
        sentence = re.sub(r"\s+[a-zA-Z]\s+", ' ', sentence)

        # Removing multiple spaces
        sentence = re.sub(r'\s+', ' ', sentence)

        return sentence.lower()[1:-2]

    def CreateTextSequancesWithWindow(self):
        cleanedText=self.cleanText(self.textSequance)
        textSplitBySpace=cleanedText.split(" ")
        sequanceLength=len(textSplitBySpace)
        
        preiviusSentance=None
        for i in range(sequanceLength-self.windowSize):
        
            textSequance=textSplitBySpace[i:i+self.windowSize]
            currentSentance=" ".join(textSequance)
            if preiviusSentance!=None:
                with open(f'preTrainingData.csv', 'a', encoding='UTF8') as f:
                    writer = csv.writer(f)
                    writer.writerow([preiviusSentance,currentSentance])
            preiviusSentance=currentSentance


for url in urls:
    Scrape(url).startScrapingWebsite()




