import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from logger import logger
from fbrequester import FBrequester

# from struct import HTMLstruct

# default setting
DRIVER = webdriver.Firefox()
CLOSE_DELAY = 5 
WAIT_TIME = 2
MAX_RETRY = 5
FB_URL = "https://m.facebook.com"
SCAPE_OPTION = {}
TRAIN_HTML_OPTION = {}
JS_FILENAMES = [
  "jquery-3.3.1.min.js",
  "functions.js"
]

# string value defination
# in case we use Portuguese for easier detection
TXT = {
  "SEARCH" : "Pesquisar"
}

# status
STATUS = {

}

class Scraper(object):

  is_login = False
  is_driveropen = False
  is_trainHTML = False
  is_apiconnect = False

  savefolder = "data"

  HTMLprops = {}

  def __init__(self, driver = DRIVER):
    # setup driver
    self.driver = self.init_driver(driver)

  '''
  DRIVER MANAGER
  '''

  def init_driver(self, custom_driver = None):
    # setup selenium
    driver = custom_driver if custom_driver else DRIVER 
    logger.info("Locating facebook from : {}".format(FB_URL))
    driver.get(FB_URL)
    self.is_driveropen = True
    logger.info("{} init success".format(__name__))
    return driver

  def close_driver(self, delay = CLOSE_DELAY):
    if self.driver :
      logger.info("Closing driver in {} sec".format(str(delay)))
      time.sleep(delay)
      self.driver.quit()
      self.is_driveropen = False
      logger.info("Driver {} closed".format(__name__))
      return True
    return False

  '''
  TRAIN PART
  '''

  def api_connect(self, page_access_token, pageid) :
    fb = FBrequester(page_access_token, pageid)
    if fb.ping() :
      self.fb = fb
      return True
    return False

  def trainHTML(self, options = TRAIN_HTML_OPTION):
    driver = self.driver
    fb = self.fb

    # 
    # part 1 get data from page token by GraphAPI
    # 

    if not fb :
      raise Exception(logger.error("StateException : " + "API not connected. Use api_connect() first."))

    logger.info("Getting fb fanpage feeds...")
    feeds = fb.getFeed()
    fullpath = self.writefile(fb.pretty(feeds), fb.pageid, "txt", surfix = "token")
    logger.info("Saved fb fanpage {}".format(fullpath))

  '''
  APPLIED PART
  '''
  
  def scape(self, page, options = SCAPE_OPTION):
    driver = self.driver
    try:
      logger.info("Scaping fb page \"{}\" using {} ...".format(page, driver.__class__.__module__))
      driver.get(page)
      time.sleep(10)
    except Exception as e:
      raise e

  def login(self, fid, fpw):
    driver = self.driver

    logger.info("logging in Facebook account ...")

    # enter login form
    elem_id = driver.find_element_by_css_selector("input[type='text']")
    elem_pw = driver.find_element_by_css_selector("input[type='password']")
    elem_id.send_keys(fid)
    elem_pw.send_keys(fpw)
    elem_pw.submit()
    self.wait_until_redirect(driver.current_url)

    # force back to home url incase fb ask to another login solution
    driver.get(FB_URL)

    # check if page is ready
    # if "search" exist
    self.wait_until(By.XPATH , "(//*[contains(text(), '" + TXT["SEARCH"] + "')] | //*[@value='" + TXT["SEARCH"] + "'])")
    self.is_login = True
    logger.info("Login Successful")
    return True
    
  '''
  DRIVER HELPER
  '''
    
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

  def wait_until_redirect(self, fromurl = None, maxretry = MAX_RETRY, delay = WAIT_TIME):
    driver = self.driver
    fromurl = fromurl if fromurl else driver.current_url
    retry = 0

    while True:
      try:
        WebDriverWait(driver, delay).until(EC.url_changes(fromurl))
        return True
      except TimeoutException as e:
        if retry < maxretry :
          retry += 1
        else :
          raise e

  def injectJS(self , filenames = None):
    if filenames :
      # logger.info("Injecting javascript file")
      for filename in filenames :
        try:
          with open(filename, 'r') as jsfile:
            js = jsfile.read()
            self.driver.execute_script(js)
            # logger.info("Injected {}".format(filename))
        except Exception as e:
          # raise e
          logger.warning("Unable to inject {}".format(filename))
      return True
    return False

  def writefile(self, data, filename, filetype, prefix = None, surfix = None, folder = None) : 
    folder = folder if folder else self.savefolder

    path = os.path.join(os.getcwd(), folder)
    path = path + "/"
    if prefix :
      path = path + prefix + "_"
    path = path + filename
    if surfix :
      path = path + "_" + surfix
    path = path + "." + filetype

    with open(path, "w+") as file :
      file.write(data)
    return path

  