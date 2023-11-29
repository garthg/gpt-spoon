import os

from guts import mainloop


# TODO: whitelist this or something
if os.environ['USER'] != 'somebodyelse':
    # always fail here unrecoverably
    diediediediediediediediediedie
    


mainloop.run_once()
    
