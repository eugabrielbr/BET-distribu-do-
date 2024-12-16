import signal
from time import sleep

def signal_handler(sig, frame):
    print("aq!!")

signal.signal(signal.SIGINT, signal_handler)
    
while True:
    
    print("oi")
    
    sleep(1)