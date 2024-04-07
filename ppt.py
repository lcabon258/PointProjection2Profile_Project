# -*- coding: utf-8 -*-
# SRLabSCART.proc.ppt Profile Projection Toolset 
# 開發 developer： 孫正瑋 ChengWei Sun 

# builtin
from pathlib import Path
from datetime import datetime
# 3rd-party
import numpy as np
import pandas as pd

def ortho(mp_table:pd.DataFrame,dp_table:pd.DataFrame)->pd.DataFrame:
    """
    將 dp_table 所有資料點的 X、Y 座標正投影至 mp_table 中的點連線。
    -----
    輸入:
        mp_table:pd.DataFrame 剖面的表格，包含以下資料:
            LineOID : 線圖徽的標記。
            MasterX : 剖面節點 X 座標。
            MasterY : 剖面節點 Y 座標。
            Mileage : 節點里程數（從第一點開始算）
            MileageRev. : 節點里程數（從第最後點開始算）

        dp_table:pd.DataFrame 資料點的表格，包含以下資料:
            PointOID : 線圖徽的標記。
            DataX : 點圖徽 X 座標。
            DataY : 點圖徽 Y 座標。 
    -----
    輸出:
        dp_table:pd.DataFrame 資料點的表格，包含以下資料:
            PointOID : 線圖徽的標記。
            DataX : 點圖徽 X 座標。
            DataY : 點圖徽 Y 座標。
            針對每一個獨立的 LineOID，令其編號為i，新增以下欄位：
                Line_i_Vertical_Distance : 資料點到剖面的垂直距離。
                Line_i_Horizontal_Distance : 資料點到剖面的水平距離。
                Line_i_ProjX : 投影點 X 座標。
                Line_i_ProjY : 投影點 Y 座標。

    """
    print(f'[{datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}]Calculating orthogonal projection.')
    # 因為兩表格要取值運算變成 numpy ndarray -> 
    # 浪費空間可是比較好寫
    m_xy_np = mp_table.to_numpy() # 主剖面的表格
    #print(m_xy_np)
    d_xy_np = dp_table.iloc[:,1:3].to_numpy() # 資料點表格，只取 XY
    #print(d_xy_np)

    # 迭代每一個獨特的 LineOID
    for line_oid in mp_table["LineOID"].unique():
        # Get the index of the line
        line_index = mp_table[mp_table["LineOID"]==line_oid].index
        # X, Y coordinate in the mp_table
        m_xy_np = mp_table.loc[line_index,"MasterX":"MasterY"].to_numpy()
        #print(m_xy_np)
        # X,Y coordinate in the dp_table
        d_xy_np = dp_table.loc[:,"DataX":"DataY"].to_numpy()
        #print(d_xy_np)
        # 針對當下的 LineOID 建立投影距離欄位
        Proj_Vertical_Distance = f"Line_{line_oid}_Vertical_Distance"
        Proj_Horizontal_Distance = f"Line_{line_oid}_Horizontal_Distance"
        ProjX = f"Line_{line_oid}_ProjX"
        ProjY = f"Line_{line_oid}_ProjY"

        # 在 df 表格新增投影距離欄位，還有新計算的 mileage
        dp_table[Proj_Vertical_Distance] = np.inf # 運算時暫存，會隨需要更新，最後再計算成 mileage
        dp_table[Proj_Horizontal_Distance] = 0. # 運算時暫存，會隨需要更新。
        dp_table[ProjX] = 0.
        dp_table[ProjY] = 0.
        ## 全部整理版本
        for i in range(m_xy_np.shape[0]-1):
            #主剖面第幾個點
            # 計算剖面方向的向量
            m_vec = m_xy_np[i+1,0:2] - m_xy_np[i,0:2] # 剖面第i個點往第i+1個點的向量
            # print(f"m_xy_np[i+1,0:2]={m_xy_np[i+1,0:2]}")
            # print(f"m_xy_np[i,0:2]={m_xy_np[i,0:2]}")
            # print(f"m_vec={m_vec}")
            
            # 計算剖面起始點到資料點向量
            md_vec = d_xy_np - m_xy_np[i,0:2]  # 剖面第i的點往資料點j的向量
            # print(f"md_vec={md_vec}")# 看起來是 element-wise，OK

            # 內積
            m_md_dot = np.dot(md_vec,m_vec)
            # print(f"m_md_dot={m_md_dot}")

            # 向量長度
            m_vec_norm = np.linalg.norm(m_vec)
            md_vec_norm = np.linalg.norm(md_vec,axis=1)
            m_md_theda = np.arccos(m_md_dot/m_vec_norm/md_vec_norm)
            # print(f"m_vec_norm={m_vec_norm}")
            # print(f"md_vec_norm={md_vec_norm}")
            # print(f"m_md_theda={m_md_theda}")

            # 計算水平與垂直距離
            md_proj_hori = md_vec_norm*np.cos(m_md_theda)
            md_proj_vert = md_vec_norm*np.sin(m_md_theda)
            # print(f"md_proj_hori={md_proj_hori}")
            # print(f"md_proj_vert={md_proj_vert}")

            # 投影後的點
            md_projected_X = m_xy_np[i,0] +  m_md_dot * m_vec[0] / (np.power(m_vec_norm,2))
            # print(f"md_projected_X={md_projected_X}")
            md_projected_Y = m_xy_np[i,1] + m_md_dot * m_vec[1] / (np.power(m_vec_norm,2))
            # print(f"md_projected_Y={md_projected_Y}")

            # 篩選
            ## 方向與在剖面兩點內。
            ## 備註：取值的時候要用：d_xy_np[in_range_indice][:,0]
            indices_horizontal_dist_in_range = np.where((md_proj_hori>=0) & (md_proj_hori<m_vec_norm))[0]
            # print(f"indices_horizontal_dist_in_range={indices_horizontal_dist_in_range}")

            ## 垂直距離已經小於原本的紀錄值
            vertical_filtered = dp_table.loc[indices_horizontal_dist_in_range,Proj_Vertical_Distance] > md_proj_vert[indices_horizontal_dist_in_range]
            vertical_filtered = vertical_filtered.values
            # print(f"vertical_filtered={vertical_filtered}")
            
            # 更新資料
            ## 垂直距離
            dp_table.loc[indices_horizontal_dist_in_range[vertical_filtered],Proj_Vertical_Distance]  = md_proj_vert[indices_horizontal_dist_in_range[vertical_filtered]]
            ## 水平距離
            dp_table.loc[indices_horizontal_dist_in_range[vertical_filtered],Proj_Horizontal_Distance]  = md_proj_hori[indices_horizontal_dist_in_range[vertical_filtered]] + mp_table["Mileage"][i]
            ## 投影座標 X
            dp_table.loc[indices_horizontal_dist_in_range[vertical_filtered],ProjX] = md_projected_X[indices_horizontal_dist_in_range[vertical_filtered]]
            ## 投影座標 Y
            dp_table.loc[indices_horizontal_dist_in_range[vertical_filtered],ProjY] = md_projected_Y[indices_horizontal_dist_in_range[vertical_filtered]]
    return dp_table