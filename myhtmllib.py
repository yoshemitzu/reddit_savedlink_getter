import time,subprocess,os
import tempdatahandler as datahandler
class document:
    def __init__(self,path=None,silent=True):
        self.text = ''
        if path == None:
            path = datahandler.temppathmake('.html')
        self.datahandler = datahandler.datahandler(path)
        self.hasbeenwritten = False
        if not silent:
            self.adddocline('<!doctype html>')
    def add(self,text):
        self.text += text
    def addandreturn(self,text):
        self.text += text
        self.addreturn()
    def addlink(self,url,text):
        self.text += maketextlink(url,text)
    def addimg(self,img):
        imgtext = makeimglink(img.linkurl,
                              img.align+' '+img.otherthing+' '+img.size,
                              img.url,
                              img.alt,
                              img.width,
                              img.height)
        self.addandreturn(imgtext)
    def addheader(self,text,size=1,style="",anchor=''):
        self.adddocline(makeheader(text,size,style,anchor))
    def addtab(self):
        self.text += '\t'
    def addhorizontalrule(self):
        return self.adddocline('<hr />')
    def addtimestamp(self,timeformat=None):
        self.text += timestamp(timeformat)
    def addreturn(self):
        self.text += '\n'
    def addlinebreak(self):
        self.text += '<br>'
    def adddocline(self,text):
        self.text += text
        self.addreturn()
    def addline(self,text):
        self.text += '<br>'+text+'</br>'
        self.addreturn()
    def addlist(self,itemlist):
        for item in itemlist:
            self.addlistitem(item)
    def addlistitem(self,text):
        self.addtab()
        self.text += makelistitem(text)
        self.addreturn()
    def addunorderedlist(self,itemlist):
        for item in itemlist:
            self.addunorderedlistitem(item)
    def addunorderedlistitem(self,text):
        self.addtab()
        self.text += makeunorderedlistitem(text)
        self.addreturn()
    def embedvideo(self,url):
        self.text += '[embed]'+url+'[/embed]'
        self.addreturn
    def write(self,path=None):
        if path != None:
            self.datahandler = datahandler.datahandler(path)
        return self.datahandler.write(self.text)
    def read(self):
        return self.datahandler.read(self.text)
    def run(self,write=True):
        if write == True or self.hasbeenwritten == False:
            self.write()
            self.hasbeenwritten = True
        subprocess.Popen(["C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                          os.path.realpath(self.datahandler.path)])
class image:
    def __init__(self,linkurl,selfurl,alt,width,height,align,size,otherthing):
        self.linkurl = linkurl
        self.url = selfurl
        self.alt = alt
        self.width = width
        self.height = height
        self.align = align
        self.size = size
        self.otherthing = otherthing
def makeimglink(linkurl,imgdetails,imgurl,alt,width,height):
    try:
        out = '<a href="'+linkurl+'">'
        out += '<img class="'+imgdetails+'" src="'+imgurl+'" alt="'+alt
        # wordpress stupidity
        out += ' width="'
        out += ' width="'+str(width)+'" height="'+str(height)+'"'
        out += '">'
        out += '</a>'
        return out
    except:
        return ''
        print "no img link available"
def makeheaderstyle(style=''):
    # options: left, right, center, justify
    if style == '':
        return ''
    else:
        return ' style="text-align: '+style+';"'
def makeanchortag(anchor):
    if anchor == '':
        return ''
    else:
        return '<a name="'+anchor[0]+'">'+anchor[1]+'</a>'
def makeheader(text,size,style,anchor):
    #text-align: center;
    return '<h'+str(size)+makeheaderstyle(style)+'>'+makeanchortag(anchor)+text+'</h'+str(size)+'>'
def maketextlink(url,text):
    return '<a href="'+url+'">'+str(text)+'</a>'
def timestamp(timeformat=None):
    date = time.localtime()
    return str(date[3])+':'+str(date[4]).zfill(2)+' '+time.tzname[0]+', '+str(date[1])+'-'+str(date[2])+'-'+str(date[0])
def makelistitem(text):
    return '<li>'+text+'</li>'
def makeunorderedlistitem(text):
    return '<ul>'+text+'</ul>'
class htmlmaker:
    def opentabsclass(self):
        self.tabnum = 0
        return self.adddocline('[tabs class="" size="large"]')
    def closetabsclass(self):
        return self.adddocline('[/tabs]')
    def startnewtab(self,tabname):
        if self.tabnum == 0:
            tabactive = 'true'
        else:
            tabactive = 'false'
        self.tabnum += 1
        return self.adddocline('[tab active="'+tabactive+'" title="'+tabname+'s"]')
    def endnewtab(self):
        return self.adddocline('[/tab]')
