'''
This class defines the structure of the TCP packet.
'''

class TcpPacket():
    def __init__(self,sourceID,destinationID,sequenceNumber,acknowledgement,
                 headerLength,reciever_window,checksum,urgentpointer,data,
                 drp=0,ter=0,urg=0,ack=0,rst=0,syn=0,fin=0):
        print("Constructing TCP  packet")
        #TODO : provide getters for this property.
        self.sourceID = sourceID
        self.destinationID = destinationID
        self.sequenceNumber = sequenceNumber
        self.acknowledgement = acknowledgement
        self.headerLength = headerLength
        self.drp = drp
        self.ter = ter
        self.urg = urgentpointer
        self.ack = acknowledgement
        self.rst = rst
        self.syn = syn
        self.fin = fin
        self.reccieve_Window = reciever_window
        self.checksum = checksum
        self.urgentpointer = urg
        self.data=data
