# -*- coding: utf-8 -*-
# Author: WTWei, CWSun
# 2024.04.12
# project points to profile lines

import sys
import arcpy
from pathlib import Path
try:
    import gdalio as gio
    import ppt
except ImportError:
    arcpy.AddError("cannot find required module")
    sys.exit(1)

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "pp2p_toolbox"
        self.alias = "pp2p_toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [pp2p]


class pp2p(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "pp2p"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(\
            displayName="Input profile (Feature Class)",\
            name="in_profile",\
            datatype="DEFeatureClass",\
            parameterType="Required",\
            direction="Input")
        param1 = arcpy.Parameter(\
            displayName="Input points (Feature Class)",\
            name="in_points",\
            datatype="DEFeatureClass",\
            parameterType="Required",\
            direction="Input")
        param2 = arcpy.Parameter(\
            displayName="Output table",\
            name="OutTable",\
            datatype="DETable",\
            parameterType="Derived",\
            direction="Output")
        params = [param0, param1, param2]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        in_profile:Path = Path(parameters[0].valueAsText)
        in_points:Path = Path(parameters[1].valueAsText)
        profile_arr = gio.gdb_linefc2df(in_profile) #read profile
        data_arr = gio.gdb_pointfc2fc(in_points) #read points
        ortho_result = ppt.ortho(profile_arr,data_arr) #投影
        # Save the result
        outputPath = in_profile.parents[1]/f"pp2p_{in_points.stem}_{in_profile.stem}.csv" # The directory with the gdb
        ortho_result.to_csv(outputPath,index=False)
        parameters[2].value = str(outputPath)
        #arcpy.AddMessage("Input:")
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
