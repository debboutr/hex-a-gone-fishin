'''
Purpose:

References:
1) https://arcpy.wordpress.com/2012/11/15/shifting-features/
2) http://desktop.arcgis.com/en/arcmap/10.5/analyze/arcpy-data-access/updatecursor-class.htm
3) http://desktop.arcgis.com/en/arcmap/latest/tools/data-management-toolbox/recalculate-feature-class-extent.htm
4) http://desktop.arcgis.com/en/arcmap/10.5/tools/data-management-toolbox/copy-features.htm
5) http://desktop.arcgis.com/en/arcmap/10.5/tools/analysis-toolbox/intersect.htm

'''


# Imports
import arcpy
arcpy.env.overwriteOutput = True
import glob
import timeit
import os

# Initial time
initialTic = timeit.default_timer()

# Variables
directory = "L:\\Public\\jhalama\\HexSim\\HexSimLeafletDevelopment\\"
# directory = "E:\\Projects\\Columbia\\Columbia_S2M\\ArcMapSide\\HexSimExportedSubsetting\\"
#inputFolder = "HexSimGeneratedShapefiles"
# inputFolder = "Testing\\UpdatedZone6"
inputFolder = "InputShps\\"
outputClipLocation = "OutputShps\\"

# Offsets           , added shifts to match the test reach.
x_shift = -2138522 + 2.463 + 0.012105 -0.024205
y_shift = 2764454 + 8.384 + 0.01873

# Access all the shapefiles to process using Glob library. Only the shapefiles (*.shp) in the folder are added to list
inputFolder = directory + inputFolder + "\\"
filesToProcess = glob.glob1(inputFolder, '*.shp')

# Loop over the files to process.
for eachFile in filesToProcess:
    # Timer
    tic=timeit.default_timer()
    print "Starting to work on " + eachFile
    
    # Build a full filepath to the next shapefile to process.
    in_features = inputFolder + eachFile
    # Loop through all the data in the shapefile updating the SHAPE@XY object.
    rowsFixed = 0
    with arcpy.da.UpdateCursor(in_features, ['SHAPE@XY']) as cursor:
        for row in cursor:
            cursor.updateRow([[row[0][0] + (x_shift or 0), row[0][1] + (y_shift or 0)]])
            # Row Incrementor.
            rowsFixed = rowsFixed + 1
    # Update on the completion of processing this shapefile.
    print "Updated vector coordinates for " + eachFile + " to the new position of x_shift: " + str(x_shift) + " and y_shift: " + str(y_shift) + "."
    # Update the shapefiles extent.
    arcpy.RecalculateFeatureClassExtent_management(in_features)
    print "Updated extent information for " + eachFile + "."  
    
    # Timer
    print "Done processing " + in_features
    toc = timeit.default_timer()
    elapsedTime = toc - tic
    if (elapsedTime < 60):
        print "Current file processing time: " + str(elapsedTime) + " seconds."
    else:
        elapsedMinutes = int(elapsedTime/60)
        elapsedSeconds = elapsedTime - (elapsedMinutes*60)
        print "Current file processing time: " + str(elapsedMinutes) + " minutes, and " + str(elapsedSeconds) + " seconds."

# Final statement claiming code is done.
print "Done working on provided shapefiles, and all downstream selected tasks."
finalToc = timeit.default_timer()
totalElapsedTime = finalToc - initialTic
if (totalElapsedTime < 60):
    print "Current file processing time: " + str(totalElapsedTime) + " seconds."
else:
    elapsedMinutes = int(totalElapsedTime/60)
    elapsedSeconds = totalElapsedTime - (elapsedMinutes*60)
    print "Current file processing time: " + str(elapsedMinutes) + " minutes, and " + str(elapsedSeconds) + " seconds."
