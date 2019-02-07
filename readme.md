# Geocom Map Package Export Tool                               

The script exports map packages from all .mxd in a given directory. Since it can be called parametrized it is well suited for updating map packages periodicaly using the windows task scheduler.

For more information please contact: support@geocom.ch. 

#### DISCLAMER: Please be aware this product is not supported. Further information can be found in the license file.


------
## Requirements

In order to use the tool you need: 
- An installation of Python 2.7 
- An installation of arcpy (preinstalled, if you have an ArcMap installed)


------
## Installation 

1. Create a folder for the script.
2. Download and save the tool into the folder.
3. Prepare folder structure, example can be found below.


------
## Usage 

### How to use it

1. Open a console Window and navigate to the script.
2. Type *'mpk_export.py'* followed by the required parameters.  
   (Run with the *-h* parameter to get a full list)
3. Hit 'Enter' and wait for the results.


#### Examples

**Folder structure**
Scripts folder: C:\python_scripts
Input folder:   C:\mxds_to_export
output folder:  C:\latest_mpks
log folder:     C:\export_logs

**Minimal input**
C:\python_scripts> mpk_export.py

**Normal usage**
C:\python_scripts> mpk_export.py -i C:\mxds_to_export -o C:\latest_mpks -l C:\export_logs

**Silent usage**
C:\python_scripts> mpk_export.py -s -i C:\mxds_to_export -o C:\latest_mpks -l C:\export_logs

**Fully parametrized**
C:\python_scripts> mpk_export.py -i C:\mxds_to_export -o C:\latest_mpks -l C:\export_logs -ln mpk_test_export.log

> A complete list of all valid parameters can be found in the **Help** section of this page.


------
## Help

The tool help can be called by running the script in the console with the -h parameter


#### Acceptetd parameters

Parameter | Description
--------- | -----------
 -h,   --help | Opens the help in the console
 -s,   --silent | Use to prevent user interaction. If no paths are given (see -i, -o, -l), the path of this script will be used for either path.
 -i,   --inDir | The directory where the mxds are stored. Asks for user interaction if not set. 
 -o,   --outDir | The directory where the mpks will be exported to. Asks for user interaction if not set.
 -l,   --logDir | The directory where the logfile will be created. Asks for user interaction if not set.
 -ln,  --logName | The name of the logfile (default: [date]__mpk_export.log).


------
## Known issues

None.
