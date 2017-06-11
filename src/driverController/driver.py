#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import built-in packages
# Import external packages
import selenium
from selenium import webdriver

# Import custom modules
# Import package-wide constants


ClassDriver = webdriver.PhantomJS

class webdriverTailored(ClassDriver):
	def __init__(self, path_driver):
		ClassDriver.__init__(self, path_driver)
		
		self.seq_iframe = []
		
	def detect_seq_iframe(self):
		self.seq_iframe = self.find_elements_by_tag_name('iframe')

	def get_pagesource_in_iframe(self, index):
		iframe = self.seq_iframe[index]
		self.switch_to_frame(iframe)
		ret = self.page_source
		
		self.switch_to_default_content()
		return ret

	def kill(self):
		self.close()
		self.quit()

"""
driver = webdriverTailored(PATH_DRIVER)
driver.get(url)
driver.detect_seq_iframe()
for i, iframe in enumerate(driver.seq_iframe):
	psrc = driver.get_pagesource_in_iframe(i)
	soup = BeautifulSoup(psrc, "html.parser")	
	for xpath in get_list_xpath(soup,[]): #, ["p", "script"]):
		print(xpath)
	print("#############################################################################")
driver.kill()
"""