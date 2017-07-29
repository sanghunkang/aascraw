#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import built-in packages
import os, sys

SEQ_TAG_UNWRAP = ["br","span","p","em","img","strong"]
SEQ_TAG_DECOMP = ["a","script","style"]
SEQ_TAGCODE = [
	"","a","abbr","acronym","address","applet","area","article","aside","audio",
	"b","base","basefont","bdi","bdo","big","blockquote","body","br","button",
	"canvas","caption","center","cite","code","col","colgroup","datalist","dd",
	"del","details","dfn","dialog","dir","div","dl","dt","em","embed","fieldset",
	"figcaption","figure","font","footer","form","frame","frameset","h1","h2",
	"h3","h4","h5","h6","head","header","hr","html","i","iframe","img","input",
	"ins","kbd","keygen","label","legend","li","link","main","map","mark","menu",
	"menuitem","meta","meter","nav","noframes","noscript","object","ol","optgroup",
	"option","output","p","param","picture","pre","progress","q","rp","rt","ruby",
	"s","samp","script","section","select","small","source","span","strike","strong",
	"style","sub","summary","sup","table","tbody","td","textarea","tfoot","th",
	"thead","time","title","tr","track","tt","u","ul","var","video","wbr",
]

SYSTEM = sys.platform
if "linux" in SYSTEM or "mac" in SYSTEM:
	PATH_DRIVER_PHANTOMJS = os.path.abspath('..') + "/drivers/phantomjs"
	PATH_DRIVER_CHROME = os.path.abspath('..') + "/drivers/chromedriver"
elif "win" in SYSTEM:
	PATH_DRIVER_PHANTOMJS = os.path.abspath('..') + "\\drivers\\phantomjs.exe"
	PATH_DRIVER_CHROME = os.path.abspath('..') + "\\drivers\\chromedriver.exe"

