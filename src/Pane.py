import threading;
import time;

class Pane(threading.Thread):
    '''
    "Abstract" class representing one of the applications "panel".
    '''
    
    def __init__(self):
        self.done=False;
        threading.Thread.__init__(self);

    def run(self):
        while(not self.done):
            time.sleep(.1);
    
    def shutdown(self):
        self.handleShutdown();
        self.done=True;
 
# To be implemented by subclass :       
    def __updateScreen__():
        '''
        Update screen pane
        '''
    def __handleEvent__():
        '''
        Handle a (touchscreen) event
        '''        
    def __handleShutdown__():
        '''
        Handle shutdown request
        '''        
    
