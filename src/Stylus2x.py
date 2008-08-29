import struct;
import time;
import pygame;
import Shell;
import os;
import Battery;
import ConfigParser
import Music;
import threading;
import TouchScreen;

class Stylus2x:
    '''
    Main class of Stylus2X app
    '''
    PANE_SHELL=1;
    PANE_MUSIC=2;

    done=False;
    debugOn=False;
    #debugOn=True;
    # TODO: kinda lame:
    isGp2X=True;

    def __init__(self):
        self.isGp2X=os.path.exists("/mnt/nand");
        self.currentArea=self.PANE_SHELL;
        
        self.cfg = ConfigParser.ConfigParser();
        self.cfg.read("stylus2x.ini");
        self.skinFolder=self.getGlobalConf("skinFolder")

        pygame.init();
        self.screen = pygame.display.set_mode((320, 240));
        self.screen.fill((0, 0,  255));
        pygame.display.flip();
        self.batLow=pygame.image.load(self.skinFolder+"/batt_bad.png");
        self.batHigh=pygame.image.load(self.skinFolder+"/batt_good.png");
        self.batFull=pygame.image.load(self.skinFolder+"/batt_full.png");
        self.batEmpty=pygame.image.load(self.skinFolder+"/batt_empty.png");
        self.batUnknown=pygame.image.load(self.skinFolder+"/batt_unknown.png");
        self.buttonShell=pygame.image.load(self.skinFolder+"/button_shell.png");
        self.buttonMusic=pygame.image.load(self.skinFolder+"/button_music.png");
        self.buttonOff=pygame.image.load(self.skinFolder+"/button_off.png");
        #launcher (+ favorites)  -> start create delete
        #browser  (launch, delete etc.. ?)
        #music
        #shell
        self.menubar=pygame.image.load(self.skinFolder+"/menubar.png");
    
    def getGlobalConf(self,option,skipParse=True):
        return self.cfg.get("Global",option,skipParse)

    def getConf(self,option,skipParse=True):
        section="GP2X";
        if(not self.isGp2X):
            section="PC";
        print "getting: "+section;
        return self.cfg.get(section,option,skipParse)
    
    def isGp2X(self):
        return self.isGp2X;    

        
    def shutdown(self):
        self.debug("Termination requested");
        self.eventThread.shutdown();
        self.shell.shutdown();
        self.music.shutdown();
        pygame.quit();
        
    def main(self):
        #load panels
        self.music=Music.Music(self);
        self.music.start();
        self.shell=Shell.Shell(self);
        self.shell.start();
        self.toogle(self.PANE_SHELL);
        #start event loop
        self.eventThread=EventThread(self);
        self.eventThread.start();

    def toogle(self, area):
        '''
        Toogle one of the panes (shell/Music/Browser etc..)
        '''
        if(area==self.PANE_MUSIC):
            self.currentArea=self.PANE_MUSIC;
            self.currentPane=self.music;
            self.currentPane.updateScreen();
        else:
            #shell
            self.currentArea=self.PANE_SHELL;
            self.currentPane=self.shell;
            self.currentPane.updateScreen();

    def paintMenuBar(self,surface=None):
        '''
        Paint the menubar on a panel
        '''
        if(surface==None):
            surface=self.screen;
        surface.blit(self.menubar,(0,0));
        surface.blit(self.buttonShell,(70,0));
        surface.blit(self.buttonMusic,(86,0));
        bat=Battery.Battery(self).getValue();
        #print bat;
        if(bat==0):
            surface.blit(self.batFull,(285,5));            
        elif(bat==1):
            surface.blit(self.batHigh,(285,5));            
        elif(bat==2):
            surface.blit(self.batLow,(285,5));            
        elif(bat==3):
            surface.blit(self.batEmpty,(285,5));            
        else:
            surface.blit(self.batFull,(285,5));            
        surface.blit(self.buttonOff,(305,0));
 
    def handleMBClick(self,pos):
        '''
        Handles a menubar click
        '''
        (x,y)=pos;
        if(x>70 and x<85):
            self.toogle(self.PANE_SHELL);
        elif(x>86 and x<101):
            self.toogle(self.PANE_MUSIC);
        elif(x>304):
            self.shutdown();
        
    def debug(self,str1,str2=""):
        if(self.debugOn):
            print str1,str2;

    
# End class
class EventThread(threading.Thread):
    '''
    Handles all the (Touchscreen) events and pass them to the active panel.
    '''
    def __init__(self,main):
        threading.Thread.__init__ ( self );
        self.ts=TouchScreen.TouchScreen(main.screen);
        self.main=main;
        self.done=False;

    def shutdown(self):
        self.done=True;
        time.sleep(.2);

    def run ( self ):
        while(not self.done):
            # check every 20ms until exit;
            value=self.ts.readTSValue();
            if(value.pressure > 0):
                self.main.debug("value.pressure",value.pressure);
                self.main.debug("value.x",value.x);
                self.main.debug("value.y",value.y);

                if(value.y<15):
                    self.main.handleMBClick((value.x,value.y));
                # pass value to current panel;
                
                if(not self.done):
                    self.main.currentPane.handleEvent(value);
            time.sleep(.2);
        self.main.debug("Event thread terminated.");
# End class
        
#MAIN for running it
Stylus2x().main();
