import os
path = r'C:\code\MyLuaGame\frameworks\runtime-src\Classes'
addPath = r'../../Classes'

for  root,dirs,files in os.walk(path):    
        for filespath in files:
            if filespath[ -4: ] == ".cpp" or filespath[ -3: ] == ".cc"or filespath[ -2: ] == ".c":
                 result = os.path.join(root,filespath)
                 result = result.replace(path, addPath)
                 result = result.replace('\\', '/')
                 print result + '   \\'
print ""
