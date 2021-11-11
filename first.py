import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from logger import *
import random
import threading

logger = set_logger(__name__)

def start_chrome():
    user_agent = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    ]
    UA = user_agent[random.randrange(0, len(user_agent), 1)]
    global option
    option = Options()  
    option.add_argument('--user-data-dir=' + os.path.join(os.getcwd(),"profile1"))    
    option.add_argument('--lang=ja-JP')
    option.add_argument('--user-agent=' + UA)
    option.add_argument('--ignore-certificate-errors')
    option.add_argument('--ignore-ssl-errors')
    option.add_argument("window-size=1000,800")
    global driver
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=option)   
    driver.get("https://auctions.yahoo.co.jp/jp/show/submit?category=0")
    time.sleep(300)

def start_chrome2():
    user_agent = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    ]
    UA = user_agent[random.randrange(0, len(user_agent), 1)]
    global option2
    option2 = Options() 
    option2.add_argument('--user-data-dir=' + os.path.join(os.getcwd(),"profile2"))    
    option2.add_argument('--lang=ja-JP')
    option2.add_argument('--user-agent=' + UA)
    option2.add_argument('--ignore-certificate-errors')
    option2.add_argument('--ignore-ssl-errors')
    option2.add_argument("window-size=1000,800")
    global driver2
    driver2 = webdriver.Chrome(ChromeDriverManager().install(),options=option2)   
    driver2.get("https://auctions.yahoo.co.jp/jp/show/submit?category=0")
    time.sleep(300)
def start_chrome3():
    user_agent = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    ]
    UA = user_agent[random.randrange(0, len(user_agent), 1)]
    global option3
    option3 = Options() 
    option3.add_argument('--user-data-dir=' + os.path.join(os.getcwd(),"profile3"))    
    option3.add_argument('--lang=ja-JP')
    option3.add_argument('--user-agent=' + UA)
    option3.add_argument('--ignore-certificate-errors')
    option3.add_argument('--ignore-ssl-errors')
    option3.add_argument("window-size=1000,800")
    global driver3
    driver3 = webdriver.Chrome(ChromeDriverManager().install(),options=option3)   
    driver3.get("https://auctions.yahoo.co.jp/jp/show/submit?category=0")
    time.sleep(300)

def main():
    t1 = threading.Thread(target=start_chrome)
    t2 = threading.Thread(target=start_chrome2)
    t3 = threading.Thread(target=start_chrome3)
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()

if __name__ == "__main__":
    main()