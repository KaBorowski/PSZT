import sys
import xml.dom.minidom as dom
import string
from xml.dom import minidom
from xml.dom.minidom import parse
import os
Read_Data = minidom.parse("polska.xml")
nodelist = Read_Data.getElementsByTagName("node")

class Node:
    def __init__(self,uid,x,y):
        self.uid=uid
        self.x=x
        self.y=y
        self.linklist=[]
        self.demandlist=[]

class Link:
    def __init__(self,uid,source,target,capacity):
        self.uid=uid
        self.source=source
        self.target=target
        self.capacity=capacity

class Demand:
    def __init__(self,uid,source,destination,demandValue):
        self.uid=uid
        self.source=source
        self.destination=destination
        self.demandValue=demandValue


nodemap={}

for node in nodelist :
    if node.hasAttribute("id"):
        Nodeid = node.getAttribute("id")
    xCoordinates = node.getElementsByTagName('x') [0]
    yCoordinates = node.getElementsByTagName('y') [0]
    nodemap[Nodeid]=Node(Nodeid,xCoordinates,yCoordinates)
    print ("%s : %s %s" %(node.getAttribute("id"), xCoordinates.childNodes[0].data, yCoordinates.childNodes[0].data))

linklist = Read_Data.getElementsByTagName("link")
for link in linklist :
    if link.hasAttribute("id"):
        Linkid = link.getAttribute("id")
    Source = link.getElementsByTagName('source') [0]
    Destination = link.getElementsByTagName('target') [0]
    Capacity = link.getElementsByTagName('capacity') [0]
    linkobj= Link(Linkid,Source,Destination,Capacity)
    if Source in nodemap:
        nodemap[Source].linklist.append(linkobj)
    if Destination in nodemap:
        nodemap[Destination].linklist.append(linkobj)

    print( "%s - %s to %s: %s" %(link.getAttribute("id"), Source.childNodes[0].data, Destination.childNodes[0].data, Capacity.childNodes[0].data))
demandlist = Read_Data.getElementsByTagName("demand")
for demand in demandlist :
    if demand.hasAttribute("id"):
        Demandid = demand.getAttribute("id")
    Source = demand.getElementsByTagName('source') [0]
    Destination = demand.getElementsByTagName('target') [0]
    Demandval = demand.getElementsByTagName('demandValue') [0]
    demandobj=Demand(Demandid,Source,Destination,Demandval)
    if Source in nodemap:
        nodemap[Source].demandlist.append(demandonj)
    if Destination in nodemap:
        nodemap[Destination].demandlist.append(demandobj)

    print ("%s needs %s" %(demand.getAttribute("id"), Demandval.childNodes[0].data))




print (nodemap)