import os, time
import getpass
from scraper import Scraper
from logger import logger

# 
# Scrapper Setting
# 

AUTO_CLOSE = False

# 
# Facebook Setting
# 

# FB_ID = "lckpdpk_warmansen_1524446842@tfbnw.net"
# FB_PW = "uv9rkvofapp"
FB_PAGE_TARGET = "https://m.facebook.com/glassesgirlXD" # glasses girl -w-

# page token change often
# you can get it here : https://developers.facebook.com/tools/explorer
FB_PAGE_TOKEN = "EAAH6eMcvEDgBAIcVMfiZAQZATDFmF86h2zHiE8xZAxrZCghPcUrbeZAQ3IdhPhHZCfZAjjGINkjZAd414Hfl2wrTgOTIWMUEu1RXdP1Cr2mWAlnLp7tdtwnMEbZBmfgVUeZB0DwLx6t1C7uHpF8075ASDvrk6E0ZAVqthpvELKfLCk3pNxAZATr1HbM42EY72GzbzHKm9cZCJqo6mzLVjJzb5Whnd"
FB_PAGE_ID = "1224164271050249"
FB_PAGE_URL = "https://m.facebook.com/SHOP-GRADE-A-1224164271050249"
FB_PAGE_NAME = ""

# Save directory
FILE_DIR = "data"

def main():

  sp = None
  try:
    sp = Scraper()

    # enter Facebook accout
    # FB_ID = input("Enter your Facebook ID : ")
    FB_ID = "Suthiwatsangsuwan@Hotmail.com" # lazy debug
    print("Using Facebook ID : {}".format(FB_ID))
    FB_PW = getpass.getpass("Enter your Facebook password (shown as blank) : ")
    
    sp.login(FB_ID ,FB_PW)

    # need train first
    sp.api_connect(FB_PAGE_TOKEN, FB_PAGE_ID)
    sp.trainHTML(FB_PAGE_URL)

  finally:
    if AUTO_CLOSE : sp.close_driver()

if __name__ == "__main__" : 
  main()