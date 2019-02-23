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

# default setting
AUTO_CLOSE = False
# FB_ID = "lckpdpk_warmansen_1524446842@tfbnw.net"
# FB_PW = "uv9rkvofapp"
FB_PAGE_URL = "https://m.facebook.com/glassesgirlXD" # glasses girl -w-

# scaper
sp = None
try:
  sp = Scraper()

  # enter Facebook accout
  # FB_ID = input("Enter your Facebook ID : ")
  FB_ID = "xocalasad@khtyler.com"
  print("Using Facebook ID : {}".format(FB_ID))
  FB_PW = getpass.getpass("Enter your Facebook password : ")
  
  sp.login(FB_ID ,FB_PW)
  sp.scape(FB_PAGE_URL)
finally:
  if AUTO_CLOSE : sp.close_driver()