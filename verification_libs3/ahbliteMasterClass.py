
import os,sys
import veri
import logs

class ahbliteMaster(logs.driverClass):
    def __init__(self,Path,Monitors,Translations={}):
        logs.driverClass.__init__(self,Path,Monitors)
        self.Path = Path
        self.queue=[]
        self.seq=[]
        self.waiting=0
        self.translations=Translations

    def translate(self,Addr):
        if Addr[0] in '0123456789':
            return eval(Addr)
        if Addr in self.translations:
            return self.translations[Addr][0]
        print('cannot determine "%s" address'%Addr)
        return 0

    def busy(self):
        if self.queue!=[]: return True
        if self.waiting>0: return True
        if self.seq!=[]:   return True
        return False

    def action(self,Txt):
        wrds = Txt.split()
        if wrds[0]=='write':
            self.write(wrds[1],wrds[2])
        elif wrds[0]=='read':
            self.read(wrds[1])
        elif wrds[0]=='wait':
            self.wait(eval(wrds[1]))
        else:
            logs.log_info('AHB ACTION %s failed'%Txt)

    def wait(self,Wait):
        self.queue.append(('wait',Wait))

    def read(self,Addr):
        if type(Addr) is str:
            Addr = self.translate(Addr)
        self.queue.append(('read',Addr))



    def write(self,Addr,Data):
        if type(Addr) is str:
            Addr = self.translate(Addr)
        self.queue.append(('write',Addr,Data))
        

    def run(self):
        if self.waiting>0:
            self.waiting -= 1
            return
        if self.seq!=[]:
            List = self.seq.pop(0)
            for (Sig,Val) in List:
                if Sig=='wait':
                    self.waiting=int(Val)
                elif Sig=='catch':
                    X = self.peek(Val)
                    print('ahb read %s'%X)
                else:
                    self.force(Sig,Val)
            return

        if self.queue!=[]:
            What = self.queue.pop(0)
            if What[0]=='wait':
                self.seq.append([('wait',What[1])])
                return
            if What[0]=='write':
                self.seq.append([('haddr',What[1]),('hwdata',What[2]),('hwrite',1),('htrans',2),('hsize',2)])
                self.seq.append([('wait',1)])
                self.seq.append([('haddr',0),('hwdata',0),('hwrite',0),('htrans',0),('hsize',0)])
                self.seq.append([('wait',5)])
                return

            if What[0]=='read':
                self.seq.append([('haddr',What[1]),('hwrite',0),('htrans',2)])
                self.seq.append([('wait',1)])
                self.seq.append([('haddr',0),('hwrite',0),('htrans',0),('catch','hrdata')])
                self.seq.append([('wait',5)])
                return



