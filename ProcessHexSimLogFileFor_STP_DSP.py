# -*- coding: utf-8 -*-
"""
@author: Jonathan Halama
@date: 25 March, 2019
@purpose: Locations fish movements from HexSim Lof file.
"""
import os
import time
starttime = time.time()

def findHexSimSTPandDSP (hexSimLogFile, newHexSimLogFile):
    myInputFile = open(hexSimLogFile, 'r')
    myNewFile = open(newHexSimLogFile, 'w')

    # Read each line in the log file.
    for line in myInputFile:
        # 
        lineInfo = line.split(",")
        
        if (lineInfo[0] == "STP"):
            # New model timestep.
            myNewFile.write(line)

        if (lineInfo[0] == "DSP"):
            myNewFile.write(line)
        
###### User inputs ######
myFilepath = "C:\\Users\\Jonat\\Desktop\\CWR_LeafletMaps\\TEST.log"
filesize = os.path.getsize(myFilepath)
newHexSimLogFile = ("C:\\Users\\Jonat\\Desktop\\CWR_LeafletMaps\\smalllerTEST.log")

findHexSimSTPandDSP(myFilepath, newHexSimLogFile)

totaltime = time.time() - starttime

minutes = 0
seconds = 0

if (totaltime > 60):
    minutes = int(totaltime/60)
    seconds = int(totaltime - (minutes*60))
    '{:2d}'.format(seconds)
    

print ("Done isolating fish and steps. Processing took: " + str(minutes) + "minutes and " + str(seconds) + " seconds to process the HexSim log file of size: " + str(filesize) + " KB. You are welcome.")





















