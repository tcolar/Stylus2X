import pygame;

class VirtualKB:
    '''
    Draw and handles a Virtula Keyboard (TouchScreen)
    '''

    ''' Special keys sequences'''
    K_ESCAPE="\x1b";
    K_LEFT="\x1b\x5b\x44";
    K_RIGHT="\x1b\x5b\x43";
    K_UP="\x1b\x5b\x41";
    K_DOWN="\x1b\x5b\x42";
    K_PG_UP="\x1b\x5b\x35\x7e";
    K_PG_DN="\x1b\x5b\x36\x7e";
    K_HM="\x1b\x5b\x31\x7e";
    K_INS="\x1b\x5b\x32\x7e";
    K_END="\x1b\x5b\x34\x7e";
    K_F1="\x1b\x5b\x31\0x31\x7e";
    K_F2="\x1b\x5b\x31\0x32\x7e";
    K_F3="\x1b\x5b\x31\0x33\x7e";
    K_F4="\x1b\x5b\x31\0x34\x7e";
    K_F5="\x1b\x5b\x31\0x35\x7e";
    K_F6="\x1b\x5b\x31\0x37\x7e";
    K_F7="\x1b\x5b\x31\0x38\x7e";
    K_F8="\x1b\x5b\x31\0x39\x7e";
    K_F9="\x1b\x5b\x32\0x30\x7e";
    K_F10="\x1b\x5b\x32\0x31\x7e";
    K_F11="\x1b\x5b\x32\0x33\x7e";
    K_F12="\x1b\x5b\x32\0x34\x7e";        
    
    red=(255,200,200);
    blue=(200,200,255);
    dkRed=(200,150,150);
    dkBlue=(150,150,200);
    grey=(150,150,150);
    green=(200,255,80);
    yellow=(200,200,150);

    keyLine1=(("1","!"), ("2","@"), ("3","#"), ("4","$"), ("5","%"), ("6","^"), ("7","&"), ("8","*"), ("9","("), ("0","!"));
    keyLine2=(("Q","Q"), ("W","W"), ("E","E"), ("R","R"), ("T","T"), ("Y","Y"), ("U","U"), ("I","I"), ("O","O"), ("P","P"));
    keyLine3=(("A","A"), ("S","S"), ("D","D"), ("F","F"), ("G","G"), ("H","H"), ("J","J"), ("K","K"), ("L","L"), ("'","\""));
    keyLine4=(("Z","Z"), ("X","X"), ("C","C"), ("V","V"), ("B","B"), ("N","N"), ("M","M"), (".","/"), (",","\\"), (";",":"));

    k2Line1=(("ESC","ESC"), ("F1","F1"), ("F2","F2"), ("F3","F3"), ("F4","F4"), ("F5","F5"), ("F6","F6"), ("F7","F7"), ("F8","F8"), ("F9","F9"), ("F10","F10"), ("F11","F11"), ("F12","F12"),('',''),("INS","INS"));
    k2Line2=(("`","~"),("1","!"), ("2","@"), ("3","#"), ("4","$"), ("5","%"), ("6","^"), ("7","&"), ("8","*"), ("9","("), ("0","!"),("-","_"),("=","+"),("BAK","BAK"),("HM","HM"));
    k2Line3=(("TAB","TAB"),("Q","Q"), ("W","W"), ("E","E"), ("R","R"), ("T","T"), ("Y","Y"), ("U","U"), ("I","I"), ("O","O"), ("P","P"),("[","{"),("]","}"),("\\","|"),("DEL","DEL"));
    k2Line4=(("CPS","CPS",1,dkRed),("A","A"), ("S","S"), ("D","D"), ("F","F"), ("G","G"), ("H","H"), ("J","J"), ("K","K"), ("L","L"), (";",":"),("'","\""),("RETURN","RETURN",2),("END","END"));
    k2Line5=(("SHF","SHF",1,dkRed),("Z","Z"), ("X","X"), ("C","C"), ("V","V"), ("B","B"), ("N","N"), ("M","M"), (",","<"), (".",">"), ("/","?"),("SHF","SHF",1,dkRed),('',''),('',''),("UP","UP"),);
    k2Line6=(("CTL","CTL",1,dkBlue),("WIN","WIN"), ("ALT","ALT",1,dkBlue), ("SPACE","SPACE",5), ("ALT","ALT",1,dkBlue), ("WIN","WIN"), ("MEN","MEN"), ("CTL","CTL",1,dkBlue),('',''),('',''),("DN","DN"));
    
    def __init__(self,main):
        self.main=main;
        self.shiftOn=False;
        self.capsOn=False;
        self.kb2On=False;
        self.ctrlOn=False;
        self.altOn=False;
        #TODO: use skinFolder property
        self.kb1Image=pygame.image.load(self.main.skinFolder+"/kb1.png");
        self.kb2Image=pygame.image.load(self.main.skinFolder+"/kb2.png");
    

    # Use functions
    def showKB1(self,screen,pos):
        (self.offsetX,self.offsetY)=pos;
        if(self.shiftOn):
            pygame.draw.rect(self.kb1Image,self.yellow,(3,122,26,26),2); 
        if(self.capsOn):
            pygame.draw.rect(self.kb1Image,self.yellow,(35,122,26,26),2); 
        screen.blit(self.kb1Image,(self.offsetX,self.offsetY));
        pygame.display.flip();

    def showKB2(self,screen,pos):
        (self.offsetX,self.offsetY)=pos;
        screen.blit(self.kb2Image,(self.offsetX,self.offsetY));
        if(self.shiftOn):
            pygame.draw.rect(screen,self.red,(3+self.offsetX,53+self.offsetY,20,12),2); 
            pygame.draw.rect(screen,self.red,(3+self.offsetX+21*11,53+self.offsetY,20,12),2); 
        if(self.capsOn):
            pygame.draw.rect(screen,self.red,(3+self.offsetX,40+self.offsetY,20,12),2); 
        if(self.altOn):
            pygame.draw.rect(screen,self.blue,(3+self.offsetX+21*2,66+self.offsetY,20,12),2); 
            pygame.draw.rect(screen,self.blue,(3+self.offsetX+21*8,66+self.offsetY,20,12),2); 
        if(self.ctrlOn):
            pygame.draw.rect(screen,self.blue,(3+self.offsetX,66+self.offsetY,20,12),2); 
            pygame.draw.rect(screen,self.blue,(3+self.offsetX+21*11,66+self.offsetY,20,12),2); 
        pygame.display.flip();
    
    def handleClickKb1(self,pos):
        '''Handle a clikc and return the VirtualKey pressed (None for things like 'shift')'''
        char=VirtualKBKey(None);
        (x,y)=pos;
        x=x-self.offsetX;
        y=y-self.offsetY;
        index=0;
        if((self.capsOn and not self.shiftOn) or (not self.capsOn and self.shiftOn)):
            index=1;
        if(x>0 and y>0 and x<320 and y<150):
            col=(x+2)/32;
            line=(y+1)/31;
            if(line==0):
               char.setKey(self.keyLine1[col][index]); 
            elif(line==1):
               char.setKey(self.keyLine2[col][index]); 
            elif(line==2):
               char.setKey(self.keyLine3[col][index]); 
            elif(line==3):
               char.setKey(self.keyLine4[col][index]); 
            elif(line==4):
                if(col==0):
                    self.shiftOn=not self.shiftOn;
                elif(col==1):
                    self.capsOn=not self.capsOn;
                elif(col==2):
                    char.setKey(VirtualKBKey.BACKSPACE);
                elif(col==3 or col==4):
                    char.setKey(VirtualKBKey.SPACE);
                elif(col==5 or col==6):
                    char.setKey(VirtualKBKey.ENTER);
                if(col==7):
                    self.ctrlOn=True;
                if(col==8):
                    self.altOn=True;
                #if(col==9):
                #    self.shiftOn=True;
                    
                    
            if(char.getKey()!=None):
                self.shiftOn=0;
                self.altOn=0;
                self.ctrlOn=0;
                if(index==0 and len(char.getKey())==1):
                    char.setKey(char.getKey().lower());
        return char;
    
    def handleClickKb2(self,pos):
        '''Handle a click and return the VirtualKey pressed (None for things like 'shift')'''
        char=VirtualKBKey(None);
        (x,y)=pos;
        x=x-self.offsetX;
        y=y-self.offsetY;
        index=0;
        if((self.capsOn and not self.shiftOn) or (not self.capsOn and self.shiftOn)):
            index=1;
        if(x>0 and y>0 and x<316 and y<77):
            col=(x+3)/21;
            line=(y+1)/13;
            if(line==0):
                char.setKey(self.k2Line1[col][index]); 
            elif(line==1):
                char.setKey(self.k2Line2[col][index]); 
            elif(line==2):
                char.setKey(self.k2Line3[col][index]); 
            elif(line==3):
                if(col==0):
                    self.capsOn=not self.capsOn;
                else:
                    if(col>12):
                        # enter key is size:2
                        col=col-1;
                    char.setKey(self.k2Line4[col][index]); 
            elif(line==4):
                if(col==0 or col==11):
                    self.shiftOn=not self.shiftOn;
                else:
                    char.setKey(self.k2Line5[col][index]); 
            elif(line==5):
                if(col==0 or col==11):
                    self.ctrlOn=not self.ctrlOn;
                elif(col==2 or col==8):
                    self.altOn=not self.altOn;
                else:
                    if(col>3 and col<=7):
                        # space key is size:5
                        col=3;
                    elif(col>7):
                        col=col-5;
                    char.setKey(self.k2Line6[col][index]); 
                    
            if(char.getKey()!=None):
                c=char.getKey();
                if(len(c)>1):
                    if(c=="RETURN"):
                        char.setKey("\n");
                    elif(c=="BAK"):
                        char.setKey("\b");
                    elif(c=="TAB"):
                        char.setKey("\t");
                    elif(c=="SPACE"):
                        char.setKey(" ");
                    elif(c=="ESC"):
                        char.setKey(self.K_ESCAPE);
                    elif(c=="UP"):
                      char.setKey(self.K_UP);
                    #elif(c=="DN"):
                    #  char.setKey(self.K_DOWN);
                    #elif(c=="L"):
                    #  char.setKey(self.K_LEFT);
                    #elif(c=="R"):
                    #  char.setKey(self.K_RIGHT);
                    #elif(c=="PG_UP"):
                    #    char.setKey(self.K_PG_UP);
                    #elif(c=="PG_DN"):
                    #    char.setKey(self.K_PG_DN);
                    elif(c=="END"):
                        char.setKey(self.K_END);
                    elif(c=="INS"):
                        char.setKey(self.K_INS);
                    elif(c=="HM"):
                        char.setKey(self.K_HM);
                    elif(c=="F1"):
                        char.setKey(self.K_F1);
                    elif(c=="F2"):
                        char.setKey(self.K_F2);
                    elif(c=="F3"):
                        char.setKey(self.K_F3);
                    elif(c=="F4"):
                        char.setKey(self.K_F4);
                    elif(c=="F5"):
                        char.setKey(self.K_F5);
                    elif(c=="F6"):
                        char.setKey(self.K_F6);
                    elif(c=="F7"):
                        char.setKey(self.K_F7);
                    elif(c=="F8"):
                        char.setKey(self.K_F8);
                    elif(c=="F9"):
                        char.setKey(self.K_F9);
                    elif(c=="F10"):
                        char.setKey(self.K_F10);
                    elif(c=="F11"):
                        char.setKey(self.K_F11);
                    elif(c=="F12"):
                        char.setKey(self.K_F12);
                self.shiftOn=0;
                self.altOn=0;
                self.ctrlOn=0;
                if(index==0 and len(char.getKey())==1):
                    char.setKey(char.getKey().lower());
        return char;

    # following are function to GENERATE the KB maps.
    def getCustomButton(self,screen,key,width,color,textPos):
        (x,y)=textPos;
        button = pygame.Surface([width,28], pygame.SRCALPHA, 32)
        pygame.draw.rect(button,color,(0,0,width,28),2); 
        text = self.font3.render(key, 1,color);
        button.blit(text, (x,y));
        return button;
        
    def getButton(self,screen,key):
        (k1,k2)=key;
        button = pygame.Surface([28,28], pygame.SRCALPHA, 32)
        pygame.draw.rect(button,self.grey,(0,0,28,28),2); 
        text = self.font.render(k1, 1,self.grey);
        text2 = self.font2.render(k2, 1,self.red);
        if(k2==k1):
            button.blit(text, (7,5));
        else:
            button.blit(text, (11,7));
            button.blit(text2, (2,2));
        return button;

    def getSmallButton(self,screen,key):
        sz=1;
        color=self.grey;
        if(len(key)>3):
            (k1,k2,sz,color)=key;
        elif(len(key)>2):
            (k1,k2,sz)=key;
        else:
            (k1,k2)=key;        
        button = pygame.Surface([20*sz+(sz-1),12], pygame.SRCALPHA, 32)
        if(not (k1=='' and k2=='')):
            pygame.draw.rect(button,color,(0,0,20*sz+(sz-1),12),2); 
            text = self.fontb.render(k1, 1,self.green);
            text2 = self.fontb2.render(k2, 1,self.red);
            if(k2==k1):
                button.blit(text, (2,2));
            else:
                button.blit(text, (11,2));
                button.blit(text2, (2,1));
        return button;
    
    def sz(self,key):
        sz=1;
        if(len(key)>2):
            sz=key[2];
        return sz;

    def generateKBImages(self):
        pygame.init();
        self.font = pygame.font.Font(None, 28);
        self.font2 = pygame.font.Font(None, 18);
        self.font3 = pygame.font.Font(None, 16);
        self.fontb = pygame.font.Font(None, 13);
        self.fontb2 = pygame.font.Font(None, 12);
        self.fontb3 = pygame.font.Font(None, 10);

        screen=pygame.surface.Surface((320,150),pygame.SRCALPHA,32);
        
        cpt=0;
        for key in self.keyLine1:
            button=self.getButton(screen,key);
            screen.blit(button,(2+cpt*32,1));
            cpt=cpt+1;
        cpt=0;
        for key in self.keyLine2:
            button=self.getButton(screen,key);
            screen.blit(button,(2+cpt*32,131));
            cpt=cpt+1;
        cpt=0;
        for key in self.keyLine3:
            button=self.getButton(screen,key);
            screen.blit(button,(2+cpt*32,61));
            cpt=cpt+1;
        cpt=0;
        for key in self.keyLine4:
            button=self.getButton(screen,key);
            screen.blit(button,(2+cpt*32,91));
            cpt=cpt+1;
        
        shift=self.getCustomButton(screen,"SHF",28,self.red,(3,10));
        screen.blit(shift,(2,121));
        caps=self.getCustomButton(screen,"CPS",28,self.red,(3,10));
        screen.blit(caps,(34,121));
        back=self.getCustomButton(screen,"DEL",28,self.grey,(4,10));
        screen.blit(back,(66,121));
        space=self.getCustomButton(screen,"SPACE",60,self.grey,(12,10));
        screen.blit(space,(98,121));
        enter=self.getCustomButton(screen,"ENTER",60,self.grey,(13,10));
        screen.blit(enter,(162,121));
        ctrl=self.getCustomButton(screen,"CTL",28,self.blue,(3,10));
        screen.blit(ctrl,(226,121));
        alt=self.getCustomButton(screen,"ALT",28,self.blue,(3,10));
        screen.blit(alt,(258,121));
        special=self.getCustomButton(screen,"{[...",28,self.grey,(4,10));
        screen.blit(special,(290,121));
        
        pygame.image.save(screen,"skin/kb1.bmp");
        print "generated skin/k1.bmp";
                
        #KB2
        screen=pygame.surface.Surface((320,80),pygame.SRCALPHA);
        cpt=0;
        for key in self.k2Line1:
            button=self.getSmallButton(screen,key);
            screen.blit(button,(3+cpt*21,1));
            cpt=cpt+self.sz(key);
        cpt=0;
        for key in self.k2Line2:
            button=self.getSmallButton(screen,key);
            screen.blit(button,(3+cpt*21,14));
            cpt=cpt+self.sz(key);
        cpt=0;
        for key in self.k2Line3:
            button=self.getSmallButton(screen,key);
            screen.blit(button,(3+cpt*21,27));
            cpt=cpt+self.sz(key);
        cpt=0;
        for key in self.k2Line4:
            button=self.getSmallButton(screen,key);
            screen.blit(button,(3+cpt*21,40));
            cpt=cpt+self.sz(key);
        cpt=0;
        for key in self.k2Line5:
            button=self.getSmallButton(screen,key);
            screen.blit(button,(3+cpt*21,53));
            cpt=cpt+self.sz(key);
        cpt=0;
        for key in self.k2Line6:
            button=self.getSmallButton(screen,key);
            screen.blit(button,(3+cpt*21,66));
            cpt=cpt+self.sz(key);
        pygame.image.save(screen,"skin/kb2.bmp");
        print "generated skin/k2.bmp";
 
    def testKBImages(self):
        # test the image
        screen = pygame.display.set_mode((320, 150),pygame.SRCALPHA);
        self.showKB1(screen,(0,0));
        pygame.time.wait(5000);


class VirtualKBKey:
    BACKSPACE="BACKSPACE";
    ENTER="ENTER";
    SPACE="SPACE";
    
    def __init__(self,key):
        self.key=key;
            
    def getKey(self):
        return self.key;
    
    def setKey(self,key):
        self.key=key;
    
#Main: manual keyboard rendering
#VirtualKB().generateKBImages();
#VirtualKB().testKBImages();
