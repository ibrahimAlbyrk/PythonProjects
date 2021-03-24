import pyautogui

from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class FastFingersBot:
    driver = None
    words= None
    waitTime = 0
    i = 0
    def __init__(self,waitTime = 0):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.waitTime = waitTime
        self.driver = webdriver.Chrome("Drivers/chromedriver.exe",chrome_options=options)

    def Start(self):
        self.driver.get("https://www.onparmak.org/klavye-hiz-testi")
        enter = self.driver.find_element_by_xpath("/html/body/main/div[2]/div[3]/div[1]/div[1]/div[4]/div[2]/input")
        enter.send_keys(Keys.ENTER)
        while 1:
            try:
                self.words = self.driver.find_element_by_id("display")
                word = self.words.find_element_by_id(self.i).text
            except Exception: break
            enter.send_keys(word)
            enter.send_keys(Keys.SPACE)
            self.i += 1
            sleep(self.waitTime)
        print("work Completed")
        
bot = FastFingersBot(waitTime=0.1)
bot.Start()
