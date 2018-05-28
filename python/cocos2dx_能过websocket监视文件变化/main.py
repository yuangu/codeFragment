#-*-coding:utf8-*-

import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado import gen

from watchdog.observers import Observer
from watchdog.events import *

import time
import datetime
import Queue 
import json
import os
import sys
import hashlib


workPaths = (
    (r"D:\code\android\cocos\game\res", r"D:\code\android\cocos\game"),
    (r"D:\code\android\cocos\game\src", r"D:\code\android\cocos\game"),
)

#获取python文件所在的路径
def p():
    frozen = "not"
    if getattr(sys, 'frozen',False):
        frozen = "ever so"
        return os.path.dirname(sys.executable)

    return os.path.split(os.path.realpath(__file__))[0]

class FileJsonMaker():
    #获取文件的md5值
    def getFileMd5(self, filename):
        try:    
            if not os.path.isfile(filename):
                return
            myhash = hashlib.md5()
            f = file(filename,'rb')
            while True:
                b = f.read(8096)
                if not b :
                    break
                myhash.update(b)
            f.close()
            return myhash.hexdigest().lower()
        except:
            print filename  + " 获取md5失败"

    #获取某目录下的所有的文件列表
    def scanfile(self, path):
        fileList = os.listdir(path)
        ret = []
        for fileName in fileList:
            filepath = os.path.join(path,fileName) 
            if os.path.isdir(filepath):            
                ret.extend(self.scanfile(filepath))
            else:
                ret.append(filepath)
        return ret

    def doWork(self):
        jsonObj = {}  #保存的json
        
        for v in workPaths:
            rootPath = v[0]
            prePath = v[1]
            gameResList = self.scanfile(rootPath)

            for desPath in gameResList:
                md5 = self.getFileMd5(desPath)
                url = os.path.relpath(desPath, prePath)
                url = url.replace("\\", "/")

                jsonObj[url] = {
                        'md5':md5 ,
                        'size': os.path.getsize(desPath),
                        'path':  url
                    }
   
       
        #保存版本json文件
        return json.dumps(jsonObj)

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    users = set()
    
    def check_origin(self, origin):
        return True

    def open(self):
        print u"[%s]-[%s]-连接系统" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.users.add(self);     

    def on_close(self):
        self.users.remove(self) 
        print u"[%s]-[%s]-断开系统" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def on_message(self,message):
        print "on_message"
        self.write_message("message received")

    def callback(self,count):
        self.write_message('{"inventorycount":"%s"}'%count)

class VersionHandler(tornado.web.RequestHandler):    
    @tornado.web.asynchronous
    def get(self):
        fileJsonMaker = FileJsonMaker()
        version = fileJsonMaker.doWork()
        self.write(version)
        self.finish()


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/fileWatch/', WebSocketHandler),        
        ]
        
        for v in workPaths:
            rootPath = v[0]
            prePath = v[1]  

            relpath = os.path.normpath( os.path.relpath(rootPath, prePath) ).replace("\\", "/")

            handlers.append(( r'/download/' +  relpath + '/(.*)', tornado.web.StaticFileHandler, {'path':rootPath} ));
        
        fileJsonMaker = FileJsonMaker()
        version = fileJsonMaker.doWork()
        
        handlers.append( (r'/download/version.json', VersionHandler));
        settings = {
        
        }

        tornado.web.Application.__init__(self, handlers, **settings)

#监视文件
class FileEventHandler(FileSystemEventHandler):
    def __init__(self, rootPath):
        self.mRootPath = rootPath
        FileSystemEventHandler.__init__(self)

    def on_moved(self, event):      
        data = {
            "is_directory":event.is_directory,
            "dest_path": os.path.normpath(os.path.relpath(event.dest_path,self.mRootPath)).replace("\\", "/"),
            "src_path":os.path.normpath(os.path.relpath(event.src_path,self.mRootPath)).replace("\\", "/"),
            "event":"moved"
        }
        
        self.sendMsg( json.dumps(data) )

    def on_created(self, event):      
        data = {
            "is_directory":event.is_directory,           
            "src_path":os.path.normpath(os.path.relpath(event.src_path,self.mRootPath)).replace("\\", "/"),
            "event":"created"
        }
        
        self.sendMsg( json.dumps(data) )

    def on_deleted(self, event):        
        data = {
            "is_directory":event.is_directory,           
            "src_path":os.path.normpath(os.path.relpath(event.src_path,self.mRootPath)).replace("\\", "/"),
            "event":"deleted"
        }
        
        self.sendMsg( json.dumps(data) )   

    def on_modified(self, event):        
        data = {
            "is_directory":event.is_directory,            
            "src_path":os.path.normpath(os.path.relpath(event.src_path,self.mRootPath)).replace("\\", "/"),
            "event":"modified"
        }
        
        self.sendMsg( json.dumps(data) )
        
    def sendMsg(self, data):
        print data
        for u in WebSocketHandler.users:  # 向已在线用户发送消息
            u.write_message(data)


@gen.coroutine
def loop_func():
    observer = Observer()   
    for v in workPaths:
        rootPath = v[0]
        prePath = v[1]
        observer.schedule(FileEventHandler(prePath), rootPath,True)

    observer.start()
    while True:   
        yield gen.sleep(1)        
    observer.join()


if __name__ == '__main__':
    tornado.options.parse_command_line()
    server = tornado.httpserver.HTTPServer(Application())
    server.listen(8000)
    tornado.ioloop.IOLoop.instance().spawn_callback(loop_func)
    tornado.ioloop.IOLoop.instance().start()