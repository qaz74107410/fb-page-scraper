import time
import os
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from logger import logger
from fbrequester import FBrequester

# from struct import HTMLstruct

# default setting
USER_AGENT = "Opera/9.80 (J2ME/MIDP; Opera Mini/5.1.21214/28.2725; U; ru) Presto/2.8.119 Version/11.10"
FF_PROFILE = webdriver.FirefoxProfile()
FF_PROFILE.set_preference("general.useragent.override", USER_AGENT)
DRIVER = webdriver.Firefox(FF_PROFILE)
CLOSE_DELAY = 5 
WAIT_TIME = 2
MAX_RETRY = 5
FB_URL = "https://m.facebook.com"
SCAPE_OPTION = {}
TRAIN_HTML_OPTION = {}
JS_FILENAMES = [
  "jquery-3.3.1.min.js",
  "scraper-functions.js"
]

# string value defination
# in case we use Portuguese for easier detection
TXT = {
  "SEARCH" : "Pesquisar",
  "MORE_POST" : "Mostrar mais",
  "LIKE" : "Gosto",
  "COMMENT" : "comentário"
  # "COMMENT" : "coment"
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

  patterns = None

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
    logger.info("Connecting fb API...")
    fb = FBrequester(page_access_token, pageid)
    if fb.ping() :
      self.fb = fb
      self.is_apiconnect = True
      logger.info("Connected")
      return True
    logger.warning("Connection failed : " + fb.checkToken().get("error").get("message"))
    return False

  def trainHTML(self, train_pag_url, options = TRAIN_HTML_OPTION):
    driver = self.driver

    if not self.is_apiconnect :
      raise Exception(logger.error("StateException : " + "API not connected. Use api_connect() first or check your page token."))
    fb = self.fb

    #  
    # part 1 get data from page token by GraphAPI
    # 

    logger.info("Getting fb fanpage feeds...")
    feeds = fb.getFeed()
    fullpath = self.writefile(fb.pretty(feeds), fb.pageid, "txt", surfix = "token")
    logger.info("Saved fb fanpage data from token at : {}".format(fullpath))

    # 
    # part 2 get each post blocks 
    # 

    logger.info("Locate for trainning from fb fanpage : {}".format(train_pag_url))
    driver.get(train_pag_url)
    fbpage_name = self.fb.getName()

    self.wait_until(By.XPATH , "(//*[contains(text(), '" + fbpage_name + "')] | //*[@value='" + fbpage_name + "'])")
    logger.info("Getting fb fanpage blocks by expanding name method...")

    is_more_post = True
    postblocks = []

    try:
      while is_more_post:
        try:
          self.injectJS(JS_FILENAMES)
          # Getting post by javascript
          # Scraper.findPostBlocks(facebookpagename, likebuttonname)
          js = "return Scraper.findPostBlocks('{}', '{}')".format(fbpage_name, TXT["LIKE"])
          # print(js)
          postblocks_per_page = driver.execute_script(js)  
          for pb in postblocks_per_page:
            postblocks.append(pb.get_attribute('innerHTML'))

          morepost_link = driver.find_element_by_link_text(TXT["MORE_POST"])
          before_url = driver.current_url
          morepost_link.click()
          self.wait_until_redirect(before_url)
        except NoSuchElementException as e:
          is_more_post = False
        except TimeoutException as e :
          raise e
    finally:
      fullpath = self.writefile(str(postblocks), fb.pageid, "txt", surfix = "html")
      logger.info("Saved fb fanpage tag from HTML scraper at : {}".format(fullpath))


    # 
    # part 3 analysis each post block with data from page token
    # 

    # how to find "data" by walk down in html node
    patterns = []
    seperator = " > "

    for pb, f in zip(postblocks, feeds):
      pattern = {}
      driver.execute_script("return Scraper.clearbody()")
      driver.execute_script("return Scraper.html(`{}`)".format(pb))

      # if have messages
      msg = f.get("message")
      msgresult = driver.execute_script("return Scraper.findTxt(`{}`, `{}`)".format('body', msg))
      if len(msgresult.get("elem")) :
        elems = msgresult.get("elem")
        elems.reverse()
        pattern["msg"] = seperator.join(elems)

      # if have pictures
      imgsresult = driver.execute_script("return Scraper.findImgTags(`{}`)".format('body'))
      if imgsresult.get("found") :
        pattern["pics"] = []
        for elems in imgsresult.get("elems") :
          elems.reverse()
          pattern["pics"].append(seperator.join(elems))

      # if have likes
      likeresult = driver.execute_script("return Scraper.findLikeCount(`{}`, `{}`)".format('body', TXT["LIKE"]))
      if len(likeresult.get("elem")) :
        elems = likeresult.get("elem")
        elems.reverse()
        pattern["like"] = seperator.join(elems)

      # if have comments
      commentsresult = driver.execute_script("return Scraper.findCommentCount(`{}`, `{}`)".format('body', TXT["COMMENT"]))
      if len(commentsresult.get("elem")) :
        elems = commentsresult.get("elem")
        elems.reverse()
        pattern["comment"] = seperator.join(elems)

      patterns.append(pattern)

    self.patterns = patterns
    
    fullpath = self.writefile(str(patterns), fb.pageid, "txt", surfix = "pattern")
    logger.info("Saved fb fanpage pattern from analysis scraper at : {}".format(fullpath))

  '''
  APPLIED PART
  '''
  
  def scape(self, page, options = SCAPE_OPTION):
    driver = self.driver
    custompatterns = SCAPE_OPTION.get("patterns")
    patterns = custompatterns if custompatterns else self.patterns 
    logger.info("Scaping fb page \"{}\" using {} ...".format(page, driver.__class__.__module__))
    driver.get(page)
    time.sleep(10)

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
    try:
      self.wait_until(By.XPATH , "(//*[contains(text(), '" + TXT["SEARCH"] + "')] | //*[@value='" + TXT["SEARCH"] + "'])")
    except TimeoutException as e:
      logger.error("Facebook login unsucessful : make sure user and password correct and swicth langugese")
      raise e
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

  def randdelay(self, min, max):
    time.sleep(random.randint(min,max))

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

    with open(path, "w+", encoding="utf-8") as file :
      file.write(data)
    return path
  
    def appendfile(self, data, filename, filetype, prefix = None, surfix = None, folder = None) : 
      folder = folder if folder else self.savefolder

      path = os.path.join(os.getcwd(), folder)
      path = path + "/"
      if prefix :
        path = path + prefix + "_"
      path = path + filename
      if surfix :
        path = path + "_" + surfix
      path = path + "." + filetype

      with open(path, "a+", encoding="utf-8") as file :
        file.write(data)
      return path

  def dictContain(self, d, targetkey, node = None) :
    if node == None :
      node = []
    if type(d) == type({}) :
      for key in d :
        if key == targetkey :
          node.append(key)
          return True , node
        nestfound, _ = self.dictContain(d.get(key), targetkey, node)
        if nestfound :
          node.append(key)
          return True, node
    return False, None
