#-*- coding:utf-8 -*-
import os
import socket
import sys
import getopt

#获取当前运行的主机地址
def getHostIp():
    # myname = socket.getfqdn(socket.gethostname())
    # myaddr = socket.gethostbyname(myname)
    # return myaddr
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    myaddr = s.getsockname()[0]
    s.close()
    return myaddr

#获取python文件所在的路径
def p():
    frozen = "not"
    if getattr(sys, 'frozen',False):
        frozen = "ever so"
        return os.path.dirname(sys.executable)

    return os.path.split(os.path.realpath(__file__))[0]


#执行命令
def runCmd(outDir, ip,  company="WoAiWo Technology Co.ltd"):     
    cmd =  'openssl genrsa -out "%s/MyCA.key" 2048 '%outDir
    print "run cmd:" +  cmd
    os.system(cmd)
    
    #cmd = 'openssl req -x509 -new -key "%s/MyCA.key" -out "%s/MyCA.cer" -days 730 -subj /CN="ipa-server:%s By %s '%(outDir,outDir,ip,author)
    # os.system(cmd)

    cmd = 'openssl req -x509 -new -key "%s/MyCA.key" -out "%s/MyCA.cer" -days 730 -subj /CN="%s" '%(outDir,outDir,company)
    print "\n\n=====================================================\nrun cmd:" +  cmd + '\n=====================================================\n\n\n'
    os.system(cmd)

    cmd = 'openssl genrsa -out "%s/Server.key" 2048 ' % (outDir)
    print "\n\n=====================================================\nrun cmd:" +  cmd + '\n=====================================================\n\n\n'
    os.system(cmd)

    cmd = 'openssl req -new -out "%s/Server.req" -key "%s/Server.key" -subj /CN=%s '%(outDir,outDir,ip)
    print "\n\n=====================================================\nrun cmd:" +  cmd + '\n=====================================================\n\n\n'
    os.system(cmd)

    cmd = 'openssl x509 -req -in  "%s/Server.req" -out "%s/Server.cer" -CAkey "%s/MyCA.key" -CA "%s/MyCA.cer" -days 365 -CAcreateserial -CAserial "%s/serial" '%(outDir,outDir,outDir,outDir,outDir)
    print "\n\n=====================================================\nrun cmd:" +  cmd + '\n=====================================================\n\n\n'
    os.system(cmd)
    
    f = open( os.path.join(outDir, "Server.key") , "r" )
    lines = f.readlines()
    f.close()

    f = open( os.path.join(outDir, "Server.cer") , "r" )
    lines.extend(f.readlines())
    f.close()

    f = open( os.path.join(outDir, "Server.pem") , "w+" )
    f.writelines(lines)
    f.close()

    # cmd = 'cat "%s/Server.key" "%s/Server.cer" > "%s/Server.pem"'%(outDir,outDir,outDir)
    # print "\n\n=====================================================\nrun cmd:" +  cmd + '\n=====================================================\n\n\n'
    # os.system(cmd)

def mkDir(dirPath):
    if os.path.exists(dirPath) and os.path.isdir(dirPath):
        return
    parent = os.path.dirname(dirPath)
    if not (os.path.exists(parent) and os.path.isdir(parent)):
        mkDir(parent)
    
    os.mkdir(dirPath)

def usage():
    print 'usage: generate-certificate [--ip  192.168.1.18] [--company="WoAiWo Technology Co.ltd"] [--dir ./out]'


def main():
    opts, args = getopt.getopt(sys.argv[1:], "dihc:", ["dir=", "ip=","help", "company="])
    outDir = "./out"
    ip = getHostIp()
    company = "WoAiWo Technology Co.ltd"

    for (o, a) in opts:
        if o in ("-h", "--help"):
            usage()      
        elif o in ("-d", "--dir"):
            outDir = a
        elif o in ("-i", "--ip"):
            ip = a
        elif o in ("-c", "--company"):
            company = a
    
    if os.path.relpath(outDir):
        outDir = os.path.normpath( os.path.join(p(), outDir))
    mkDir(outDir)

    runCmd(outDir, ip, company )


if __name__ =="__main__":
    try:
        main()
    except BaseException,e:
        print e
    