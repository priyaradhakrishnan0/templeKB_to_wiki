"""This module uses Jinja2 template rendering to create wiki pages of templeKB temples.
Code is modelled on Nikhil's repo for rendering karnatic raga pages in the IIIT-Hyderabad's
Indian Language Wikipedia project. Please refer https://github.com/nikhilpriyatam/kb_to_wiki for more info."""

import json
import re
from jinja2 import Environment, FileSystemLoader

ENV = Environment(loader=FileSystemLoader('templates')) # Global variable
ENV.line_statement_prefix = '#'

def listClean(localList):
    cleanList = []
    non_null_answers = [k for k in localList if k !=' ']
    if len(non_null_answers) > 0:
        for ans in non_null_answers:
            if '[CLS]' in ans or '[SEP]' in ans:
                continue
            if ans in cleanList: #already present. Skip to next ans
                continue
            cleanList.append(ans)
    return cleanList                

def getTempleDic(ansList):
    templeDic = dict()
    for i in range(len(ansList)):
        if i==0:##Location : "Where is temple located?","Where is the temple situated?",
            locationList = listClean(ansList[0])
            if len(locationList) > 0:
                templeDic['Location'] = (',').join(locationList)
        elif i==1 and 'Location' not in templeDic:
            locationList = listClean(ansList[1])
            if len(locationList) > 0:
                templeDic['Location'] = (',').join(locationList)
        elif i==2:##Diety : "The temple is dedicated to whom?", "Who is the diety?",
            dietyList = listClean(ansList[2])
            if len(dietyList) > 0:
                templeDic['Diety'] = (',').join(dietyList)
        elif i==3 and 'Diety' not in templeDic:
            dietyList = listClean(ansList[3])
            if len(dietyList) > 0:
                templeDic['Diety'] = (',').join(dietyList)
        templeDic['Built'] =''
        templeDic['Darshan hours'] = ''
        templeDic['Darshan duration'] = ''
        templeDic['Facilities available'] = ''
        templeDic['Managed by'] = ''
        templeDic['Language'] = ''
        templeDic['Email'] = ''
        templeDic['Contact'] = ''
        templeDic['Website'] = ''    
    return templeDic

def fetch_temples():
    corpusPath = './corpus/WebTempleCorpus.json'
    count = 0
    with open(corpusPath, 'r') as f:
        jason = json.load(f)
        for temple in jason:
            if "head_line" in temple:
                continue
            #print(len(jason[temple]["answers"]))
            templeDic = getTempleDic(jason[temple]["answers"])
            temple_name = re.split('Temple',temple,1)
            if len(temple_name)>1:
                templeDic['key'] = temple_name[0] + ' Temple'
            else:
                templeDic['key'] = temple_name[0].replace('.txt','')
            #print(templeDic)
            count +=1
            #if count>= 5:
            if temple=='Bharathappilly Sree Bharatha Temple.txt':
                #demo_wiki(templeDic)
                demo_indianLanguage(templeDic) #malayalam by default
                #demo_indianLanguage(templeDic,'telugu')
                break

#def demo_wiki(t1):
#    template = ENV.get_template('demo_temple.wiki')
#    res_str = template.render(temple=t1)
#    with open('rendered_pages/demo_temple.wiki', 'w') as res:
#        res.write(res_str)

def demo_wiki(t1=None):
    """Demo temple_wiki in Englishs"""
    template = ENV.get_template('demo_temple.wiki')
    if t1==None:
        t1 = {'key':"Vadapalani Dhandayutapaani, Vadapalani Andavar Temple.txt", 'Diety':"Muruga", 'Website':"http://vadapalaniandavartemple.tnhrce.in/"}
        t2 = {'key':"Tiruvirkolam Tripurantaka -. Temple  - Shivastalam.txt", 'Diety':"Shiva", 'Website':"http://www.shivatemples.com/tnaadu/tn14.php"}
    res_str = template.render(temple=t1)
    with open('rendered_pages/'+t1['key']+'.wiki', 'w') as res:
        res.write(res_str)

def demo_indianLanguage(t1=None, language='malayalam'):
    """Default language is malayalam"""
    template = ENV.get_template(language+'_temple.wiki')
    if t1==None:
        t1 = {'key':"Kodungallur Bhagawati Temple", 'Diety':"Durga", 'Website':"http://kerala.bizhat.com/kodungallor.html"}
    res_str = template.render(temple=t1)
    with open('rendered_pages/'+language+'/'+t1['key']+'.wiki', 'w') as res:
        res.write(res_str)

if __name__ == '__main__':
    fetch_temples()
    #demo_wiki()
