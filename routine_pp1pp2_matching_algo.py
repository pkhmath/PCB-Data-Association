#******************************************************************************************************************************************
# TITLE     : ROUTINE_PP1PP2_MATCHING
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

#PP1-PP2 PCB Data Association

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
Forward PP1 PP2 Matching Process
"""

print('Start of defining procedure : fwd_pp1pp2_matching_algo :', datetime.datetime.now())
print('Version used : 2019-06-19 14:37')

def fwd_pp1pp2_matching_algo(pcb_level_dfone,pcb_level_dftwo):
    """
    Purpose : Perform PP1-PP2 forward matching
    Inputs  : pcb_level_dfone - The PCB level dataframe corresponding to first machine (PP1)
              pcb_level_dfone - The PCB level dataframe corresponding to second machine (PP2)
    Output  : matched_df      - The dataframe that contains the matched PCBs       
    """
    
    STR_TIME = datetime.datetime.now()
    
    print('=======================================================')
    print("START : ", STR_TIME)
    print('=======================================================')

    PP1PP2_MATCH_THRESHOLD = 0.7
    
    #Initialization
    no_of_matched_pcbs = 0
    
    #Initialize weight matrix
    weight_mtrx = np.zeros([len(pcb_level_dfone),len(pcb_level_dftwo)])

    #Assign weights
    for i in range(0,len(pcb_level_dfone)):
        for j in range(0,len(pcb_level_dftwo)):
            arvl_one = pcb_level_dfone.arvl_tmstmp[i]
            arvl_two = pcb_level_dftwo.arvl_tmstmp[j]
            parm1 = 1 / (pd.Timedelta(pd.Timestamp(arvl_two) - pd.Timestamp(arvl_one)).total_seconds())
        
            dptr_one = pcb_level_dfone.dptr_tmstmp[i]
            dptr_two = pcb_level_dftwo.dptr_tmstmp[j]
            parm2 = 1 / (pd.Timedelta(pd.Timestamp(dptr_two) - pd.Timestamp(dptr_one)).total_seconds())
        
            parm3 = 1 / (pd.Timedelta(pd.Timestamp(arvl_two) - pd.Timestamp(dptr_one)).total_seconds())
        
            if parm1 < 0 :
                parm1 = 0.0
            if parm2 < 0 :
                parm2 = 0.0
            if parm3 < 0 :
                parm3 = 0.0
            
            sum_parms = parm1 + parm2 + parm3
            prd_parms = parm1 * parm2 * parm3
        
            weight_mtrx[i,j] = pcb_level_dfone.weightage[i] * prd_parms * pcb_level_dftwo.weightage[j]
        #endfor
    #endfor    
    
    print('Weight matrix generation completed at:', datetime.datetime.now())
    
    #Now perform the matchng
    matched_df = pd.DataFrame(columns=['pp1_indx','pp1_arvl','pp1_dptr','pp2_indx','pp2_arvl','pp2_dptr','edge_weight_pp1pp2'])
    for i in range (0,len(pcb_level_dfone)):
        if (pcb_level_dfone.weightage[i] >= PP1PP2_MATCH_THRESHOLD):
            j = np.argmax(weight_mtrx[i,:])
            if (pcb_level_dftwo.weightage[j] >= PP1PP2_MATCH_THRESHOLD):
                if (weight_mtrx[i,j] > 0):
                    edge_weight_pp1pp2 = np.asscalar(weight_mtrx[i,j])
                    data = pd.DataFrame([[i,pcb_level_dfone.arvl_tmstmp[i],pcb_level_dfone.dptr_tmstmp[i],j,pcb_level_dftwo.arvl_tmstmp[j],pcb_level_dftwo.dptr_tmstmp[j],edge_weight_pp1pp2]],columns=matched_df.columns)                    
                    matched_df = matched_df.append(data)
                    del data
                    no_of_matched_pcbs = no_of_matched_pcbs + 1
                #endif
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
print('End   of defining procedure : fwd_pp1pp2_matching_algo :', datetime.datetime.now())



#=============================================================================================================

"""
Reverse PP1 PP2 Matching Process
"""

print('Start of defining procedure : rev_pp1pp2_matching_algo :', datetime.datetime.now())
print('Version used : 2019-06-19 14:37')

def rev_pp1pp2_matching_algo(pcb_level_dfone,pcb_level_dftwo):
    """
    Purpose : Perform PP1-PP2 reverse matching
    Inputs  : pcb_level_dfone - The PCB level dataframe corresponding to first machine (PP1)
              pcb_level_dfone - The PCB level dataframe corresponding to second machine (PP2)
    Output  : matched_df      - The dataframe that contains the matched PCBs       
    """
    
    STR_TIME = datetime.datetime.now()
    
    print('=======================================================')
    print("START : ", STR_TIME)
    print('=======================================================')

    PP1PP2_MATCH_THRESHOLD
    
    #Initialization
    no_of_matched_pcbs = 0
    
    #Initialize weight matrix
    weight_mtrx = np.zeros([len(pcb_level_dfone),len(pcb_level_dftwo)])

    #Assign weights
    for i in range(0,len(pcb_level_dfone)):
        for j in range(0,len(pcb_level_dftwo)):
            arvl_one = pcb_level_dfone.arvl_tmstmp[i]
            arvl_two = pcb_level_dftwo.arvl_tmstmp[j]
            parm1 = 1 / (pd.Timedelta(pd.Timestamp(arvl_two) - pd.Timestamp(arvl_one)).total_seconds())
        
            dptr_one = pcb_level_dfone.dptr_tmstmp[i]
            dptr_two = pcb_level_dftwo.dptr_tmstmp[j]
            parm2 = 1 / (pd.Timedelta(pd.Timestamp(dptr_two) - pd.Timestamp(dptr_one)).total_seconds())
        
            parm3 = 1 / (pd.Timedelta(pd.Timestamp(arvl_two) - pd.Timestamp(dptr_one)).total_seconds())
        
            if parm1 < 0 :
                parm1 = 0.0
            if parm2 < 0 :
                parm2 = 0.0
            if parm3 < 0 :
                parm3 = 0.0
            
            sum_parms = parm1 + parm2 + parm3
            prd_parms = parm1 * parm2 * parm3
        
            weight_mtrx[i,j] = pcb_level_dfone.weightage[i] * prd_parms * pcb_level_dftwo.weightage[j]
        #endfor
    #endfor    
    
    print('Weight matrix generation completed at:', datetime.datetime.now())
    
    #Now perform the matchng
    matched_df = pd.DataFrame(columns=['pp1_indx','pp1_arvl','pp1_dptr','pp2_indx','pp2_arvl','pp2_dptr','edge_weight_pp1pp2'])
    for j in range (0,len(pcb_level_dftwo)):
        if (pcb_level_dftwo.weightage[j] >= PP1PP2_MATCH_THRESHOLD):
            i = np.argmax(weight_mtrx[:,j])
            if (pcb_level_dfone.weightage[i] >= PP1PP2_MATCH_THRESHOLD):
                if (weight_mtrx[i,j] > 0):
                    edge_weight_pp1pp2 = np.asscalar(weight_mtrx[i,j])
                    data = pd.DataFrame([[i,pcb_level_dfone.arvl_tmstmp[i],pcb_level_dfone.dptr_tmstmp[i],j,pcb_level_dftwo.arvl_tmstmp[j],pcb_level_dftwo.dptr_tmstmp[j],edge_weight_pp1pp2]],columns=matched_df.columns)                    
                    matched_df = matched_df.append(data)
                    del data
                    no_of_matched_pcbs = no_of_matched_pcbs + 1
                #endif
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
print('End   of defining procedure : rev_pp1pp2_matching_algo :', datetime.datetime.now())