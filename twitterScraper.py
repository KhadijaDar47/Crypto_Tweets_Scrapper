import os
import re
import psutil
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 
import time 
import csv

def search_file(file_name, search_path):
    for root, dirs, files in os.walk(search_path):
        if file_name in files:
            return os.path.join(root, file_name)
    return None

def TwitterScraper(pTag,coin):
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 'chrome.exe':
                proc.kill()
        options = webdriver.ChromeOptions()
        file_name  = "chrome.exe"
        search_path = "C:\\"
       
        file_path = search_file(file_name, search_path)
        options.add_argument("--start-maximized")
        username = os.getlogin()
        user_data_dir = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\"
        options.add_argument("user-data-dir=" + user_data_dir)
        options.add_argument("--disable-extensions") 
        options.binary_location = file_path

        options.add_argument("user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'")
        options.add_argument("Accept-Language=en-US, en;q=0.5")
      
        prefs = {"profile.default_content_setting_values.notifications": 2}
        bot = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        time.sleep(5)
        bot.get("https://twitter.com/home")
        time.sleep(10)
   

        try:
            search_input = WebDriverWait(bot, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input'))
            )
            search_input.send_keys(pTag)
            search_input.send_keys(Keys.RETURN)

            time.sleep(10)
            tweet_data = []
            tweet_ids = set()
            last_position = bot.execute_script("return window.pageYOffset;")
        

            reached_end = False  # Flag to track if the end of the page is reached
            
            while not reached_end:
                # Check if new cards are loaded
                try:
                    if WebDriverWait(bot, 10).until(EC.presence_of_element_located((By.XPATH, '//article[@data-testid="tweet"]'))):
                        cards = bot.find_elements(By.XPATH, '//article[@data-testid="tweet"]')
                except Exception as e:
                  print("\033[31mNo Data found in your time range.\033[0m")
                  break
                
                
                if len(cards) > 0:
                    # Process the new cards
                    for card in cards[-15:]:
                        data = get_tweet_data(card)
                        if data:
                            tweet_id = ''.join(data)
                            if tweet_id not in tweet_ids:
                                tweet_ids.add(tweet_id)
                                tweet_data.append(data)
                else:
                    raise NoSuchElementException('No cards were found')

                # Scroll down
                bot.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(4)
                currentPosition = bot.execute_script("return window.pageYOffset;")
                
                if last_position == currentPosition:
                    time.sleep(2)  # Wait for a while to check if it has reached the end
                    new_position = bot.execute_script("return window.pageYOffset;")
                    if last_position == new_position:
                        reached_end = True  # Stop scrolling if no change in position after waiting
                        print("\033[34mReached the end of scrolling.\033[0m")

                else:
                    last_position = currentPosition

                    
            save_data(tweet_data,coin)
        except Exception as e:
           print(e)
           print("\033[31mYou are not logged in to your twitter account on web")
 
       
def get_tweet_data(card):
        # username , getting the first span tag after the current tag
        username = card.find_element(By.XPATH,'.//span').text 
        # print("Username: " + username + "\n")
        # twitter handle 
        handle = card.find_element(By.XPATH,'.//span[contains(text(),"@")]').text 
        # print("Twitter Handle: " + handle + "\n")
        # post date 
        try:
            postDate = card.find_element(By.XPATH,'.//time').get_attribute('datetime')
            # print("Post Date: " + postDate + "\n")
        except NoSuchElementException:
            return
        responding = card.find_element(By.CLASS_NAME, 'css-1dbjc4n').text
        responding = responding.replace('\n', ' ').strip()
        responding = re.sub(r'\b\d+\b', '', responding)

        # Remove extra spaces resulting from number removal
        responding = ' '.join(responding.split())
        # print("Cleaned Responding: " + responding)

        # retweet 
        retweets = card.find_element(By.CSS_SELECTOR,'div[data-testid="retweet"]').text
        # print("Retweets: " + retweets + "\n")

        # likes 
        likes = card.find_element(By.CSS_SELECTOR,'div[data-testid="like"]').text
        # print("Likes: " + likes + "\n")
        
        tweet = (username,handle,postDate,responding,retweets,likes)
        return tweet
      
def save_data(tweet_data,coin):    
        # saving the tweet 
        with open(f"Files\\{coin}.csv",'w',newline='', encoding='utf-8') as f:
            header = ['Username','TwitterHandle','Date','Tweet','Retweets','Likes']
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(tweet_data)



    



