'''
This is the main file where the application begins.
'''
from mission_helper import setup_adhoc_network,create_log_file
import time
import os
#TODO: Fix this clean up of resources.
def cleanUpResources():
    print("cleaning the file")
    os.remove(os.getcwd()+"/start_communication.txt")
if __name__ == "__main__":
    try:
        create_log_file()
        print("Setting up network")
        start_time = time.time()
        setup_adhoc_network()
        print("Network setup done in",(time.time()-start_time),"Seconds")
    #TODO keyboard exception
    except KeyboardInterrupt as k:
        cleanUpResources()
