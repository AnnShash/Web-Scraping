# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 09:11:33 2019
@author: Shashini
"""
import re
import urllib.request
from nltk.stem import PorterStemmer
import collections, functools, operator 

def file_append_data(file_name):
    """This append data from a text file"""
    My_Data = []
    f = open(file_name,'r')
    for line in f:
        My_Data.append(line[0:-1])
    f.close()
    return My_Data

def get_word_array(content,key):
    """This will extract all the text in the given HTML tags"""
    text = ''
    tag = re.compile(key)
    text = re.findall(tag,content)
    text = re.sub('<.*?>', ' ', str(text))
    return text
    
def clean(text):
    """This will clean punctuation and transform all words to lowercase"""
    news = ''
    Data = []
    text = text.lower()
    for c in text:
        if c >= 'a' and c <= 'z':
            news += c
        else:
            news += ' '
    for word in news.split(' '):
        Data.append(word)
    return Data

def common_words(words):
    """This will remove all the common words maintained in commonwords.txt"""
    stopwrds = file_append_data('commonwords.txt')
    key_words = [word for word in words if word not in stopwrds]
    return key_words

def stemmer(word):
    """This will stem all the keywords"""
    ps = PorterStemmer()
    stems = []
    for i in word:
        stems.append(ps.stem(i))
    return stems

def weight_cnt(cln_stem,wgt):
    """This will give the word count and multiply it with the given weight"""
    wdict = {}
    for word in cln_stem:
        wdict[word] = wdict.get(word,0)+(1*wgt)
    return wdict

def combine(content,key,wgt):
    """Combination of all functions to clean & extract data"""
    txt = get_word_array(content,key)
    cln = clean(txt)
    cw = common_words(cln)
    stem = stemmer(cw)
    weight = weight_cnt(stem,wgt)
    return {'text':txt, 'clean':cln,'com_wrds':cw, 'stemmer':stem, 'wgt':weight}

#def combine(soup,key,wgt):
#    ft = weight_cnt(stemmer(common_words(clean(get_word_array(soup,key)))),wgt)
#    return ft

def file_write(file_name,Data,url,index):
    """This will write data to a text file. The text file will open in writing 
    mode if the index is 0, else with the appending mode"""
    if index == 0:
        fp = open(file_name,'w',encoding = 'utf-8')
    else:
        fp = open(file_name,'a',encoding = 'utf-8')
    fp.write('url {} - {}'.format(index+1,url))
    fp.write('\n')
    
    """Will sum up all the dictionaries and append the relevent information"""
    reduced_data = dict(functools.reduce(operator.add,map(collections.Counter,Data))) 
    
    word_freq = []
    for key, value in reduced_data.items():
        word_freq.append((key,value))
    
    """sorting and writing the information to the text file"""
    word_freq.sort(key=lambda tup: tup[1], reverse=True)
    fp.write('\n'.join('{} : {}'.format(item[0],'%0.1f' %item[1]) for item in word_freq))
    fp.write('\n\n')
    fp.close()
    
"""Extracting required data"""
urls = file_append_data('URLList.txt')


for index,url in enumerate(urls):
    
    htmlfile = urllib.request.urlopen(url)
    content = str(htmlfile.read())
    
    title = combine(content,'<title>(.*?)</title>',1)
    h1 = combine(content,'<h1>(.*?)</h1>',0.8)
    h2 = combine(content,'<h2>(.*?)</h2>',0.7)
    h3 = combine(content,'<h3>(.*?)</h3>',0.6)
    para = combine(content,'<p>(.*?)</p>',0.5)

    Data = [title['wgt'],h1['wgt'],h2['wgt'],h3['wgt'],para['wgt']]
    file_write('directory.txt',Data,url,index)
    
    
    
    
    
    
    
    
    
    
  