# -*- coding: utf-8 -*-
import jieba
import re
import sys
import time
import jieba.posseg as pseg
import thread

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


starttime =time.clock()
print 'start at:'+str(starttime)
cnlist = [u'！',u' ',u'￥',u'……',u'（',u'）',u'——',u'【',u'】',u'、',u'；',u'：',u'，',u'。',u'《',u'》',u'？',u'你',u'我',u'他',u'她',u'它',u'啊',u'吧',u'的',u'是',u'\u3000',u'"',u')',u'(',u'“',u'%',u'”',u'/',u'\\',u'‘',u'．',u'呀',u'.',u'']
reg = re.compile(r'\d+|[a-z|A-Z]')

def calcfreq(seg_list,cnlist,reg):
    empty={}
    for i in seg_list: #.split('|'):
        if i not in empty and i not in cnlist and not reg.match(i) :
            empty[i]=1
        elif i in empty:
            empty[i]+=1
    return empty

def parseprocess(data):
    print 'In Textprocess'
    nonest = ['n','ns','nr','nt','nz','vn','an']
    secst = ['f','v','vf']
    processtime =time.clock()
    timemap = {}
    a=0
    for i in data:
        a+=1
        if a%3000==0:
            print str(a)+' loops in '+str(time.clock()-processtime)
    #    if a==100:
    #        break
        line = i.split(',')
        timestamp = line[3][1:5]+line[3][6:8]+line[3][9:11]
        #print 'cutting'
        ns = pseg.cut(line[2])
        #print 'cutting over'
        seg_list=[]
        for t in ns:
            if t.flag in nonest:
                seg_list.append(t.word)
        #seg_list = '|'.join(pseg.cut(line[2]))
        calclst = calcfreq(seg_list,cnlist,reg)
        calcmap={}
        if timestamp in timemap:
            calcmap=timemap[timestamp]

        for i in calclst:
            if i in calcmap:
                calcmap[i]+=calclst[i]
            else:
                calcmap[i]=calclst[i]
                #log = i+'='+str(calc_map[i])+u'\n'
                #logfile.write(log.encode('utf-8'))
            timemap[timestamp]=calcmap
            #print str(timemap.keys())
    return timemap


def makefiles(mapdata):
    logfile = open('./tmp.txt','w')
    statisticfile = open('./statistic.csv','w')
    totalwords={}
    for i in mapdata.keys():
        logfile.write(i.decode('utf-8','replace')+u'\n')
        calcwords = ''
        for k in mapdata[i].keys():
            calcwords =calcwords+','+k
            if k in totalwords:
                totalwords[str(i)+','+str(k)]+=a[i][k]
            else:
                totalwords[str(i)+','+str(k)]=a[i][k]
        calcvalues = ''
        for j in a[i].values():
            calcvalues = calcvalues+','+str(j)
    #print calcwords[1:]+'\n'
        logfile.write(calcwords[1:].decode('utf-8','replace')+'\n')
        logfile.write(calcvalues[1:].decode('utf-8','replace')+'\n')
        logfile.flush()
    for i in totalwords.keys():
        if totalwords[i]>2:
            statisticfile.write(i.decode('utf-8','reploace')+','+str(totalwords[i])+'\n')

#update for thread simple and ugly....
def combinemap(map1,map2):
    mapkeys = map1.keys().append(map2.keys())
    resmap={}
    seti=Set(i)
    for j in i:
        if j in map1 and j in map2:
            resmap[j]=map1[j]+map2[j]
        elif j in map1:
            resmap[j]=map1[j]
        else:
            resmap[j]=map2[j]
    return resmap

def textprocess(data):
    lines = data.readlines()
    timemap={}
    par = len(lines)/4
    if par<0: #TODO:remarked for mutip thread update
        for j in lines:
            try:
                tm1=thread.start_new_thread(parseprocess,(lines[0:par],))
                timemap=combinemap(tmc1,tmc2)
            except:
                print 'Error in textprocess thread'
    else:
        timemap=parseprocess(lines)
    return timemap

data = open('data.csv','r')
a = textprocess(data)
makefiles(a)
endtime =time.clock()
print 'totaltime='+str(endtime-starttime)
