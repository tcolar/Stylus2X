import struct;
import time;
import pygame;
import TouchScreen;
import VirtualKB;

class Editor:
    
    done=False;
    
    def __init__(self,container):
        self.screen=container;
        self.kb=VirtualKB.VirtualKB();
        self.ts=TouchScreen.TouchScreen(container);
        self.font=pygame.font.Font(None,18);
        self.font2=pygame.font.Font(None,14);
        self.str="xyz";

    def start(self):
        self.updateEditPane();
        self.mainLoop();
        
    def mainLoop(self):
        while(not self.done):
            # check every 20ms until exit;
            value=self.ts.readTSValue();

            if(value.pressure > 0):
                print value.x, value.y, value.pressure;
                #self.screen.fill((255,0,0),(value.x, value.y, 2, 2));
                key=self.kb.handleClick((value.x,value.y));
                char=key.getKey();
                if(char!=None):
                    print "Got a char from VirtualKB: ",char;
                    if(char==VirtualKB.VirtualKBKey.BACKSPACE):
                        self.str=self.str[0:len(self.str)-1];
                    elif(char==VirtualKB.VirtualKBKey.ENTER):
                        self.str=self.str;
                    elif(char==VirtualKB.VirtualKBKey.SPACE):
                        self.str=self.str+' ';
                    else:
                        self.str=self.str+char;
                self.updateEditPane();

            if(value.x>300 and value.y>200):
                self.done=True;
            time.sleep(.02);
    
    def updateEditPane(self):
        self.editPane=pygame.Surface((320,220));
        self.editPane.fill((0,0,0));
        pygame.draw.rect(self.editPane,(80,80,80),(0,0,30,220));
        pygame.draw.rect(self.editPane,(80,80,100),(30,40,290,15));
        line=self.font2.render("123:",True,(0,255,0));
        txt=self.font.render(self.str,True,(0,255,0));
        self.editPane.blit(line,(1,144));#44
        self.editPane.blit(txt,(35,140));#40
        self.screen.blit(self.editPane,(0,20));
        self.kb.showKB1(self.screen,(0,88));
        pygame.display.flip();
        
# End class

#MAIN for running it
#Editor().main();
