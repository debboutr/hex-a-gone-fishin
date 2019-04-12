# -*- coding: utf-8 -*-
"""
@author: Jonathan Halama
@date: 25 March, 2019
@purpose: Locations fish movements from HexSim Lof file.
"""
import os
import time
starttime = time.time()

def findFish (hexSimLogFile, desiredHexIds):
    FishDictionary = {}                     # Empty dictionary. Returned Object.
    myInputFile = open(hexSimLogFile, 'r')  # Open the file as a FileObject.
    step = 0                                # Step is advanced at first STP event, so presumed that HexSim's first step is "1".
    # Read each line in the log file.
    for line in myInputFile:
        lineInfo = line.split(",")          # Parse the line by comma.
        
        # Check if the current lines event is a DSP event.
        if (lineInfo[0] == "STP"):
            step = step + 1                 # New model timestep.
            FishDictionary[step] = {}       # Add new empty dictionary with time step as the key.
        '''
        Log Key for DSP Events:
        0 DSP (Dispersal Data Record)
        1 Field: Current Replicate
        2 Field: Current Step
        3 Field: Population ID
        4 Field: Individual ID
        5 Field: Trait Index
        6 Field: Hexagons Dispersed
        7 Field: Meters Displaced
        8 Field: Hexagons Listed
        9 Field: Dispersal Origin
        10 Field: Dispersed Hexagons ...
        Example:
        Index: 0,  1,2,3,   4,              5, 6,        7, 8,      9,     10
        #      DSP,1,7,3,1596,302537491320680,74,1506.5072,75,2987006,2976812,2976813,...
        '''
        
        # Check if the current lines event is a DSP event.
        if (lineInfo[0] == "DSP"):
            littleFishy = int(lineInfo[4])  # Grab the fish ID from this line.
            
            # Grab HexIDs; then check for any matches to CWR hexagons.
            hexsTravelledInCWR = []
            i = 10
            while (i < len(lineInfo)):
                # 
                value = int(lineInfo[i])
                if (value in desiredHexIds):
                    # 
                    hexsTravelledInCWR.append(int(lineInfo[i]))
                    # print ("Appended CWR ID!")
                i=i+1
            
            #
            if (len(hexsTravelledInCWR) > 0):
                # Need to check if the fish is in dictionary or not, and add as needed.
                if(littleFishy in FishDictionary[step]):
                    #
                    hexTravel = FishDictionary[step][littleFishy]
                    hexTravel = hexTravel + hexsTravelledInCWR
                    #print ("MATCH to fish in DICT")
                    #print (FishDictionary[step][littleFishy])
                    '''
                    i=0
                    while (i < len(hexsTravelledInCWR)):
                        hexToAdd = hexsTravelledInCWR[i]
                        hexTravel.append(hexToAdd)
                        i=i+1
                    '''
                    #
                    FishDictionary[step][littleFishy] = hexTravel
                    
                # Else means for the current time-step the current fish ID has not been added yet.                    
                else:
                    FishDictionary[step][littleFishy] = hexsTravelledInCWR
            
    FinalFishDictionary = {} 
    priorLen = len(FishDictionary)
    # Clear all steps with no information.
    for steps in FishDictionary:
        # 
        dictionary = FishDictionary[steps]
        if bool(dictionary):
            FinalFishDictionary[steps] = dictionary
    
    # Updates
    finalLen = len(FinalFishDictionary)
    print ("FishDictionary was length: " + str(priorLen) + ".")
    print ("FishDictionary is now length: " + str(finalLen) + ".")
                
    # Returning a nested list of fish events. 
    return FinalFishDictionary



def findCwrTemps(thermalFile, desiredColumbia, desiredCWR_stream, desiredCWR_plume1, desiredCWR_plume2):
    doneColumbia = False
    doneStream = False
    donePlume1 = False
    donePlume2 = False
    thermalDataColumbia = []
    thermalDataStream = []
    thermalDataPlume1 = []
    thermalDataPlume2 = []
    
    myInputFile = open(thermalFile, 'r')  # Open the file as a FileObject.
    
    # Read each line in the log file.
    for line in myInputFile:
        lineInfo = line.split(",")          # Parse the line by comma.
        
        # 
        if (doneColumbia == False or doneStream == False or donePlume1 == False or donePlume2 == False):
            # Check if the current line is the desiredColumbia.
            if (lineInfo[0] == desiredColumbia):
                # 
                doneColumbia = True
                thermalDataColumbia = []
                i = 1
                while (i < len(lineInfo)):
                    thermalDataColumbia.append(float(lineInfo[i]))
                    i=i+1
                    
            # Check if the current lines event is a DSP event.
            if (lineInfo[0] == desiredCWR_stream):
                # 
                doneStream = True
                thermalDataStream = []
                i = 1
                while (i < len(lineInfo)):
                    thermalDataStream.append(float(lineInfo[i]))
                    i=i+1
                    
            # Check if the current lines event is a DSP event.
            if (lineInfo[0] == desiredCWR_plume1):
                #
                donePlume1 = True
                thermalDataPlume1 = []
                i = 1
                while (i < len(lineInfo)):
                    thermalDataPlume1.append(float(lineInfo[i]))
                    i=i+1
                    
            # Check if the current lines event is a DSP event.
            if (lineInfo[0] == desiredCWR_plume2):
                #
                donePlume2 = True
                thermalDataPlume2 = []
                i = 1
                while (i < len(lineInfo)):
                    thermalDataPlume2.append(float(lineInfo[i]))
                    i=i+1
                    
    myInputFile.close()
                    
    # Returns two lists: 1) all the thermal data matching stream zone of the CWR, 2) all the thermal data mathcing the plume of the CWR.
    return thermalDataColumbia, thermalDataStream, thermalDataPlume1, thermalDataPlume2

'''
'''
def loadDesiredHexIds (hexFile):
    hexagons = []
    myInputFile = open(hexFile, 'r')  # Open the file as a FileObject.
    myInputFile.readline()
    # Read each line in the hexagon file.
    for line in myInputFile:
        lineInfo = line.split(",")          # Parse the line by comma.
        value = int(lineInfo[0])
        # stripLineInfo = int(value.strip(value))
        hexagons.append(value)
        
    return hexagons
        
###### User inputs ######
hexSimSimulationFilepath = "C:\\Users\\Jonat\\Desktop\\Python\\LeafletMapping\\smallerTEST.log"
hexsFilePath = "C:\\Users\\Jonat\\Desktop\\Python\\LeafletMapping\\HermanCreek_Hexs_SMALLER.csv"
thermalFilePath = "C:\\Users\\Jonat\\Desktop\\Python\\LeafletMapping\\thermal_patch_temp.csv"


# grab the file for fun. Not really needed though. If removed, fix final statement at end of code.
filesize = os.path.getsize(hexSimSimulationFilepath)

# Load the hexagons related to the currect CWR of interest.
hexagons = loadDesiredHexIds(hexsFilePath)

# Get the temperature data related to the CWR.
columbia = "ColJD"
stream = "Herman_filled"
plume1 = "HermanPMax"
plume2 = "HermanPMax"

thermalDataColumbia, thermalDataStream, thermalDataPlume1, thermalDataPlume2 = findCwrTemps(thermalFilePath, columbia, stream, plume1, plume2)

print ("Length of list is: " + str(len(thermalDataColumbia)))
print ("Length of list is: " + str(len(thermalDataStream)))
print ("Length of list is: " + str(len(thermalDataPlume1)))
print ("Length of list is: " + str(len(thermalDataPlume2)))

# Call the fish finder.
FinalFishDictionary = findFish(hexSimSimulationFilepath, hexagons)


# Count the number of fish found in the CWR.
singleFishSteps = 0
doubleFishSteps = 0
moreThan2FishSteps = 0

for steps in FinalFishDictionary:
    thisDictionary = FinalFishDictionary[steps]
    if (len(thisDictionary) == 1):
        singleFishSteps = singleFishSteps + 1
    if (len(thisDictionary) == 2):
        doubleFishSteps = doubleFishSteps + 1
    if (len(thisDictionary) > 2):
        moreThan2FishSteps = moreThan2FishSteps + 1

print ("Time steps with a single fish was: " + str(singleFishSteps) + ".")
print ("Time steps with a two fish was: " + str(doubleFishSteps) + ".")
print ("Time steps with more than two fish was: " + str(moreThan2FishSteps) + ".")

# Timing Code.
totaltime = time.time() - starttime
minutes = 0
seconds = 0
if (totaltime > 60):
    minutes = int(totaltime/60)
    seconds = int(totaltime - (minutes*60))
    '{:2d}'.format(seconds)
else:
    seconds = int(totaltime)
    '{:2d}'.format(seconds)
    
print ("Done. FishFinder took: " + str(minutes) + " minutes and " + str(seconds) + " seconds to process the HexSim log file of size: " + str(filesize) + " KB. You are welcome.")











 








