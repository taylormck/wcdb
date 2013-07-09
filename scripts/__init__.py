import sys, os
path = [os.path.join(os.getcwd(),"..")]
if path not in sys.path:
    sys.path += path
