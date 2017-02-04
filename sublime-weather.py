# -*- coding: utf-8 -*- 
import sublime, sublime_plugin
import threading  
import time

i=0
checkinterval = 1
fetchinterval = 30
msg = ''

import json
import urllib.request

url = 'http://www.weather.com.cn/data/sk/101010100.html'
json_str = '' 
#'{"weatherinfo":{"city":"北京","cityid":"101010100","temp":"18","WD":"东南风","WS":"1级","SD":"17%","WSE":"1","time":"17:05","isRadar":"1","Radar":"JC_RADAR_AZ9010_JB","njd":"暂无实况","qy":"1011","rain":"0"}}'

def use_urllib():
    global json_str;    
    json_strutf8 = urllib.request.urlopen(url, timeout=5).read()   
    json_str = json_strutf8.decode('utf-8')

def getmessage():
    if len(json_str) != 0:
        data = json.loads(json_str)
        global msg;
        msg = "["+data['weatherinfo']['city'] + "="+data['weatherinfo']['temp']+"℃]"
        print (msg)

def write_time():
    if i%fetchinterval == 1:
        use_urllib();
        getmessage();
    sublime.status_message("Weather:"+msg+time_manage(i))

def time_manage(time_number):
    time_str='+('+str(int(time_number/60)).zfill(2)+'m'+str(time_number%60).zfill(2)+'s)'
    return time_str        

class timer(threading.Thread): #The timer class is derived from the class threading.Thread  
    def __init__(self, num, interval):
        threading.Thread.__init__(self)
        self.thread_num = num
        self.interval = interval
        self.thread_stop = False 
    def run(self): #Overwrite run() method, put what you want the thread do here
        global i
        while not self.thread_stop:
            sublime.set_timeout(write_time,checkinterval)
            i+=1  
            time.sleep(self.interval)          
    def pause(self):        
        self.thread_stop = True
    
    def zero(self):
        global i
        i=0    


thread1 = timer(1, 1)
class getweatherCommand(sublime_plugin.TextCommand):    
    def run(self, edit):
        global thread1
        thread=timer(1,checkinterval) 
        if thread1.isAlive():
            live=True
        else:                               
            thread.start()
            thread1=thread

class getweatherpauseCommand(sublime_plugin.TextCommand):    
    def run(self, edit):         
        global thread1
        thread1.pause()

class getweatherzeroCommand(sublime_plugin.TextCommand):    
    def run(self, edit):
        global thread1
        thread1.zero()
        

