#-*-coding:utf8-*-
import zipfile
import os
import shutil
import ConfigParser
import sys
import datetime
import getopt
#获取python文件所在的路径
def p():
    frozen = "not"
    if getattr(sys, 'frozen',False):
        frozen = "ever so"
        return os.path.dirname(sys.executable)

    return os.path.split(os.path.realpath(__file__))[0]

def checkPath(path):
    if not os.path.isabs(path):
        path = os.path.join(p(), path)
    return os.path.normpath(path)

def readConf(path = "config.ini"):
    cf = ConfigParser.ConfigParser()
    path = checkPath(path)
    cf.read(path)
    #获取证书相关的配置信息
    certificate = {v[0]:v[1]  for v  in cf.items("certificate") }
    #工程相关的
    project= {v[0]:v[1]  for v  in cf.items("project") }
    #文件拷贝
    copyList = [v[1].split('=>')  for v  in cf.items("copy") ]  
    return {"certificate":certificate, "project":project, "copyList":copyList }

#获取母包
def getParentPack(apkPath, outPath = "./out" , delList = []):
    outPath = os.path.realpath(outPath)

    with zipfile.ZipFile("Game.apk", "r") as fz:
        for file in fz.namelist():
            fz.extract(file, outPath)
    
    for fname in delList:
        fullPath = os.path.join(outPath, fname)
        if not os.path.exists(fullPath):
            continue
        if os.path.isdir(fullPath) :
            shutil.rmtree(fullPath)
        elif os.path.isfile(fullPath):
            os.remove(fullPath)

#从souce_dir拷贝代码至zip_dir目录下的
def packToZip(zipf, source_dir, zip_dir = None):
    fullSourcePath =  os.path.realpath(source_dir)
  
    if os.path.isfile(fullSourcePath):
        fileRelPath = os.path.basename(fullSourcePath)
        if zip_dir:
            fileRelPath = zip_dir      
        zipf.write(fullSourcePath, fileRelPath)
        
        return

    for parent, dirnames, filenames in os.walk(source_dir): 
        for filename in filenames:
            #获取文件绝对路径
            filePath = os.path.join(parent, filename)
            #获取文件相对的路径 
            fileRelPath = os.path.relpath(filePath, fullSourcePath)
            #需要加上前缀路径
            if zip_dir:
                fileRelPath = os.path.join(zip_dir, fileRelPath)

            zipf.write(filePath, fileRelPath)

#给apk签名
def signApk(keystorePath, storepass, keypass, aliseName, inAPK, outAPK):
    cmd = "jarsigner -verbose -keystore %s -storepass %s -keypass  %s  -signedjar %s %s %s"%(keystorePath, storepass, keypass, outAPK,inAPK,aliseName)
    print "run cmd:" +  cmd
    os.system(cmd)


if __name__ == '__main__':
    
    configPath = "config.ini"
    try:  
        opts, args =  getopt.getopt(sys.argv[1:], "i:"); 
        for v in opts:   
            if v[0] == "-i":
               configPath = v[1] 
       
    except getopt.GetoptError:
        print "usage: quickPackAndroid.py -i XXXX.ini"
        sys.exit(-1)
    
    #获取配置
    config = readConf(configPath)   
    originalAPK = config["project"]["originalapk"]
    originalAPK = checkPath(originalAPK)
    print "originalAPK=" + originalAPK

    tmpPath = config["project"]["tmpdir"]
    tmpPath = checkPath(tmpPath )

    if not os.path.exists(tmpPath):
        os.mkdir(tmpPath)

    print "tmpPath="+tmpPath

    #这个是解压出来的母包地址
    originalDir = os.path.join(tmpPath, "android")

    #生成母包解压文件
    getParentPack(originalAPK, originalDir, ["assets", "META-INF"])

    #生成的未签名包地址
    tmpkpg= os.path.join(tmpPath, "tmp.apk")
    #将文件打入新生成的apk
    with zipfile.ZipFile(tmpkpg, "w", zipfile.ZIP_DEFLATED) as fz:
        packToZip(fz, originalDir)
        for  info in config["copyList"] : 
            fromPath = checkPath(info[0])     
            print fromPath + "=>" + info[1]
            packToZip(fz,fromPath, info[1])
        #packToZip(fz, r"F:\code\APP\agency\branch\develop\Resource\images", "assets/images")
        #packToZip(fz, r"F:\code\APP\agency\branch\develop\Resource\scripts", "assets/scripts")
        #packToZip(fz, r"F:\code\APP\agency\branch\develop\Resource\plugin", "assets/plugin")

    #最终生成包的地方
    outPath = config["project"]["outdir"]
    outPath = checkPath(outPath )
    if not os.path.exists(outPath):
        os.mkdir(outPath)
    print "outPath="+outPath

    #生成签名包
    keystorePath = config["certificate"]["keystorepath"]
    keystorePath = checkPath(keystorePath)
    print "keystorePath=" + keystorePath

    storepass = config["certificate"]["storepass"]
    print "keystorePath=" + storepass

    keypass= config["certificate"]["keypass"]
    print "keypass=" + keypass

    aliseName = config["certificate"]["alisename"]
    print "aliseName=" + aliseName


    appName = config["project"]["appname"]
    now = datetime.datetime.now()
    appName  = appName + "_"  + now.strftime('%Y-%m-%d_%H_%M_%S')  + ".apk"
    print "appName=" + aliseName

    savePath = os.path.join(outPath, appName)
    savePath = os.path.normpath(savePath)

    signApk(keystorePath, storepass, keypass, aliseName, tmpkpg, savePath)
    #清理缓存 
    if os.path.exists(tmpPath):
        shutil.rmtree(tmpPath)
        




    
