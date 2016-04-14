import pickle,time,os
class datahandler:
    def __init__(self,path,pickler=False):
        self.path = path
        if pickler:
            self._write = self.picklewrite
        else:
            self._write = self.defaultwrite
        if pickler:
            self._read = self.pickleread
        else:
            self._read = self.defaultread
    def read(self,data=None):
        f = open(self.path,'r')
        out = self._read(f)
        print 'read success at '+self.path
        f.close()
        return out
    def write(self,data=None):
        import codecs
        f = codecs.open(self.path,'wb')
        out = self._write(data.encode('utf-8'),f)
        print 'write success at '+self.path
        f.close()
        return out
    def pickleread(self,fileobj):
        return pickle.load(fileobj)
    def defaultread(self,fileobj):
        return fileobj.read()
    def picklewrite(self,data,fileobj):
        return pickle.dump(data,fileobj)
    def defaultwrite(self,data,fileobj):
        return fileobj.write(data)
def temppathmake(ext='.py'):
    t = str(time.time())
    secs = t[0:t.find(".")]
    path = 'C://ahktempfiles//temp//dump_' + secs + ext
    return path
