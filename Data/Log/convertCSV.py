import  re
import sys

# path='Dia_system/20211201_165213'
path= sys.argv[1]
oneLine=""
with open(path,encoding='utf-8') as f:
    for line in f.readlines():
        lineList = line.split('|')
        line = lineList[3]
        if(line.find('----')==-1):

            if(line.find("input")==-1):
                oneLine += ","
            oneLine += re.sub('.*:','',line).rstrip()
            if(line.find("output")!=-1):
                print(oneLine)
                oneLine =""
            if(line.find("/reset")!=-1):
                print("\n\n")
                oneLine+=""
        
