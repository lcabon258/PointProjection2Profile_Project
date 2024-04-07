# -*- encoding:utf-8 -*-
# 讀取 FC 並且將座標輸出為 numpy array

from pathlib import Path
import sys

import numpy as np
import pandas as pd
from osgeo import ogr 

def gdb_linefc2df(inputFC:Path)->pd.DataFrame:
    """Reads the FC layer from the gdb and return the coordinates to xy(z) array
    -----
    input:
        InputFC: the path to a gdb in layer
    -----
    output:
    mp_table:pd.DataFrame 剖面的表格，包含以下資料:
        LineOID : 線圖徽的標記。
        MasterX : 剖面節點 X 座標。
        MasterY : 剖面節點 Y 座標。
        Mileage : 節點里程數（從第一點開始算）
        MileageRev. : 節點里程數（從第最後點開始算）
    """
    ### 使用「FileGDB」或是「OpenFileGDB」去讀取 FileGDB 資料庫。###
    driver = ogr.GetDriverByName("OpenFileGDB")
    if driver is None:
        print("The driver 'OpenFileGDB' is NOT available in this system!")
        # Try to load FileGDB using "OpenFileGDB" driver.
        driver = ogr.GetDriverByName("FileGDB")
        if driver is None:
            print("The driver 'FileGDB' is NOT available in this system!")
            print("Please confirm the driver installation needed for accessing FileGDB")
            raise Exception("Driver not available")
        else:
            print("Using 'OpenFileGDB' as driver")
        
    # 開啟GDB檔案
    print("Opening the FileGDB")
    try:
        gdb = driver.Open(str(inputFC.parent),0) # 0 means read-only
    except Exception as e:
        print(e)
    # 測試是否成功開啟：
    if gdb is None:
        print("Fail to open the geodatabase.")
        sys.exit(1)
    else:
        print("Opened the geodatabase")
    ### 開啟特定圖層 ###
    FC_layer = gdb.GetLayerByName(str(inputFC.stem))
    # 確認FC數量以建立儲存空間
    featureCount = FC_layer.GetFeatureCount()
    print("Feature Count:",featureCount)
    # Count the number of vertices
    vertexCount = 0
    for feature in FC_layer:
        geom = feature.GetGeometryRef()
        for line_geom in geom:
            vertexCount += line_geom.GetPointCount()
    # 資料輸出表格
    mp_table = pd.DataFrame(np.zeros(shape=(vertexCount,5)),columns=["LineOID","MasterX","MasterY","Mileage","MileageRev."])
    # 迭代資料與表格
    datacursor = 0
    for i,feature in enumerate(FC_layer):
        geom = feature.GetGeometryRef() # MultilineString = list of line
        for line_geom in geom:
            for vertices in line_geom.GetPoints():
                mp_table.loc[datacursor,"LineOID"] = i
                mp_table.loc[datacursor,"MasterX"] = vertices[0]
                mp_table.loc[datacursor,"MasterY"] = vertices[1]
                datacursor += 1
    # 計算里程
    # iterate through the unique LineOID
    for line_oid in mp_table["LineOID"].unique():
        # Get the index of the line
        line_index = mp_table[mp_table["LineOID"]==line_oid].index
        # Calculate the mileage
        mp_table.loc[line_index[1:],"Mileage"] = np.sqrt(np.diff(mp_table.loc[line_index,"MasterX"])**2 + np.diff(mp_table.loc[line_index,"MasterY"])**2).cumsum()
        mp_table.loc[line_index[:-1],"MileageRev."] = mp_table.loc[line_index,"Mileage"].max() - mp_table.loc[line_index,"Mileage"]
    
    return mp_table

def gdb_pointfc2fc(inputFC:Path)->pd.DataFrame:
    """Reads the FC layer from the gdb and return the coordinates to xy(z) array
    -----
    input:
        InputFC: the path to a gdb in layer
    -----
    output:
    dp_table:pd.DataFrame 剖面的表格，包含以下資料:
        PointOID : 線圖徽的標記。
        DataX : 點圖徽 X 座標。
        DataY : 點圖徽 Y 座標。

    """
    ### 使用「FileGDB」或是「OpenFileGDB」去讀取 FileGDB 資料庫。###
    driver = ogr.GetDriverByName("OpenFileGDB")
    if driver is None:
        print("The driver 'OpenFileGDB' is NOT available in this system!")
        # Try to load FileGDB using "OpenFileGDB" driver.
        driver = ogr.GetDriverByName("FileGDB")
        if driver is None:
            print("The driver 'FileGDB' is NOT available in this system!")
            print("Please confirm the driver installation needed for accessing FileGDB")
            raise Exception("Driver not available")
        else:
            print("Using 'OpenFileGDB' as driver")
        
    # 開啟GDB檔案
    print("Opening the FileGDB")
    try:
        gdb = driver.Open(str(inputFC.parent),0) # 0 means read-only
    except Exception as e:
        print(e)
    # 測試是否成功開啟：
    if gdb is None:
        print("Fail to open the geodatabase.")
        sys.exit(1)
    else:
        print("Opened the geodatabase")
    ### 開啟特定圖層 ###
    FC_layer = gdb.GetLayerByName(str(inputFC.stem))
    # 確認FC數量以建立儲存空間
    featureCount = FC_layer.GetFeatureCount()
    print("Feature Count:",featureCount)
    # 資料輸出表格
    dp_table = pd.DataFrame(np.zeros(shape=(featureCount,3)),columns=["PointOID","DataX","DataY"])
    # 迭代資料與表格
    for i,feature in enumerate(FC_layer):
        geom = feature.GetGeometryRef()
        dp_table.loc[i,"PointOID"] = i
        dp_table.loc[i,"DataX"] = geom.GetX()
        dp_table.loc[i,"DataY"] = geom.GetY()
    
    return dp_table