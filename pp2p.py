# -*- encoding:utf-8 -*-
# pp2p.py: Project points to profile
# Author: CWSun Apr.,2024

from pathlib import Path
from argparse import ArgumentParser,Namespace
import logging
# This module
import gdalio as gio
import ppt

# define the argument parser
def ParseArg()->Namespace:
    parser = ArgumentParser(description="Project points to profile. Currently only support feature class inside the gdb.")
    parser.add_argument("profile", type=Path, help="The path of profile line feature class. eg. /Path/To/Data.gdb/ProfileLine")
    parser.add_argument("points", type=Path, help="The path of points feature class. eg. /Path/To/Data.gdb/DataPoints")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    logging.info("Parsing commandline arguments.")
    args = ParseArg()
    logging.debug(f"command line arguments:\n{args}")
    # Read points
    logging.info("Reading points.")
    gdbPointFc:Path = args.points
    dataarr = gio.gdb_pointfc2fc(gdbPointFc)
    # Reading profile
    logging.info("Reading profile.")
    gdbLineFc:Path = args.profile
    profile_arr = gio.gdb_linefc2df(gdbLineFc)
    # Project points to profile
    logging.info("Projecting points to profile.")
    ortho_result = ppt.ortho(profile_arr,dataarr)
    # Save the result
    outputPath = profile_arr.parents[1]/"pp2p_{gdbPointFc.stem}_{gdbLineFc.stem}.csv" # The directory with the gdb
    logging.info(f"Saving the result to {outputPath}")
    ortho_result.to_csv(outputPath,index=False)
    logging.info(f"Done.")