from BeautifulSoup import BeautifulSoup
import urllib2
import os
import threading

addr    = 'http://manhua.fzdm.com/17/'
path    = '/home/lycheng/Pictures/comic/fa'
logAddr = path + "/" + "log"
thrNum  = 2

urls    = []
logs    = []
threads = []

mutexForUrls = threading.Lock()
mutexForLog  = threading.Lock()

def readLog():
    fp    = open(logAddr, "r")
    lines = fp.readlines()
    for log in lines:
        logs.append( log[:-1] )
    fp.close()

def getUrls():
    page      = urllib2.urlopen( addr )
    soup      = BeautifulSoup( page )
    container = soup.find(attrs = {'id': 'content'}).findAllNext('li')
    for li in container:
        a = BeautifulSoup(str(li)).find('a')
        try:
            if str(a['href'])[:-1] not in logs:
                urls.append( str( a['href'] )[:-1] ) 
        except:
            pass

def downLoadImg(src, filePath):
    img = urllib2.urlopen( src ).read()
    fp = open( filePath, "w" )
    fp.write( img )
    fp.close()

def threadFun():
    while len( urls ):
        mutexForUrls.acquire()
        url = urls.pop()
        mutexForUrls.release()

        dirPath = path + '/' + url + "/"
        address = addr + url

        if not os.path.isdir( dirPath ):
            os.mkdir( dirPath )

        last   = ''
        suffix = "index_%d.html" 
        for i in xrange(0, 200):
            page = urllib2.urlopen(address + '/' + (suffix % i)).read()
            soup = BeautifulSoup(page)
            imgSrc = soup.find( 'img', id="mhpic" )["src"]
            if last == imgSrc:
                break
            last = imgSrc
            extend = imgSrc[imgSrc.rindex(".") :]
            print imgSrc
            downLoadImg(imgSrc, dirPath + str(i) + extend)

        mutexForLog.acquire()
        fp = open(logAddr, "a")
        fp.write(url + "\n")
        fp.close()
        mutexForLog.release()

def mainFun():
    readLog()
    getUrls()

    for i in xrange(0, thrNum):
        threads.append( threading.Thread( target=threadFun ) )

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print "OK"

if __name__ == "__main__":
    mainFun()
