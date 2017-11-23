'''
This is the main file where the application begins.
'''
from mission_helper import setup_adhoc_network,create_log_file
if __name__ == "__main__":
    create_log_file()
    print("Setting up network")
    setup_adhoc_network()
