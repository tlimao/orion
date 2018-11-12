import urllib.request
import ssl
from datetime import datetime
from warren.common import *
from warren.stnparser import StnParser

class StnCrawler():

	def __init__(self):
		self.stnparser = StnParser()

		self.ctx = ssl.create_default_context()
		self.ctx.check_hostname = False
		self.ctx.verify_mode = ssl.CERT_NONE

	def crawling(self):
		stnPage = urllib.request.urlopen(STN_PAGE)
	
		return self.stnparser.parse(str(stnPage.read()))