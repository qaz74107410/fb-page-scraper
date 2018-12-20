import os, time
from scraper import Scraper

# Test User Login Credentials
# Name	
# Carol Albeejehdaiig Warmansen
# User ID	100025505841997
# Login Email	lckpdpk_warmansen_1524446842@tfbnw.net
# Password	uv9rkvofapp

# setting
AUTO_CLOSE = False
FB_ID = "lckpdpk_warmansen_1524446842@tfbnw.net"
FB_PW = "uv9rkvofapp"

sp = None
try:
  sp = Scraper(FB_ID ,FB_PW)

  sp.login()
finally:
  if AUTO_CLOSE : sp.close_driver()