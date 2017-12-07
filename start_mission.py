'''
This is the main file where the application begins.
'''
from mission_helper import setup_adhoc_network,create_log_file
import time
if __name__ == "__main__":
    create_log_file()
    print("Setting up network")
    start_time = time.time()
    setup_adhoc_network()
    print("Netowork setup done in",(time.time()-start_time),"Seconds")
