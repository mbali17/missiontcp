'''
This is the helper module for the mission.Consisting of the utility methods.
'''
import time
import sys
#from network_entity import NetworkEnity
import logging
from collections import defaultdict
from heapq import *


def setup_adhoc_network():
    #get main logger
    app_logger = logging.getLogger("main_logger")
    with open("network_entities.csv","r") as entities:
        app_logger.info("Reading entities file.")
        # Skip the first line.
        next(entities)
        # Start each entity in the network as a separate thread.Each entity is started after 5 seconds.
        for entity in entities:
            app_logger.info("Starting entity "+entity)
            entityThread = NetworkEnity(entity_details = entity)
            entityThread.start()
            app_logger.info("Sleeping for 5 seconds")
            #Sleep for 5 seconds before adding the new entity.
            time.sleep(5)

        with open("start_communication.txt","w") as sync_file:
            sync_file.write("Start_communication")
            sync_file.close()
        print("Communication to begin in a while")
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
    #set the file to which the logs are to be written.e
    logging_file_handler = logging.FileHandler("logs/"+log_name)
    logging_file_handler.setFormatter(logging_formatter)
    logger.addHandler(logging_file_handler)
    return logger

"""
Implements Djikstras to find the shortest. Writes the result to a single or agent specific file.
"""
orig_stdout = sys.stdout
f = open('dijkstra.csv', 'w')
sys.stdout = f

def dijkstra(edges, f, t):
    g = defaultdict(list)
    for l,r,c in edges:
        g[l].append((c,r))

    q, seen = [(0,f,())], set()
    while q:
        (cost,v1,path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 == t: return (cost, path)

            for c, v2 in g.get(v1, ()):
                if v2 not in seen:
                    heappush(q, (cost+c, v2, path))

    return float("inf")

# TODO: 
if __name__ == "__main__":
    edges = [
        ("111", "8000", 0),
	("8000", "111", 0),
        ("8000", "8001", 4),
	("8001", "8000", 4),
        ("8000", "8002", 3),
	("8002", "8000", 3),
        ("8000", "8004", 7),
	("8004", "8000", 7),
	("8001", "8002", 6),
	("8002", "8001", 6),
        ("8001", "8007", 5),
	("8007", "8001", 5),
        ("8002", "8003", 11),
	("8003", "8002", 11),
        ("8003", "8007", 9),
	("8007", "8003", 9),
	("8003", "8005", 6),
	("8005", "8003", 6),
	("8003", "8006", 10),
	("8006", "8003", 10),
        ("8004", "8006", 5),
	("8004", "8006", 5),
	("8004", "200", 0),
        ("200", "8004", 0),
        ("8005", "8007", 5),
	("8007", "8005", 5),
	("100", "8005", 0),
	("8005", "100", 0 ),
    ]

    print ("=== Dijkstra ===")
    print ("Ann -> Chan:")
    print (dijkstra(edges, "111", "200"))
    print ("Chan -> Ann:")
    print (dijkstra(edges, "200", "111"))

    print ("Chan -> Jan:")
    print (dijkstra(edges, "200", "100"))
    print ("Jan -> Chan:")
    print (dijkstra(edges, "100", "200"))

    print ("Jan -> Ann:")
    print (dijkstra(edges, "100", "111"))
    print ("Ann -> Jan:")
    print (dijkstra(edges, "111", "100"))

sys.stdout = orig_stdout
f.close()
