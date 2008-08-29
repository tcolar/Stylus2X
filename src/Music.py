import pygame;
import Pane;
import TouchScreen;
import time;
import threading;
import os;
import fnmatch;
from pygame.mixer import music as music
import mutagen;
import mutagen.easyid3;
import random;

class Music(Pane.Pane):
    '''
    Music Panel app
    '''
    def __init__(self,main):
        self.forceRefresh=False;
        self.imgPatterns=[".png",".jpg",".jpeg",".gif"];
        
        self.meta = {"artist":"--","title":"--","tracknumber":"--","date":"--","album":"--","length":0}

        Pane.Pane.__init__ ( self );
        self.main=main;
        self.screen=main.screen;
        self.ts=TouchScreen.TouchScreen(self.screen);
        
        self.font2=pygame.font.Font(self.main.skinFolder+"/font.ttf",8);
        self.font=pygame.font.Font(None,12);
        self.musicImage=pygame.image.load(self.main.skinFolder+"/music.png");
        self.buttonPlay=pygame.image.load(self.main.skinFolder+"/button_play.png");
        self.buttonNext=pygame.image.load(self.main.skinFolder+"/button_next.png");
        self.buttonPrev=pygame.image.load(self.main.skinFolder+"/button_prev.png");
        self.buttonNew=pygame.image.load(self.main.skinFolder+"/button_new.png");
        self.buttonAdd=pygame.image.load(self.main.skinFolder+"/button_add.png");
        self.buttonSave=pygame.image.load(self.main.skinFolder+"/button_save.png");
        self.buttonLoad=pygame.image.load(self.main.skinFolder+"/button_load.png");
        self.emptyCD=pygame.image.load(self.main.skinFolder+"/cd.jpg");
        self.cdImg=self.emptyCD;
        self.editPane=pygame.Surface((320,240));
        musicFolder=main.getConf("musicFolder")
        
        self.updater=ScreenUpdater(self);
        self.updater.start();
        
        #test
        #self.selfTest();
        
        self.playlist=PlayList();
        
        ## testiing ##
        self.playlist.addFolder(musicFolder,True);
        self.playlist.randomize();
 
    def handleEvent(self,value):
        x=value.x;
        y=value.y;
        #print str(x)+" "+str(y);
        if(x<60 and y>20):
            if(y<53):
                #play/pause
                pass
            elif(y<86):
                #next
                self.prev();
            elif(y<120):
                self.next();
            elif(y<150):
                pass;
            elif(y<180):
                pass;
            else:
                pass;
        
    def updateScreen(self,fullUpdate=True):
        start=20;
        gap=18;
        if(fullUpdate or self.forceRefresh):
            self.forceRefresh=False;
            # draw background & buttons
            self.screen.blit(self.musicImage,(0,0));
            pygame.draw.line(self.screen,(0,0,150,200),(0,120),(320,120),2)
            self.screen.blit(self.buttonPlay,(0,20));
            self.screen.blit(self.buttonPrev,(0,53));
            self.screen.blit(self.buttonNext,(0,86));
            self.screen.blit(self.buttonLoad,(0,120));
            self.screen.blit(self.buttonSave,(0,150));
            self.screen.blit(self.buttonAdd,(0,180));
            self.screen.blit(self.buttonNew,(0,210));
            
            #song/artist/album etc.. infos
            self.screen.blit(self.cdImg,(65,25,75,75))
            self.drawText(self.meta['artist'],(0,250,0,200),(145,start));
            self.drawText(self.meta['album'],(150,150,250,200),(145,start+gap));
            self.drawText(self.meta['tracknumber']+": "+self.meta['title'],(250,50,50,200),(145,start+gap*2));
            self.drawText(self.meta['date'],(200,200,200,200),(145,start+gap*3));
            
            #TODO: show volume somewhere        
            self.main.paintMenuBar();        
            #playlist
            self.playlist.drawPane(self,(70,130));
        else:
            # clear the areas that need to refresh (progressbar & indicator);
            pygame.draw.rect(self.screen,(0,0,0,255),(145,start+gap*4,160,10));
            pygame.draw.rect(self.screen,(0,0,0,255),(70,105,240,11));
        
        # needs to be done wether full or light update
        # progress bar
        pygame.draw.line(self.screen,(100,100,100,200),(75,110),(305,110),10)
        pygame.draw.line(self.screen,(200,200,250,200),(75,110),(305,110),2)
        posX=75;
        length=self.meta['length'];
        progress=str(music.get_pos()/60000)+":"+str(music.get_pos()/1000%60)+" / --:--";
        if(length>0):
            if(music.get_busy()):
                posX=75+(305-75)/1000.0*music.get_pos()/length  
            progress=str(music.get_pos()/60000)+":"+str(music.get_pos()/1000%60)+" / "+str(int(length/60))+":"+str(int(length%60))
        pygame.draw.line(self.screen,(150,150,250,255),(posX,105),(posX,115),5)

        self.drawText(progress+"         Vol:50%",(200,100,200,200),(145,start+gap*4));

        pygame.display.flip();
    
    def drawText(self,text,color,startPos,cutoff=34):
        '''
        Draw a text at a location, splitting on 2 lines if too long
        '''
        (x,y)=startPos;
        text2=None;
        if(len(text)>cutoff):
            text2=text[cutoff:len(text)];
            text=text[0:cutoff];
        ln=self.font2.render(text,True,color);
        self.screen.blit(ln,(x,y));
        if(text2!=None):
            ln2=self.font2.render(text2,True,color);
            self.screen.blit(ln2,(x,y+8));
    
    def shutdown(self):
        music.stop();
        self.updater.shutdown();
        self.done=True;
    
    def selfTest(self):
        pass;
        
    def next(self):
        file=self.playlist.getNextSong();
        #print "next file: "+file;
        if(file!=None):
            self.play(file,self.findAlbumArt(file));
            
    def prev(self):
        file=self.playlist.getPrevSong();
        #print "prev file: "+file;
        if(file!=None):
            self.play(file,self.findAlbumArt(file));
    
    def findAlbumArt(self,song):
        albumdir=os.path.dirname(song);
        dirList=os.listdir(albumdir)
        for file in  dirList:
            for pattern in self.imgPatterns:
                if(file.lower().endswith(pattern)):
                    return os.path.join(albumdir,file);
        return None;
        
    def play(self,file,cdImage=None,pos=0.0):
        '''
        play a music file (file)
        show the cdImage(album art) if passed.
        '''
        print "Starting playback of: "+file;
        self.meta=self.parseMetadata(file);
        music.load(file);
        if(cdImage!=None):
            img=pygame.image.load(cdImage);
            self.cdImg=pygame.transform.scale(img, (75,75))
        else:
            self.cdImg=self.emptyCD;
        self.forceRefresh=True;
        music.play(0,pos);
        
    def parseMetadata(self,file):
        '''
        Parse music metadata using metagen
        '''
        meta = {"artist":"--","title":"--","tracknumber":"-","date":"","album":"--","length":0}
        muta = mutagen.File(file);
        meta["length"]=muta.info.length;        
        if(file.lower().endswith(".mp3")):
            muta = mutagen.easyid3.EasyID3(file);
        # Any of those tags might be missing/broken, so try/catch them one by one and get whatever we can without blowing up.
        try:
            meta["artist"]=muta["artist"][0];
        except Exception:
            meta["artist"]="--";
        try:
            meta["title"]=muta["title"][0];
        except Exception:
            meta["title"]="--";
        try:
            meta["album"]=muta["album"][0];
        except Exception:
            meta["album"]="--";
        try:
            meta["date"]=muta["date"][0];
        except Exception:
            meta["date"]="";
        try:
            meta["tracknumber"]=muta["tracknumber"][0];
        except Exception:
            meta["tracknumber"]="-";
        #print meta;
        return meta;

# End class

class PlayList:
    name=None;

    songs=[];
    patterns=[".ogg",".mp3"];
    index=-1;
    
    def __init__(self):
        self.songs=[];
        self.index=-1;
    
    def getNextSong(self):
        if(len(self.songs)>self.index+1):
            self.index=self.index+1;
            return self.songs[self.index];
        elif(len(self.songs)>0):
            self.index=0;
            return self.songs[0];
        return None;
 
    def getPrevSong(self):
        if(self.index>0):
            self.index=self.index-1;
        return self.songs[self.index];
    
    def addSingleFile(self, file):
        for pattern in self.patterns:
            if(file.lower().endswith(pattern)):
                self.songs.append(file);
                #print file
                break;
        
    def addFolder(self,folder,recursive=False):
        pass
        dirList=os.listdir(folder)
        if(not recursive):
            for file in  dirList:
                self.addSingleFile(os.path.join(folder, file));
        else:
            for root, dirs, files in os.walk( folder, True, None ):
                for name in files:
                    self.addSingleFile(os.path.join(root, name))
    
    def randomize(self):
        for i in range(0, len(self.songs)):
            # swap 2 songs
            j=random.randint(0,len(self.songs)-1);
            if(j!=i):
                tmp=self.songs[i];
                self.songs[i]=self.songs[j];
                self.songs[j]=tmp;
    
    def drawPane(self,main,pos):
        '''
        Draw the playlist view on the screen surface at pos location
        '''
        (x,y)=pos;
        start=self.index-2;
        if(start<0):
            start=0;
        end=start+5;
        nbSongs=len(self.songs)
        if(end > nbSongs):
            end = nbSongs
        if(end<0):
            end=0;
        for i in range(start, end):
            meta=main.parseMetadata(self.songs[i]);
            ln1=self.songs[i]
            ln2=""
            if(meta!=None):
                ln1=meta['artist']+" ["+meta['album']+"]"
                ln2=meta['tracknumber']+": "+meta['title']
            if(i==self.index):
                main.drawText(ln1,(0,250,0,200),(x,y),500);
                main.drawText(ln2,(0,250,0,200),(x,y+8),500);
            else:
                main.drawText(ln1,(250,250,0,200),(x,y),500);
                main.drawText(ln2,(250,250,0,200),(x,y+8),500);
            y+=20;
        

        
    def save(self,file):
        self.name=""
        
    def load(self, file, shuffle=False):
        self.name=""
        
# end playlist

class ScreenUpdater ( threading.Thread ):
    '''
    Thread to update the screen regularly
    '''
    done=False;
    loopDone=False;
    
    def __init__(self,main):
        threading.Thread.__init__ ( self );
        self.main=main;
        
    def run ( self ):
        while(not self.done):
            if(self.main.main.currentArea==self.main.main.PANE_MUSIC and music.get_busy()):
                self.main.updateScreen(False);
            pygame.time.delay(500);
        self.loopDone=True;
    
    def shutdown(self):
        self.done=True;
        while(not self.loopDone):
            time.sleep(.05);

#Test
pl=PlayList();
pl.addFolder("/media/extHD/Music/",True);

