#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import built-in packages
# Import external packages
import selenium
from selenium import webdriver

# Import custom modules
# Import package-wide constants

def create_driver_phantomjs(system, path_driver):
	if "linux" in system or "mac" in system:
		path_phantomjs = path_driver + "phantomjs"
	elif "win" in system:
		path_phantomjs = path_driver + "phantomjs.exe"
	ret = webdriver.PhantomJS(path_phantomjs)
	return ret

def create_driver(system, path_driver, type_driver="phantomjs"):
	if type_driver == "phantomjs":
		ret = create_driver_phantomjs(system, path_driver)
	return ret


driverClass = webdriver.PhantomJS

class webdriverTailored(driverClass):
	# def __init__(self):
	pass

	def break_into_iframe(self, driver, iframe):
		self.driver.switch_to_frame(iframe)
		ret = driver.page_source
		driver.switch_to_default_content()
		return ret

	def has_iframe(self):
		driver = create_driver(SYSTEM)
		driver.get(url)
		try:
			driver.find_element_by_tag_name('iframe')
		except selenium.common.exceptions.NoSuchElementException:
			ret = False
		else:
			ret = True
		return ret

	def kill(self):
		self.close()
		self.quit()







def some_action(url):
	driver = create_driver(SYSTEM, PATH_DRIVER)	
	driver.get(url)
	outputs = []
	
	iframes = driver.find_elements_by_tag_name('iframe')
	for iframe in iframes:
		outputs.append(break_into_iframe(driver, iframe))
	
	kill_driver(driver)		
	return outputs