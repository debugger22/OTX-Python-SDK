#!/usr/bin/env python

import time
import re
import logging
import datetime
import simplejson as json

try:
	# For Python2
	import httplib
	import urlparse
except ImportError:
	# For Python3
	import http.client as httplib
	import urllib.parse as urlparse

try:
	# For Python2
	from urllib2 import URLError, build_opener
except ImportError:
	# For Python3
	from urllib.error import URLError
	from urllib.request import build_opener


logger = logging.getLogger("OTXv2")


class InvalidAPIKey(Exception):
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)


class BadRequest(Exception):
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)


class OTXv2(object):
	"""
	Main class to interact with the AlienVault OTX API.
	"""
	def __init__(self, key, server="http://otx.alienvault.com"):
		self.key = key
		self.server = server 

	def get(self, url):
		request = build_opener()
		request.addheaders = [('X-OTX-API-KEY', self.key)]
		response = None
		try:
			response = request.open(url)
		except URLError as e:
			if e.code == 403:
				raise InvalidAPIKey("Invalid API Key")
			elif e.code == 400:
				raise BadRequest("Bad Request")
		data = response.read()
		json_data = json.loads(data)
		return json_data

	def getall(self, limit=20):
		pulses = []
		next = "%s/api/v1/pulses/subscribed?limit=%d" % (self.server, limit)
		while next:
			json_data = self.get(next)
			for r in json_data["results"]:
				pulses.append(r)
			next = json_data["next"]
		return pulses

	def getall_iter(self, limit=20):
		pulses = []
		next = "%s/api/v1/pulses/subscribed?limit=%d" % (self.server, limit)
		while next:
			json_data = self.get(next)
			for r in json_data["results"]:
				yield r
			next = json_data["next"]
		
	def getsince(self, mytimestamp, limit=20):
		pulses = []
		next = "%s/api/v1/pulses/subscribed?limit=%d&modified_since=%s" % (self.server, limit, mytimestamp)
		while next:
			json_data = self.get(next)
			for r in json_data["results"]:
				pulses.append(r)
			next = json_data["next"]
		return pulses

	def getsince_iter(self, mytimestamp, limit=20):
		pulses = []
		next = "%s/api/v1/pulses/subscribed?limit=%d&modified_since=%s" % (self.server, limit, mytimestamp)
		while next:
			json_data = self.get(next)
			for r in json_data["results"]:
				yield r
			next = json_data["next"]
		

	def getevents_since(self, mytimestamp, limit=20):
		events = []
		next = "%s/api/v1/pulses/events?limit=%d&since=%s" % (self.server, limit, mytimestamp)
		while next:
			json_data = self.get(next)
			for r in json_data["results"]:
				events.append(r)
			next = json_data["next"]
		return events
