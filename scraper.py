import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from logger import logger

# default setting
DRIVER = webdriver.Firefox()
CLOSE_DELAY = 5
WAIT_TIME = 2
MAX_RETRY = 3
FB_URL = "https://m.facebook.com"

# string value defination
# in case we use Portuguese for easier detection
TXT = {
  "SEARCH" : "Pesquisar"
}

class Scraper(object):

  def __init__(self, fb_id, fb_pw, driver = DRIVER):
    # setup facebook
    self.fb = {"id" : fb_id, "pw" : fb_pw}
    self.driver = self.init_driver(driver)

  def init_driver(self, custom_driver = None):
    # setup selenium
    driver = custom_driver if custom_driver else DRIVER 
    logger.info("locating facebook from : {}".format(FB_URL))
    driver.get(FB_URL)
    logger.info("{} init success".format(__name__))
    return driver

  def close_driver(self, delay = CLOSE_DELAY):
    if self.driver :
      logger.info("closing driver in {} sec".format(str(delay)))
      time.sleep(delay)
      self.driver.quit()
      logger.info("driver {} closed".format(__name__))
      return True
    return False
  
  def scape(self, page, options):
    # TODO : need loging first
    driver = self.driver
    try:
      
      # login
      
      logger.info("Scaping fb page \"{}\" using {}".format(page, driver.__class__.__module__))
    except Exception as e:
      raise e
    finally:
      driver.quit()

  def wait_until(self, by, condition, maxretry = MAX_RETRY, delay = WAIT_TIME):
    driver = self.driver
    retry = 0

    while True:
      try:
        # WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((by, condition)))
        return True
      except TimeoutException as e:
        if retry < maxretry :
          retry += 1
        else :
          raise e

  def login(self):
    driver = self.driver  
    fid = self.fb.get("id")
    fpw = self.fb.get("pw")
    try:
      # enter login form
      elem_id = driver.find_element_by_css_selector("input[type='text']")
      elem_pw = driver.find_element_by_css_selector("input[type='password']")
      elem_id.send_keys(fid)
      elem_pw.send_keys(fpw)
      elem_pw.submit()
      driver.implicitly_wait(3)
      # force back to home url incase fb ask to another login solution
      driver.get(FB_URL)
      # check if page is ready
      self.wait_until(By.XPATH , "(//*[contains(text(), '" + TXT["SEARCH"] + "')] | //*[@value='" + TXT["SEARCH"] + "'])")
    except Exception as e:
      raise e