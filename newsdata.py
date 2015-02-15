# -*- coding: utf-8 -*-
import jieba
import re
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

def calcfreq(seg_list):
    cnlist = [u'！',u' ',u'￥',u'……',u'（',u'）',u'——',u'【',u'】',u'、',u'；',u'：',u'，',u'。',u'《',u'》',u'？',u'你',u'我',u'他',u'她',u'它',u'啊',u'吧',u'的',u'是',u'\u3000',u'"',u')',u'(',u'“',u'%',u'”',u'/',u'\\',u'‘',u'．',u'呀']
    reg = re.compile(r'\d+')
    empty={}
    for i in seg_list.split('|'):
        if i not in empty and i not in cnlist and not reg.match(i):
            empty[i]=1
        elif i in empty:
            empty[i]+=1
    return empty

def textprocess(data):
    lines = data.readlines()
    timemap = {}
    a=0
    for i in lines:
        a+=1
        if a%300==0:
            print "log line: "+str(a)
        #if a==1400:
        #    break
        line = i.split(',')
        timestamp = line[3][1:5]+line[3][6:8]+line[3][9:11]
        seg_list = '|'.join(jieba.cut(line[2]))
        calclst = calcfreq(seg_list)
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


data = open('newsdata.csv','r')
a = textprocess(data)

logfile = open('/home/kurisu/dataanalysis/newsandstockpredict/tmp.log','w')
for i in a.keys():
    logfile.write(i.decode('utf-8','replace')+u'\n')
    calcwords = ''
    for k in a[i].keys():
        calcwords =calcwords+','+k
    calcwords=calcwords
    calcvalues = ''
    for j in a[i].values():
        calcvalues = calcvalues+','+str(j)
    #print calcwords[1:]+'\n'
    logfile.write(calcwords[1:].decode('utf-8','replace')+'\n')
    logfile.write(calcvalues[1:].decode('utf-8','replace')+'\n')
    logfile.flush()
