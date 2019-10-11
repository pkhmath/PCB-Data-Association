#******************************************************************************************************************************************
# TITLE     : ROUTINE_LDRSPR_MATCHING
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

#LDR-SPR PCB Data Association 

import csv
import datetime

import numpy  as np
import pandas as pd

import importlib

import routine_get_histogram
importlib.reload(routine_get_histogram)

#pcb_level_dfldr : arvl_tmstmp, dptr_tmstmp
#pcb_level_dfspr : dptr_tmstmp

#Procedure to perform data association (matching) between loader and screen-printer
print('Start of defining procedure : rev_ldrspr_matching_algo :', datetime.datetime.now())
print('Version : 2019-04-27 21:05')

def rev_ldrspr_matching_algo (pcb_level_dfldr,pcb_level_dfspr):

    STR_TIME = datetime.datetime.now()
    
    print('=======================================================')
    print("START : ", STR_TIME)
    print('=======================================================')
    
    no_of_matched_pcbs = 0
    matched_df = pd.DataFrame(columns=['ldr_dptr','spr_indx','spr_dptr','spr_special_entry','ldr_multiple_events'])

    print('Creating initial matched dataframe...')
    
    for i in range(0,len(pcb_level_dfspr)):
        spr_curr_tmstmp = pcb_level_dfspr.dptr_tmstmp[i]
        if (i == 0):
            ldr_events_df = pcb_level_dfldr.query('dptr_tmstmp < @spr_curr_tmstmp')
        else:
            spr_prev_tmstmp = pcb_level_dfspr.dptr_tmstmp[i-1]
            ldr_events_df = pcb_level_dfldr.query('(dptr_tmstmp > @spr_prev_tmstmp) & (dptr_tmstmp < @spr_curr_tmstmp)')
        #end-if
        ldr_events_df = ldr_events_df.reset_index()
        ldr_events_df = ldr_events_df.iloc[:,1:len(ldr_events_df.columns)]
    
        if (len(ldr_events_df) == 0):
            print('No loader event identified at i =', i, ':spr_timestamp =', spr_curr_tmstmp)
            ldr_dptr = np.nan
            spr_indx = i
            spr_dptr = spr_curr_tmstmp
            spr_special_entry   = 1   
            ldr_multiple_events = 0
            data = pd.DataFrame([[ldr_dptr,spr_indx,spr_dptr,spr_special_entry,ldr_multiple_events]],columns=matched_df.columns)
            matched_df = matched_df.append(data)
            del data
        elif (len(ldr_events_df) == 1):
            ldr_dptr = ldr_events_df.dptr_tmstmp[0]
            spr_indx = i
            spr_dptr = spr_curr_tmstmp
            spr_special_entry   = 0
            ldr_multiple_events = 0
            data = pd.DataFrame([[ldr_dptr,spr_indx,spr_dptr,spr_special_entry,ldr_multiple_events]],columns=matched_df.columns)
            matched_df = matched_df.append(data)
            del data
        else:
            print('Multiple loader events identified at i =', i, ':spr_timestamp =', spr_curr_tmstmp)
            for j in range(0,len(ldr_events_df)):
                ldr_dptr = ldr_events_df.dptr_tmstmp[j]
                spr_indx = i
                spr_dptr = spr_curr_tmstmp
                spr_special_entry   = 0
                ldr_multiple_events = 1
                data = pd.DataFrame([[ldr_dptr,spr_indx,spr_dptr,spr_special_entry,ldr_multiple_events]],columns=matched_df.columns)
                matched_df = matched_df.append(data)
                del data
            #end-for
        #end-if
    #end-for    

    matched_df = matched_df.reset_index()
    matched_df = matched_df.iloc[:,1:len(matched_df.columns)]
    
    #Obtain the 1-1 LDR-SPR matched events
    temp_df = matched_df.query('(ldr_multiple_events == 0) & (spr_special_entry == 0)')
    temp_df = temp_df.reset_index()
    temp_df = temp_df.iloc[:,1:len(temp_df.columns)]
    
    print('Finding maximum likely time delay between LDR event and SPR exit...')
    
    #Obtain the maximum likely delay between loader event and screen-printer exit
    time_diff = []
    for i in range (0,len(temp_df)):
        td = pd.Timedelta(pd.Timestamp(temp_df.spr_dptr[i]) - pd.Timestamp(temp_df.ldr_dptr[i])).total_seconds()
        time_diff = np.append(time_diff,td)
    #end-for  

    hist_df,hist_mode = routine_get_histogram.get_mode(pd.Series(time_diff),0.0,0.5)
    
    print('hist_mode =', hist_mode)
    
    #Obtain the many-to-1 LDR-SPR matched events
    mult_ldr_df = matched_df.query('ldr_multiple_events == 1')
    mult_ldr_df = mult_ldr_df.reset_index()
    mult_ldr_df = mult_ldr_df.iloc[:,1:len(mult_ldr_df.columns)]
    
    print('Correction for multiple loader events...')
    
    #Correction for multiple loading events
    cor_mult_ldr_df = pd.DataFrame(columns=matched_df.columns)

    uniq_spr_indx = mult_ldr_df.spr_indx.unique()
    uniq_spr_dptr = mult_ldr_df.spr_dptr.unique()

    for i in range (0,len(uniq_spr_indx)):
        curr_spr_indx = uniq_spr_indx[i]
        ldr_dptr_srs = mult_ldr_df.query('spr_indx == @curr_spr_indx').loc[:,['ldr_dptr']]
        ldr_dptr_srs = ldr_dptr_srs.reset_index()
        ldr_dptr_srs = ldr_dptr_srs.iloc[:,1:len(ldr_dptr_srs.columns)]
    
        dev_arr = []
        for j in range (0,len(ldr_dptr_srs)):
            td = pd.Timedelta(pd.Timestamp(uniq_spr_dptr[i]) - pd.Timestamp(ldr_dptr_srs.ldr_dptr[j])).total_seconds()
            dev_arr = np.append(dev_arr,np.abs(td-hist_mode))
        #end-for
        min_dev = np.argmin(dev_arr)
    
        ldr_dptr            = ldr_dptr_srs.ldr_dptr[min_dev]
        spr_indx            = uniq_spr_indx[i]
        spr_dptr            = uniq_spr_dptr[i]
        spr_special_entry   = 0
        ldr_multiple_events = 1
        data = pd.DataFrame([[ldr_dptr,spr_indx,spr_dptr,spr_special_entry,ldr_multiple_events]],columns=matched_df.columns)
        cor_mult_ldr_df = cor_mult_ldr_df.append(data)
        del data
    #end-for

    cor_mult_ldr_df = cor_mult_ldr_df.reset_index()
    cor_mult_ldr_df = cor_mult_ldr_df.iloc[:,1:len(cor_mult_ldr_df.columns)]
    
    print('Creating final matched dataframe...')
    
    #Combine all to form only 1-1 LDR-SPR matched dataframe
    ldr_spr_matched_df = pd.DataFrame(columns=matched_df.columns)

    non_mult_ldr_df = matched_df.query('ldr_multiple_events == 0')

    ldr_spr_matched_df = ldr_spr_matched_df.append(non_mult_ldr_df)
    ldr_spr_matched_df = ldr_spr_matched_df.append(cor_mult_ldr_df)
    ldr_spr_matched_df = ldr_spr_matched_df.sort_values(by='spr_dptr')
    ldr_spr_matched_df = ldr_spr_matched_df.reset_index()
    ldr_spr_matched_df = ldr_spr_matched_df.iloc[:,1:len(ldr_spr_matched_df.columns)]
    
    no_of_matched_pcbs = len(ldr_spr_matched_df)
    print('No. of matched PCBs =', no_of_matched_pcbs)
    
    END_TIME = datetime.datetime.now()
    
    print('=======================================================')
    print("END   : ", END_TIME)
    print('=======================================================')
    
    DUR_TS    = pd.Timestamp(END_TIME) - pd.Timestamp(STR_TIME)
    EXEC_TIME = pd.Timedelta(DUR_TS).total_seconds()
    
    return ldr_spr_matched_df
    
#end-proc
print('End   of defining procedure : rev_ldrspr_matching_algo :', datetime.datetime.now())



