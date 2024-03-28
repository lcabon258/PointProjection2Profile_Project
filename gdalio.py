# -*- encoding:utf-8 -*-
# 讀取 FC 並且將座標輸出為 numpy array

from pathlib import Path
import sys

import numpy as np
from osgeo import ogr 

NoneType = type(None)

def gdb_pointfc2arr(inputFC:Path)->np.ndarray:
    """Reads the FC layer from the gdb and return the coordinates to xy(z) array
    input:
        InputFC: the path to a gdb in layer
    output:
        arr:np.ndarray: a Nx3 array represents the x, y, z coordinate.
    """
    # 步驟：
    # 開啟 GDB 圖層
    # 結點數量計算，準備 np.ndarray 把結果填進去
    # 讀取圖層內的節點的座標填進去

    ### 使用「FileGDB」或是「OpenFileGDB」去讀取 FileGDB 資料庫。###
    driver = ogr.GetDriverByName("FileGDB")
    if isinstance(driver,NoneType):
        print("The driver 'FileGDB' is NOT available in this system!")
        # Try to load FileGDB using "OpenFileGDB" driver.
        driver = ogr.GetDriverByName("OpenFileGDB")
        if isinstance(driver,NoneType):
            print("The driver 'OpenFileGDB' is NOT available in this system!")
            print("Please confirm the driver installation needed for accessing FileGDB")
        else:
            print("Using 'OpenFileGDB' as driver")
        
    # 開啟GDB檔案
    print("Opening the FileGDB")
    try:
        gdb = driver.Open(str(inputFC.parent),0) # 0 means read-only
    except Exception as e:
        print(e)
    # 測試是否成功開啟：
    if isinstance(gdb,NoneType):
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
    out_arr = np.zeros((featureCount,2))
    # 迭代資料與表格
    for i,feature in enumerate(FC_layer):
        geom = feature.GetGeometryRef()
        out_arr[i,0] = geom.GetX()
        out_arr[i,1] = geom.GetY()        
    
    return out_arr

def gdb_linefc2arr(inputFC:Path)->np.ndarray:
    """Reads the FC layer from the gdb and return the coordinates to xy(z) array
    input:
        InputFC: the path to a gdb in layer
    output:
        arr:np.ndarray: a Nx3 array represents the x, y, z coordinate.
            fields: feature ID
    """
    # 步驟：
    # 開啟 GDB 圖層
    # 結點數量計算，準備 np.ndarray 把結果填進去
    # 讀取圖層內的節點的座標填進去

    ### 使用「FileGDB」或是「OpenFileGDB」去讀取 FileGDB 資料庫。###
    driver = ogr.GetDriverByName("FileGDB")
    if isinstance(driver,NoneType):
        print("The driver 'FileGDB' is NOT available in this system!")
        # Try to load FileGDB using "OpenFileGDB" driver.
        driver = ogr.GetDriverByName("OpenFileGDB")
        if isinstance(driver,NoneType):
            print("The driver 'OpenFileGDB' is NOT available in this system!")
            print("Please confirm the driver installation needed for accessing FileGDB")
        else:
            print("Using 'OpenFileGDB' as driver")
        
    # 開啟GDB檔案
    print("Opening the FileGDB")
    try:
        gdb = driver.Open(str(inputFC.parent),0) # 0 means read-only
    except Exception as e:
        print(e)
    # 測試是否成功開啟：
    if isinstance(gdb,NoneType):
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
    out_arr = np.zeros((featureCount,3))
    # 迭代資料與表格
    for i,feature in enumerate(FC_layer):
        out_arr[i,0] = i
        geom = feature.GetGeometryRef() # MultilineString = list of line
        for line_geom in geom:
            for vertices in line_geom.GetPoints():
                out_arr[i,1] = vertices[0]
                out_arr[i,2] = vertices[1]        
    
    return out_arr

