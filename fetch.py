#!/usr/bin/python3
import sys
import xml.etree.ElementTree
import urllib.request
import re
import pickle

# to get the text between <content> tags in ted-xml files
#$ unxml.py tedfile.xml > target

number = str(5644)
def main():
    f,t = getRange()
    for n in range(f,t+1):    # include t in the range
        savepage(str(n))

    pickle.dump(t,open('lastsaved','wb'))


        
def getRange():
    from_ = pickle.load(open('lastsaved','rb')) + 1 #unpickle last index saved, add one for next
    with urllib.request.urlopen('http://www.sw-ka.de/en/internationales/tandem/') as url:
      content = url.read().decode('utf-8')
    matchObj = re.search( r'<a href="./\?id=(\d{4,})">', content) # first userID
    to_ = int(matchObj.group(1))
    return from_, to_
        
def savepage(number):

   with urllib.request.urlopen('http://www.sw-ka.de/en/internationales/tandem/?id='+number) as url:
      content = url.read().decode('utf-8')

   with open(number+'.html', 'w') as f:
      f.write(content)


    
"""
root = xml.etree.ElementTree.parse(sys.argv[1]).getroot()
for content in root.iter('content'):
    print(content.text)
"""

if __name__ == "__main__":
    main()
