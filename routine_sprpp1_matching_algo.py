#******************************************************************************************************************************************
# TITLE     : ROUTINE_SPRPP1_MATCHING
# AUTHOR    : PRAKASH HIREMATH M
# DATE      : AUG 2018 - JUN 2019
# INSTITUTE : INDIAN INSTITUTE OF SCIENCE
#******************************************************************************************************************************************


#******************************************************************************************************************************************
# VERSION HISTORY
#******************************************************************************************************************************************
# DATE (YYYY-MM-DD) | AUTHOR              | COMMENTS
#------------------------------------------------------------------------------------------------------------------------------------------
# 2019-10-11        | PRAKASH HIREMATH M  | Initial version
#******************************************************************************************************************************************

#SPR-PP1 PCB Data Association 

import pandas as pd
import numpy as np
import scipy as sp

import csv
import datetime

from matplotlib import pyplot as plt
from matplotlib import dates  as md 
from matplotlib.colors import LogNorm

#==============================================================================================
"""
Forward SPR - PP1 Matching Process
"""

print('Start of defining procesure : fwd_sprpp1_matching_algo :', datetime.datetime.now())
def fwd_sprpp1_matching_algo(pcb_level_dfspr,pcb_level_dfpp1):
    """
    Purpose : Perform forward matching of SPR and PP1
    Inputs  : pcb_level_dfspr - The PCB level dataframe corresponding to screen printer
              pcb_level_dfpp1 - The PCB level dataframe corresponding to PP1
    Output  : matched_df      - The dataframe that contains the matched PCBs       
    """
    
    STR_TIME = datetime.datetime.now()
    
    print('=======================================================')
    print("START : ", STR_TIME)
    print('=======================================================')

    #Initialization
    no_of_matched_pcbs = 0
    
    #Initialize weight matrix
    weight_mtrx = np.zeros([len(pcb_level_dfspr),len(pcb_level_dfpp1)])

    #Assign weights
    for i in range(0,len(pcb_level_dfspr)):
        for j in range(0,len(pcb_level_dfpp1)):
            dptr_spr = pcb_level_dfspr.dptr_tmstmp[i]
            arvl_pp1 = pcb_level_dfpp1.arvl_tmstmp[j]
            dptr_pp1 = pcb_level_dfpp1.dptr_tmstmp[j]
            parm1 = 1 / (pd.Timedelta(pd.Timestamp(arvl_pp1) - pd.Timestamp(dptr_spr)).total_seconds())
                
            if parm1 < 0 :
                parm1 = 0.0
            #endif    

            prd_parms = parm1
        
            weight_mtrx[i,j] = prd_parms * pcb_level_dfpp1.weightage[j]
        #endfor
    #endfor    
    
    print('Weight matrix generation completed at:', datetime.datetime.now())
    
    #Now perform the matchng
    matched_df = pd.DataFrame(columns=['spr_indx','spr_dptr','pp1_indx','pp1_arvl','pp1_dptr','edge_weight_sprpp1'])
    for i in range (0,len(pcb_level_dfspr)):
        j = np.argmax(weight_mtrx[i,:])
        if (pcb_level_dfpp1.weightage[j] >= 0.8):
            if (weight_mtrx[i,j] > 0):
                edge_weight_sprpp1 = np.asscalar(weight_mtrx[i,j])
                data = pd.DataFrame([[i,pcb_level_dfspr.dptr_tmstmp[i],j,pcb_level_dfpp1.arvl_tmstmp[j],pcb_level_dfpp1.dptr_tmstmp[j],edge_weight_sprpp1]],columns=matched_df.columns)                    
                matched_df = matched_df.append(data)
                del data
                no_of_matched_pcbs = no_of_matched_pcbs + 1
            #endif
        #endif 
    #endfor  
    
    matched_df = matched_df.reset_index()
    matched_df = matched_df.iloc[:,1:len(matched_df.columns)]

    END_TIME = datetime.datetime.now()
    
    print('No. of matched PCBs =', no_of_matched_pcbs)
    
    print('=======================================================')
    print("END   : ", END_TIME)
    print('=======================================================')
    
    DUR_TS    = pd.Timestamp(END_TIME) - pd.Timestamp(STR_TIME)
    EXEC_TIME = pd.Timedelta(DUR_TS).total_seconds()
    
    print("Execution time =",EXEC_TIME/60,"mins")
    print('=======================================================')

    return matched_df
#end-proc
print('End   of defining procedure : fwd_sprpp1_matching_algo :', datetime.datetime.now())



#==============================================================================================================
"""
Reverse SPR PP1 Matching
"""

print('Start of defining procedure : rev_sprpp1_matching_algo :', datetime.datetime.now())
print('Version used : 2019-05-08 13:02')

def rev_sprpp1_matching_algo(pcb_level_dfspr,pcb_level_dfpp1):
    """
    Purpose : Perform matching from PP1 to SPR
    Inputs  : pcb_level_dfspr - The PCB level dataframe corresponding to screen printer
              pcb_level_dfpp1 - The PCB level dataframe corresponding to PP1
    Output  : matched_df      - The dataframe that contains the matched PCBs       
    """
    
    STR_TIME = datetime.datetime.now()
    
    print('=======================================================')
    print("START : ", STR_TIME)
    print('=======================================================')

    #Initialization
    no_of_matched_pcbs = 0
    
    #Initialize weight matrix
    weight_mtrx = np.zeros([len(pcb_level_dfspr),len(pcb_level_dfpp1)])
    
    #Assign weights
    for i in range(0,len(pcb_level_dfspr)):
        for j in range(0,len(pcb_level_dfpp1)):
            dptr_spr = pcb_level_dfspr.dptr_tmstmp[i]
            arvl_pp1 = pcb_level_dfpp1.arvl_tmstmp[j]
            dptr_pp1 = pcb_level_dfpp1.dptr_tmstmp[j]
            parm1 = 1 / (pd.Timedelta(pd.Timestamp(arvl_pp1) - pd.Timestamp(dptr_spr)).total_seconds())
                
            if parm1 < 0 :
                parm1 = 0.0
            #endif    

            prd_parms = parm1
        
            weight_mtrx[i,j] = prd_parms * pcb_level_dfpp1.weightage[j]
        #endfor
    #endfor    
    
    print('Weight matrix generation completed at:', datetime.datetime.now())
    
    #Now perform the matching
    matched_df = pd.DataFrame(columns=['spr_indx','spr_dptr','pp1_indx','pp1_arvl','pp1_dptr','edge_weight_sprpp1'])
    for j in range (0,len(pcb_level_dfpp1)):
        i = np.argmax(weight_mtrx[:,j])
        if (pcb_level_dfpp1.weightage[j] >= 0.8):
            if (weight_mtrx[i,j] > 0):
                edge_weight_sprpp1 = np.asscalar(weight_mtrx[i,j])
                data = pd.DataFrame([[i,pcb_level_dfspr.dptr_tmstmp[i],j,pcb_level_dfpp1.arvl_tmstmp[j],pcb_level_dfpp1.dptr_tmstmp[j],edge_weight_sprpp1]],columns=matched_df.columns)                    
                matched_df = matched_df.append(data)
                del data
                no_of_matched_pcbs = no_of_matched_pcbs + 1
            #endif
        #endif 
    #endfor  
    
    matched_df = matched_df.reset_index()
    matched_df = matched_df.iloc[:,1:len(matched_df.columns)]

    END_TIME = datetime.datetime.now()
    
    print('No. of matched PCBs =', no_of_matched_pcbs)
    
    print('=======================================================')
    print("END   : ", END_TIME)
    print('=======================================================')
    
    DUR_TS    = pd.Timestamp(END_TIME) - pd.Timestamp(STR_TIME)
    EXEC_TIME = pd.Timedelta(DUR_TS).total_seconds()
    
    print("Execution time =",EXEC_TIME/60,"mins")
    print('=======================================================')

    return matched_df
#end-proc
print('End   of defining procedure : rev_sprpp1_matching_algo :', datetime.datetime.now())

