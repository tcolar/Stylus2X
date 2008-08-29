import struct;
import time;
import pygame;
import TouchScreen;
import VirtualKB;
import pexpect;
import threading;
import ANSI
import traceback;
import Battery;
import Pane;

class Shell( Pane.Pane ):
    '''
    Shell panel, start and handles a shell (~ bash)
    '''
    
    nbLines=18;
    nbCols=64;
    #nbLines=10;
    #nbCols=20;
    ansi=ANSI.ANSI(nbLines-1,nbCols-1);
    textColor=(255,255,0);
    yOffset=17;   
    yStep=8; 
    
    def __init__(self,main):
        Pane.Pane.__init__ ( self );
        self.main=main;
        self.screen=main.screen;
        self.kb=VirtualKB.VirtualKB(main);
        
        self.font2=pygame.font.Font(self.main.skinFolder+"/font.ttf",8);
        self.font=pygame.font.Font(None,12);
        
        self.str="";
        self.bash = pexpect.spawn("/bin/bash");
        self.shellReader=ShellReader(self);
        self.shellReader.start();
        self.shellLines=[];
        self.shellImage=pygame.image.load(self.main.skinFolder+"/shell.png");
        self.editPane=pygame.Surface((320,240));
        
    def handleEvent(self,value):
                    
        key=self.kb.handleClickKb2((value.x,value.y));
        char=key.getKey();
        if(char!=None):
            # note: this will callback "updateshell" as necessary
            self.bash.send(char);
            self.main.debug("Got key: ",char);
        else:
            self.updateScreen();
            
    
    def updateScreen(self):
        self.editPane.blit(self.shellImage,(0,0));
        
        if(self.shellLines!=None):
            y=self.yOffset;
            cpt=0;
            for line in self.shellLines:
                if(cpt>len(self.shellLines)-self.nbLines):
                    line = line.replace('\t', ' ');
                    ln=self.font2.render(line,True,self.textColor);
                    self.editPane.blit(ln,(2,y));
                    y=y+self.yStep;
                cpt=cpt+1;
        self.screen.blit(self.editPane,(0,0));
        self.kb.showKB2(self.screen,(0,240-80));
        self.main.paintMenuBar();
        pygame.display.flip();
    
    def appendLine(self,line):
        if(line!=None and len(line)>0):
            #self.showHex(line);
            self.ansi.write(line);
            self.main.debug (self.ansi.pretty());
            self.shellLines=str(self.ansi).splitlines();
        self.updateScreen();
    
    def handleShutdown(self):
        self.shellReader.shutdown();
        self.bash.close();
        
    def showHex(self,line):
        s="";
        for c in line:
            s+=hex(ord(c))+"("+c+") ";
        print s;
# End class

class ShellReader ( threading.Thread ):
    done=False;
    loopDone=False;
    
    def __init__(self,shell):
        '''will consume the shell/bash output'''
        threading.Thread.__init__ ( self );
        self.shell=shell;
        
    def run ( self ):
        while(not self.done):
            pygame.time.delay(100);
            try:
                line=self.shell.bash.read_nonblocking(5000,2);
                self.shell.appendLine(line);
            except pexpect.TIMEOUT:
                pass;
            except pexpect.EOF:
                print "Shell script EOF - done.";
                return;
            except pexpect.ExceptionPexpect:
                traceback.print_exc();
        self.loopDone=True;
    
    def shutdown(self):
        self.done=True;
        while(not self.loopDone):
            time.sleep(.05);
        

#MAIN for running it
#Editor().main();
