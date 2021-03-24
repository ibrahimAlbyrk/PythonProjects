import pyautogui
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

i = 0


def write(word):
    pyautogui.write(word)
    pyautogui.press("space")


driver = webdriver.Chrome("Drivers/chromedriver.exe")
driver.fullscreen_window()
driver.get("https://www.onparmak.org/klavye-hiz-testi")
enter = driver.find_element_by_xpath("/html/body/main/div[2]/div[3]/div[1]/div[1]/div[4]/div[2]/input")
enter.send_keys(Keys.ENTER)
while 1:
    words = driver.find_element_by_id("display")
    word = words.find_element_by_id(i).text
    print(word)
    enter.send_keys(word)
    enter.send_keys(Keys.SPACE)
    i += 1
