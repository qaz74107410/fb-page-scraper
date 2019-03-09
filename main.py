import os, time
import getpass
from scraper import Scraper
from logger import logger

# Test User Login Credentials
# Name	

# Carol Albeejehdaiig Warmansen
# User ID	100025505841997
# Login Email	lckpdpk_warmansen_1524446842@tfbnw.net
# Password	uv9rkvofapp
# https://www.facebook.com/settings?tab=language&section=account&view

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
FB_PAGE_TOKEN = "EAAH6eMcvEDgBANjh7fLFmqo9ayekkZCN99TgQzXlZAJ1BZA6PYMZAxl19mIfshYsV6TZB0pPR5NrVBjWLoAust2HBZBZCH8QI3BnuI7jfJN1w7JQQK3y3ETOZBQ5j5CjF3Epm9CzNqhoGWzS2JkHBqXW66ZBJiOYkyytRDJq5IsvSXbBwoMq4sXPYVZBM6Wmz4cr6KTjaMQmXSywZDZD"
FB_PAGE_ID = "1224164271050249"
FB_PAGE_URL = "https://m.facebook.com/SHOP-GRADE-A-1224164271050249"
FB_PAGE_NAME = ""

# Save directory
FILE_DIR = "data"

# scaper
sp = None
try:
  sp = Scraper()

  # enter Facebook accout
  # FB_ID = input("Enter your Facebook ID : ")
  FB_ID = "Suthiwatsangsuwan@Hotmail.com"
  print("Using Facebook ID : {}".format(FB_ID))
  FB_PW = getpass.getpass("Enter your Facebook password : ")
  
  sp.login(FB_ID ,FB_PW)

  # need train first
  sp.api_connect(FB_PAGE_TOKEN, FB_PAGE_ID)
  sp.trainHTML(FB_PAGE_URL)
  
finally:
  if AUTO_CLOSE : sp.close_driver()