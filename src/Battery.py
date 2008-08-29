import struct;
from array import array

class Battery:
    '''
    Handles retrieveing the battery level of the GP2X
    '''
    def __init__(self,container):
        self.BATT_LEVEL_HIGH=0
        self.BATT_LEVEL_MID=1
        self.BATT_LEVEL_LOW=2
        self.BATT_LEVEL_EMPTY=3
        self.SamplesPerLoop=5;
        
    def getValue(self):
        ''' 
        return -1 if value not avail.
        otherwise 0=full 3=empty 1=good, 2=bad
        '''
        self.f100=False;
        try:
            f=open('/dev/batt', 'rb');
            self.f100=True;
        except IOError:
            self.f100 = False;
        self.f200=False;
        if(not self.f100):
            try:
                f=open('/dev/mmsp2adc', 'rb');
                self.f200=True;
            except IOError:
                self.f200 = False;

        value=-1;
        # for f100, more accurate reading
        if(self.f100):
            value=0;
            data = array('h')
            data.fromfile(f, self.SamplesPerLoop)

            for v in data:
                value += v;
            value /= self.SamplesPerLoop
            if (value>=780):
                value=self.BATT_LEVEL_HIGH
            elif (value>=740):
                value=self.BATT_LEVEL_MID
            elif (value>=690):
                value=self.BATT_LEVEL_LOW
            else:
                value=self.BATT_LEVEL_EMPTY

        # f200 : 0 to 3 reading
        if(self.f200):
        # what the heck is remocon ??
            (value,remocon)=struct.unpack('hh', f.read(4));
    
        if(self.f100 or self.f200):
            f.close();

        return value;
        
