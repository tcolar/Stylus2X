import struct;
import time;
import pygame;

class TSValue:
    ts=0;
    pressure=0;
    x=0;
    y=0;
    pad=0;

    def __init__(self,pressure,x,y,pad,ts):
        self.x=x;
        self.y=y;
        self.pressure=pressure;
        self.pad=pad;
        self.ts=ts;

class TouchScreen:
    
    def __init__(self,container):
        self.screen=container;
        self.mouseX=0;
        self.mouseY=0;
        self.mousePressure=0;
        self.onGP2X=True;
        try:
            f=open('/dev/touchscreen/wm97xx', 'rb');
        except IOError:
            self.onGP2X = False;
        if(self.onGP2X):
            f.close();
                
    def readTSValue(self):
        # process std events, so mouse etc... values gets updated
        self.handleEvents();
        
        if(self.onGP2X):
            f=open('/dev/touchscreen/wm97xx', 'rb');  # for testing on "real" PC
            # C format of dev file uint16_t(H),uint16_t(H),uint16_t(H),uint16_t(H),(long(i),long(i))
            # 2B, 2B, 2B ,2B, 4B, 4B => 16B
            (pressure, x, y, pad, ts1, ts2) = struct.unpack('HHHHii', f.read(16));
            # ts is timestamp in ms.
            ts=ts1*1000000+ts2/1000;
            screenX = (x - 200) * 320 / 3750;
            screenY = 240 - ((y - 200) * 240 / 3750);
            value=TSValue(pressure,screenX,screenY,pad,ts);
            f.close();
        else:
            # create "fake" TouchScreen value using mouse location/click
            value=TSValue(self.mousePressure,self.mouseX,self.mouseY,0,0);
        return value;
            
    def handleEvents(self):
        self.mousePressure=0;
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mousePressure=500;
                (self.mouseX, self.mouseY)=pygame.mouse.get_pos();
    
# End class
