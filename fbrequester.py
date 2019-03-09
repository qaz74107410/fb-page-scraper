import requests
import json
from logger import logger

FB_GRAPH_URL = "https://graph.facebook.com"
FB_GRAPH_VERSION = "v3.2"

GET_FEED_PARAMS = {"fields" : "created_time,id,likes,reactions{type},comments,message,story,attachments{subattachments}"} 

class FBrequester(object):
  
  def __init__(self, access_token, pageid):
    self.access_token = access_token
    self.pageid = pageid

  """
  REQUEST METHOD
  """

  def ping(self):

    #### if token is 
    # "error": {
    #   "message": "Error validating access token: Session has expired on Monday, 04-Mar-19 00:00:00 PST. The current time is Monday, 04-Mar-19 06:12:36 PST.",
    #   "type": "OAuthException",
    #   "code": 190,
    #   "error_subcode": 463,
    #   "fbtrace_id": "EKU/kVFHv1+"
    # }

    url = self.normalizeQuery("{}".format(self.pageid))
    r = requests.get(url)
    if r.json().get("error") :
      return False
    return True

  def checkToken(self):
    url = self.normalizeQuery("{}".format(self.pageid))
    r = requests.get(url)
    if r.json().get("error") :
      return r.json()
    return { "success" : True }

  def getFeed(self):
    url = self.normalizeQuery("{}/feed".format(self.pageid), GET_FEED_PARAMS)
    r = self.checkBadreq(requests.get(url))
    datalist = r.json().get("data")
    for data in datalist :
      self.removeKey(data, "paging", "likes")
      self.removeKey(data, "paging", "reactions")
      self.removeKey(data, "paging", "comments")
      # data.get("likes").pop("paging")
      # data.get("reactions").pop("paging")
      # data.get("comments").pop("paging")
    return datalist

  def getName(self):
    url = self.normalizeQuery("{}".format(self.pageid))
    r = self.checkBadreq(requests.get(url))
    datalist = r.json()
    return datalist.get("name")

  """
  HELPER METHOD
  """

  def normalizeQuery(self, endpoint, params = None):
    access_token = self.access_token
    access_token_query = "access_token={}&format={}".format(access_token,"json")

    path = "{}/{}".format(FB_GRAPH_URL, FB_GRAPH_VERSION)
    
    if endpoint :
      path = "{}/{}".format(path, endpoint)
    
    path = "{}?{}".format(path, access_token_query)

    if params :
      for key, val in params.items() :
        path = "{}&{}={}".format(path, key, val)

    return path

  def removeKey(self, d, deskey, parentkey) :
    if d.get(parentkey) :
      d[parentkey].pop(deskey)
    elif d.get(deskey) :
      d.pop(deskey)
    return

  # deprecated
  def pretty_old(self, d, indent=0):
    for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
        self.pretty(value, indent+1)
      else:
        print('\t' * (indent+1) + str(value))

  def pretty(self, d, indent=2):
    return json.dumps(d, ensure_ascii=False, indent=2)

  def checkBadreq(self, r):
    if r.status_code == 400 :
      raise Exception(logger.error("Bad Request (400) : " + str(r.json())))
    return r