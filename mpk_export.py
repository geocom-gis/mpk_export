#-------------------------------------------------------------------------------
# Name:        mpk_export.py
# Purpose:     Find all the map documents that reside in a specified folder and
#              create tile packages for each map document.
#
# Author:      Geocom Informatik AG
#
# Created:     07.11.2018
# Copyright:   (c) Geocom Informatik AG 2018
#-------------------------------------------------------------------------------
import os, stat, sys, shutil
import arcpy
import datetime
import argparse

def createLogfile(logDir, logName):
    """
    Creates a logfile in the given directory with the given name.
    Needs:
        logDir:  The directory where the logfile will be stored
        logName: The Name of the log file. Nameing pattern [date]__[logName]
    """
    logFile = open(logDir + "\\" + str(datetime.date.today()) +"__" + logName, "w")
    logFile.write("Map package export log - " + str(datetime.date.today()))
    logFile.write("\n------------------------------------\n")

    return logFile

def writeLog(logFile, exception, error_count, mxd):
    """
    Writes an error message into a logfile.
    Needs:
        logFile:     an open file
        exception:   the error message to write into the file
        error_count: the number of error during processing
        mxd:         the name of the mxd file that caused the error
    """
    logLines = ["#################\n", "Error number: " + str(error_count) +"\n", "Caused by: " + mxd + "\n", "Message:\n" , str(exception), "\n"]
    logFile.writelines(logLines)

def closeLog(logFile, error_count):
     """
     Writes an end message into the given logfile and closes it.
     Needs:
         logFile:     an open file
         error_count: the number of errors during processing
      """
     if error_count == 0:
        print("-------")
        print("All map packages successfully created.")
        logFile.write("CONGRATULATIONS! No erros occured during processing." )
     elif error_count == 1:
        print("-------")
        print("An error occured during packaging. Refer to the logfile for detailed information.")
     elif error_count == -1:
        print("-------")
        print("There are no MXD in the given input directory!")
        logFile.write("The given input directory was empty! Thus no mpk could be exported.")
     else:
        print("-------")
        print(str(error_count) + " errors occured during packaging. Refer to the logfile for detailed information.")
     logFile.close()

def checkDirectory(path):
    """
    Checks if a directory does exist. If not, tries to create it.
    Needs:
        path: the path to be checked
    """
    if os.path.exists(path):
        if not os.path.isdir(path):
            path = raw_input("The given input refers to a file. Please provide the path only:  ")
            checkDirectory(path)
    else:
        try:
            print("The given diretory does not exist. Trying to create it:")
            os.makedirs(path)
            print("Directory successfully created!")
        except Exception as e:
            print("ERROR while creating directory. Error message: \n")
            print e

def remove_readonly(func, path, _):
    """
    Changes read-only files to writable so they can be deleted by shutil
    Needs:
        func: the function to be called after the permission changed
        path: the path of the file to be changed
    """
    "Clear the readonly bit and reattempt the removal"
    os.chmod(path, stat.S_IWRITE)
    func(path)

def mpkExport(arguments):
    """
    Goes through the list of mxds in the given directory and tries to export them as mpks.
    Needs:
        arguments: the list of arguments from the parser in main()
    """
    workspace = arguments.inDir
    output = arguments.outDir
    logDir = arguments.logDir
    logName = arguments.logName
    error_count = 0
    # Set environment settings
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = workspace
    mxdlist = arcpy.ListFiles("*.mxd")
    # Create a logfile
    log = createLogfile(logDir, logName)

    if len(mxdlist)< 1:
        error_count -= 1
    else:
        # Loop through the workspace, find all the mxds and create a map package using the same name as the mxd
        for mxd in mxdlist:
            print("Packaging " + mxd)
            outPath = output + '\\' + os.path.splitext(mxd)[0]
            try:
                arcpy.PackageMap_management(mxd, outPath + '.mpk', "PRESERVE", "CONVERT_ARCSDE", "#", "ALL", "RUNTIME")
                print("SUCCESS: " + mxd + " processed successfully.")
                # if a packaging folder was created, it will be removed
                if os.path.exists(outPath):
                    try:
                        shutil.rmtree(outPath, onerror=remove_readonly)
                    except Exception as e:
                        error_count += 1
                        writeLog(log, e, error_count, mxd)
                        print("Removal of package directory " + outPath + " failed. Consider running the script with administrator permissions.")
            except Exception as e:
                error_count += 1
                writeLog(log, e, error_count, mxd)
                print("ERROR while processing " + mxd)

    # close the Logfile
    closeLog(log, error_count)

def main():
    """
    Defines and parses the arguments of the given module. Invokes mpkExport.
    """
    parser = argparse.ArgumentParser(description="MPK export tool V1.0")
    parser.add_argument("-s", "--silent", help="use to prevent user interaction. If no paths are given (see -i, -o, -l), the path of this script will be used for either path. ", action="store_true")
    parser.add_argument("-i", "--inDir", metavar="", type=str, help="the directory where the mxds are stored. Asks for user interaction if not set.", default=None)
    parser.add_argument("-o", "--outDir", metavar="", type=str, help="the directory where the mpks will be exported to. Asks for user interaction if not set.",default=None)
    parser.add_argument("-l", "--logDir", metavar="", type=str, help="the directory where the logfile will be created. Asks for user interaction if not set.",default=None)
    parser.add_argument("-ln", "--logName", metavar="", type=str, help="the name of the logfile (default: [date]__mpk_export.log)",default="mpk_export.log")
    arguments = parser.parse_args()

    if arguments.silent:
        if arguments.inDir == None:
            arguments.inDir = sys.path[0]
        if arguments.outDir == None:
            arguments.outDir = sys.path[0]
        if arguments.logDir == None:
            arguments.logDir = sys.path[0]
    else:
        if arguments.inDir == None:
            arguments.inDir = raw_input("Enter input folder: ")
            checkDirectory(arguments.inDir)
        if arguments.outDir == None:
            arguments.outDir = raw_input("Enter destination folder for .mpk: ")
            checkDirectory(arguments.outDir)
        if arguments.logDir == None:
            arguments.logDir = raw_input("Enter folder for logfiles: ")
            checkDirectory(arguments.logDir)

    mpkExport(arguments)

main()