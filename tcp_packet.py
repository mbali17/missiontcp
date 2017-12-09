'''
This class defines the structure of the TCP packet.
'''
#mir basheer ali(1001400462) neerja narayannapa (1001575625)
class TcpPacket():
    def __init__(self,sourceID,destinationID,sequenceNumber,acknowledgement,
                 headerLength,reciever_window,checksum,urgentpointer,data,
                 drp=0,ter=0,urg=0,ack=0,rst=0,syn=0,fin=0):
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
        self.urgentpointer = urgentpointer
        self.data=data
    #getters for the properties.
    @property
    def getSourceID(self):
        return self.sourceID
    @property
    def getDestinationport(self):
        return self.destinationID
    @property
    def getSequenceNumber(self):
        return self.sequenceNumber
    @property
    def getAcknowledgement(self):
        return self.acknowledgement
    @property
    def getHeaderLength(self):
        return self.headerLength
    @property
    def getDrp(self):
        return self.drp
    @property
    def getTer(self):
        return self.ter
    @property
    def getUrg(self):
        return self.urg
    @property
    def getAck(self):
        return self.ack
    @property
    def getRst(self):
        return self.rst
    @property
    def getSyn(self):
        return self.syn
    @property
    def getFin(self):
        return self.fin

    @property
    def getReciever_window(self):
        return self.reccieve_Window
    @property
    def getCheckSum(self):
        return self.checksum
    @property
    def getUrgentPointer(self):
        return self.urgentpointer
    @property
    def getData(self):
        return self.data



