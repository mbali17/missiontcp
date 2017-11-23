'''
This is the helper module for the mission.Consisting of the utility methods.
'''
import time

from network_entity import NetworkEnity
import logging

def setup_adhoc_network():
    #get main logger
    app_logger = logging.getLogger("main_logger")
    with open("network_entities.csv","r") as entities:
        app_logger.info("Reading entities file.")
        #Skip the first line.
        next(entities)
        #Start each entity in the network as a separate thread.Each entity is started after 5 seconds.
        for entity in entities:
            app_logger.info("Starting entity "+entity)
            entityThread = NetworkEnity(entity_details = entity)
            entityThread.start()
            app_logger.info("Sleeping for 5 seconds")
            #Sleep for 5 seconds before adding the new entity.
            time.sleep(5)
"""
    Creates a logger with a given logger name file name.
    Reference: https://stackoverflow.com/a/17037016/6765884
"""
def create_log_file(log_name = "mission_tcp.log",logger_name = "main_logger"):
    #Create Logger. This is the main logger for the application.
    logger = logging.getLogger(logger_name)
    #set loglevel
    logger.setLevel(logging.INFO)
    #create formatter for the log.
    logging_formatter = logging.Formatter('%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    #set the file to which the logs are to be written.
    logging_file_handler = logging.FileHandler("logs/"+log_name)
    logging_file_handler.setFormatter(logging_formatter)
    logger.addHandler(logging_file_handler)
    return logger


def calcualte_shortest_path():
    print("calulating shortest path.")

