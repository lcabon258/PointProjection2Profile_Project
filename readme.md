# Point projection to profile  
  
## Author   
CWSun 2024 
Project page: [lcabon258/PointProjection2Profile_Project](https://github.com/lcabon258/PointProjection2Profile_Project)  
  
## Purpose  
When create a geologic profile, project the points (attitudes) to a given lines (profile).  
  
## Environments  
Python packages:  
* gdal   
* numpy  
* pandas  
    
Create the conda environment using the command: `conda create -n gdal -c conda-forge python notebook gdal pandas numpy`  
  
## How to use  
1. Install the required python environment using the command above.  
2. Activate the python environment (e.g. `conda activate gdal`)  
3. Execute the `pp2p.py`.
    
usage: pp2p.py [-h] profile points
positional arguments:
* profile:Path The path of profile line feature class. eg. /Path/To/Data.gdb/ProfileLine  
* points:Path The path of points feature class. eg. /Path/To/Data.gdb/DataPoints  
**Currently, only the feature class in gdb is supported.**  
  
4. Output will be a table in csv format. The columns of the table includes:
* PointOID:int The OID of the point. This field can be used to join the table to original point feature class.  
* DataX:float The X coordinate of the point feature.  
* DataY:float The Y coordinate of the point feature.  
For each line feature, the following field will be generated:
* Line_{i}_Vertical_Distance : Vertical distance from the point to profile i.
* **Line_{i}_Horizontal_Distance** : Mileage on the profile.
* Line_{i}_ProjX : X coordinate of the projected data point.
* Line_{i}_ProjY : Y coordinate of the projected data point.
  
## Further dev. direction
### IO
[ ] Save the result into the gdb.
[ ] Support shapefile format.
[ ] Wrap the pp2p.py into a arcgis toolbox (.pyt).
### Functions
[ ] Generate the verification plot.
[ ] Calculate the angle between the azimuth of strike and the azimuth of the profile line. This can be further used to calculate the apparent dip.