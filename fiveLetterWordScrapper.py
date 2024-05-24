#import the usual
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time 
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import JavascriptException
from pathlib import Path
import random as rand
import pyautogui

#just gets rid of the ad unless the ad dosen't exist
def check_exists_by_xpath_ad(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException or JavascriptException:
        return False
    return driver.execute_script(f"document.getElementById('{'ad-top'}').remove();")

#usual with selenium
url = "https://www.nytimes.com/games/wordle/index.html"
driver = webdriver.Firefox()
driver.maximize_window()
driver.get(url)

#hits both of the play buttons and checks if ad exist

wait = WebDriverWait(driver, 15)
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='Play']"))).click()           
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "svg[data-testid='icon-close']"))).click() 
check_exists_by_xpath_ad('//*[@id="ad-top"]') 

#picks a random five letter word out of all five letter words 
fiveWordList = []
with open(Path.cwd() / 'fiveWordList.txt', 'r') as wordList:
  reader = wordList.read().splitlines()
  fiveWordList.append(reader)
fiveWordList = fiveWordList[0]
randomWord = rand.choice(fiveWordList)

open(Path.cwd() / 'something.txt', 'w').close()
something = open(Path.cwd() / 'something.txt', 'a')

#things to set
letterCheckerDict = {'correct' : ['', '', '', '', ''], 'absent' : set(), 'present' : set()}
tries = 0
removeSameSpot = set()

time.sleep(1)
#loop starts
while '' in letterCheckerDict['correct'] and tries != 6:
  time.sleep(1)
  for letter in randomWord:
    pyautogui.write(letter, .25)
  pyautogui.write(['enter'])

  gameRows = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'Board-module_board__jeoPS')))
  gameKeys = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'Tile-module_tile__UWEHN')))[tries * 5:(tries * 5) + 5]
  time.sleep(2)

  PresentArr = []
  indexOfGameKey = 0
  #correct data structures
  for value in gameKeys:
    if value.get_attribute('data-state') == 'correct':
      if value.text.lower() in letterCheckerDict['absent']:
        letterCheckerDict['absent'].remove(value.text.lower())
      letterCheckerDict['correct'][indexOfGameKey] = value.text.lower()
    if value.get_attribute('data-state') == 'present':
      letterCheckerDict['present'].update(value.text.lower())
      PresentArr.append(value.text.lower())
    else:
       PresentArr.append(' ')
    if value.get_attribute('data-state') == 'absent':
      if value.text.lower() not in letterCheckerDict['correct'] and value.text.lower() not in letterCheckerDict['present']:
        letterCheckerDict['absent'].update(value.text.lower())

    
    indexOfGameKey += 1

  something.write(str(PresentArr))
  something.write('\n\n\n')
  #checks which values meet requirements    
  newfiveWordList = []
  for word in fiveWordList:
      is_valid = True
      for ind, char in enumerate(letterCheckerDict['correct']):
          if char and word[ind] != char:
              is_valid = False
              break
          
      for char in (letterCheckerDict['absent']):
          if char in word:
            is_valid = False
            break
          
      for char in (letterCheckerDict['present']):
          if char not in word:
            is_valid = False
            break
          else:
            for ind in range(len(PresentArr)):
               if word[ind] == PresentArr[ind]:
                  removeSameSpot.add(word)
                  is_valid = False

              
      if is_valid and word not in removeSameSpot:
          newfiveWordList.append(word)

  something.write(str(removeSameSpot))
  something.write('\n\n\n')
  something.write(str(letterCheckerDict))
  something.write('\n\n\n')
  if len(newfiveWordList) > 1 and randomWord in newfiveWordList:
     newfiveWordList.remove(randomWord)

  randomWord = rand.choice(newfiveWordList)
  tries += 1

wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "svg[data-testid='icon-close']"))).click()           
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "svg[data-testid='icon-close']"))).click() 

#if u want to close at the end or not
#driver.close()