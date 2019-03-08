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

# 
# Scrapper Setting
# 

AUTO_CLOSE = False

# 
# Facebook Setting
# 

# FB_ID = "lckpdpk_warmansen_1524446842@tfbnw.net"
# FB_PW = "uv9rkvofapp"
FB_PAGE_URL = "https://m.facebook.com/glassesgirlXD" # glasses girl -w-

# page token change often
FB_PAGE_TOKEN = "EAAH6eMcvEDgBADQLibvxFXZCHMWUF3hoZAM71SHPBZCKHFeLCfICNyoQsXKn7rG9ZATQXeiw8Mb6qNyE9hZAhhRdWvWloy24VQnxFTCwFgWFVPnBolcDZBIjodIOBGJWEgD7EDVwAvYwylLUlhgKLWw74sZBNNA5wNqlde6s7CziMhnZAF59bSLfrZA0uoHfbHnAZD"
FB_PAGE_ID = "1224164271050249"

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
  
  success = sp.login(FB_ID ,FB_PW)
  if not success :
    raise Exception(logger.error("Facebook login unsucessful : make sure user and password correct and swicth langugese" ))

  sp.api_connect(FB_PAGE_TOKEN, FB_PAGE_ID)
  
  # need train first
  # sp.scape(FB_PAGE_URL)
finally:
  if AUTO_CLOSE : sp.close_driver()