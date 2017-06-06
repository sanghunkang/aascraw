#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import built-in packages
from urllib import request

# Import external packages
from bs4 import BeautifulSoup

def get_HTMLdoc(url):
	req = request.urlopen(url)
	charset = req.info().get_content_charset()
	ret = req.read().decode(charset)
	return ret