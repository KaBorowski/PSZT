from xml.dom import minidom


class Node:
    def __init__(self, uid, x, y):
        self.uid = uid
        self.x = x
        self.y = y
        self.linklist = []
        self.demandlist = []


class Link:
    def __init__(self, uid, source, target, capacity):
        self.uid = uid
        self.source = source
        self.target = target
        self.capacity = capacity


class Demand:
    def __init__(self, uid, source, destination, demandValue):
        self.uid = uid
        self.source = source
        self.destination = destination
        self.demandValue = demandValue


class Network:
    def __init__(self, net="polska.xml"):
        self.net = net

    def get_Network(self):
        Read_Data = minidom.parse(self.net)
        nodemap = {}

        nodelist = Read_Data.getElementsByTagName("node")
        for node in nodelist:
            if node.hasAttribute("id"):
                Nodeid = node.getAttribute("id")
            xCoordinates = node.getElementsByTagName('x')[0]
            xCoordinates = xCoordinates.childNodes[0].data
            yCoordinates = node.getElementsByTagName('y')[0]
            yCoordinates = yCoordinates.childNodes[0].data
            nodemap[Nodeid] = Node(Nodeid, xCoordinates, yCoordinates)
            print ("%s : %s %s" % (node.getAttribute("id"), xCoordinates, yCoordinates))

        linklist = Read_Data.getElementsByTagName("link")
        for link in linklist:
            if link.hasAttribute("id"):
                Linkid = link.getAttribute("id")
            Source = link.getElementsByTagName('source')[0]
            Source = Source.childNodes[0].data
            Destination = link.getElementsByTagName('target')[0]
            Destination = Destination.childNodes[0].data
            Capacity = link.getElementsByTagName('capacity')[0]
            Capacity = Capacity.childNodes[0].data
            linkobj = Link(Linkid, Source, Destination, Capacity)
            if Source in nodemap:
                nodemap[Source].linklist.append(linkobj)
            if Destination in nodemap:
                nodemap[Destination].linklist.append(linkobj)

            print("%s - %s to %s: %s" % (
            link.getAttribute("id"), Source, Destination, Capacity))
        demandlist = Read_Data.getElementsByTagName("demand")
        for demand in demandlist:
            if demand.hasAttribute("id"):
                Demandid = demand.getAttribute("id")
            Source = demand.getElementsByTagName('source')[0]
            Source = Source.childNodes[0].data
            Destination = demand.getElementsByTagName('target')[0]
            Destination = Destination.childNodes[0].data
            Demandval = demand.getElementsByTagName('demandValue')[0]
            Demandval = Demandval.childNodes[0].data
            demandobj = Demand(Demandid, Source, Destination, Demandval)
            if Source in nodemap:
                nodemap[Source].demandlist.append(demandobj)
            if Destination in nodemap:
                nodemap[Destination].demandlist.append(demandobj)

            print ("%s needs %s" % (demand.getAttribute("id"), Demandval))
        return nodemap
