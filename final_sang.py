# -*- coding: cp949 -*-
import requests, sys, re, collections
from bs4 import BeautifulSoup



class Crawl:
    def __init__(self, url):
        self.url = url

    def get_source(self):
        r = requests.get(self.url)
        if r.status_code == 200:
            s = BeautifulSoup(r.content, "html.parser")
            return s
        else:
            raise Exception("Invalid URL")

    def res(self,req):
        lst = req.find_all('div',{'id' : 'lyrics'})
        return lst

    def wfile(self,a):
        with open('sample.txt','w') as f:
            for i in a:
                f.write(i.text)


    
def main():
    if len(sys.argv) != 3:
        print 'usage: ./wordcount.py {-c | -h | - t} file'
        sys.exit(1)

    option = sys.argv[1]
    fname = sys.argv[2]

    if option == '-c':
        dct_count(fname)

    elif option == '-h':
        histo(fname)

    elif option == '-t':
        topfive(fname)
        

    else:
        print 'unknown option: ' + option
        sys.exit(1)


def helper(fname):
    with open(fname, 'r') as f:
        lst = list()
        data = f.read()
        sym = re.sub('[-()\"#/@;:<>{}`+=~|.!?,]', ' ', data)
        data = sym.split()
        for i in data:
            lst.append(i.lower())

        return lst


def dct_count(fname):
    dct = dict()
    words = helper(fname)
    for word in words:
        dct[word] = words.count(word)
    print dct

def histo(fname):
    words = helper(fname)
    ex_list = list(set(words))
    for word in ex_list:
        print '%-15s' %word,':', words.count(word) * '*'

def topfive(fname):
    dct = dict()
    words = helper(fname)
    ex_list = list(set(words))
    for w in ex_list:
        dct[w] = words.count(w)

    dct_tup = dct.items()
    dct_tup.sort(key=lambda x: x[1], reverse = True)
    for i in range(5):
        print "top{})".format(i+1),dct_tup[i][0], ':' + str(dct_tup[i][1])
        
    


if __name__ == "__main__":
    lyric = Crawl("https://www.songtexte.com/songtext/freddie-mercury/bohemian-rhapsody-23982857.html")
    req = lyric.get_source()
    a = lyric.res(req)
    lyric.wfile(a)
    main()
    
