#!/usr/bin/python3
# -*- coding: utf-8 -*-

import xml.sax
import os

count = 0
bugs = {}
bugInfo = []

class JiraBugHandler( xml.sax.ContentHandler ):
   def __init__(self):
      self.CurrentData = ""
      self.link = ""
      self.title = ""
      self.component = ""
 
   # 元素开始事件处理
   def startElement(self, tag, attributes):
      self.CurrentData = tag
      global count
      if tag == "item":
         #print("*****bug*****")
         bugInfo.clear()
         count = count + 1
 
   # 元素结束事件处理
   def endElement(self, tag):
      if self.CurrentData == "title":
         #print("title:", self.title)
         bugInfo.append(self.title)
      elif self.CurrentData == "link":
         print(self.link)
         bugInfo.append(self.link)
      elif self.CurrentData == "component":
         #print("component:", self.component)
         bugInfo.append(self.component)
         if self.component not in bugs.keys():
           bugs[self.component] = []
         bugs[self.component].append(bugInfo)
 
   # 内容事件处理
   def characters(self, content):
      if self.CurrentData == "title":
         self.title = content
      elif self.CurrentData == "link":
         self.link = content
      elif self.CurrentData == "component":
         self.component = content
  
if ( __name__ == "__main__"):
   
   # 创建一个 XMLReader
   parser = xml.sax.make_parser()
   # turn off namepsaces
   parser.setFeature(xml.sax.handler.feature_namespaces, 0)
 
   # 重写 ContextHandler
   Handler = JiraBugHandler()
   parser.setContentHandler( Handler )
   
   parser.parse("D:\\SearchRequest.xml")

   #i = 0
   #for (k,v) in bugs.items():
       #print(k,' :\n')
       #for bug in v:
           #print(bug[1],'\n')
           #i = i+1
   print("total bugs link {0}".format(count))