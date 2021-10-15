import numpy as np
import time
from Phase2.FeatureExtractor import *
import pickle
import os
import pandas as pd
attack_label = ["Ack","Combo","Junk","Scan","Syn","Tcp","Udp","Udpplain"] #attack_label: Attack list 

message_file_path = "./homeview/static/message/phase2_output.ms";
####################################################################################################
# to preprocess for testing: to check if trainmodel exists in ml_dir
####################################################################################################
def _prep_():
    testcasecout = 0
    strMsg = ""
    message_file = open(message_file_path,"a")
    for idx in range(len(attack_label)):
        path_pickle = f'./ml_model/Pickle_RL_Model{idx+1}.pkl' ;
        if os.path.isfile(path_pickle):
            testcasecout = testcasecout+1
    if testcasecout == 0 :
        print("You should train the dataset...")
        strMsg = "You should train the dataset...";
        message_file.write(strMsg)
        message_file.close()
        return strMsg, -2
    if testcasecout < len(attack_label) :
        print("You should train the dataset for all attacks...")
        strMsg = "You should train the dataset for all attacks...";
        message_file.write(strMsg)
        message_file.close()
        return strMsg,-2
    message_file.close()
    return strMsg,1

####################################################################################################
#1. The system can take input as PCAP. to convert pcap to tsv
####################################################################################################
def pcaptoTSV(path):
    #path = "test2.pcap" #the pcap, pcapng, or tsv file to process.
    packet_limit = np.Inf
    FE_val = FE(path,packet_limit)
    strMsg = FE_val._preprocess()
    return strMsg, FE_val

def featureimportance_selection(mode,comb1):    
    #Testing/Training Data

    #path_mode_feature = f'./ml_model/Feature-Importance{mode}.fs'
    path_mode_feature = f'./ml_model/CFS-Result{mode}.cfs'
    print(path_mode_feature)
    if os.path.isfile(path_mode_feature):
        imFeatureList = []
        with open(path_mode_feature, "r") as f:
            for line in f:
                imFeatureList.append((line.strip())) 
    return comb1[imFeatureList]

###########################################################################################################################
# Then, apply reprocessing on tsv file to make it have the same features as N-BaIoT dataset which I shared the link above.
############################################################################################################################
def tsvTocsv(FE_val,path):
    start = time.time()
    df_summary = FE_val.getDataFeaturePacket()
    end = time.time()
    message_file=open(message_file_path,"a")
    print("elapsed time for parsing:"+str(end-start))
    strMsg = "\nelapsed time for parsing:"+str(end-start)
    message_file.write(strMsg)
    df_summary.to_csv(f'{path}.csv', index = False)
    message_file.close()
    return strMsg,df_summary

####################################################################################################
# Now, we give these features to the trained models to detect abnormal activities.
# The system should generate ALERT (Printing), once the abnormal is found by at least one model.
####################################################################################################
def testForAttack(df_summary):
    
    isAlert = 0
    #print(df_summary)
    for idx in range(len(attack_label)):
        isAttack = 0
        testX = featureimportance_selection(idx+1,df_summary)

        Pkl_Filename = f'./ml_model/Pickle_RL_Model{idx+1}.pkl' ;
        with open(Pkl_Filename, 'rb') as file:  
            Pickled_LR_Model = pickle.load(file)
        prediction = Pickled_LR_Model.predict(testX)
        #print(prediction)
        for pidx in range(len(prediction)):
            if prediction[pidx] == 1:
                isAttack = isAttack +1;
                #break;
        if (isAttack/(len(prediction))) >= 0.01:
        #if isAttack > 1:    
        #print(f'>>>>>>>>>>>>Checking for Attack{idx} {attack_label[idx]}...<<<<<<<<<<<<<<')
        #if isAttack == 1:
            isAlert = 1
            #print(f'{attack_label[idx]}: Abnormal')                    
            #print(f'attack packets :{isAttack} of {len(prediction)}')
        
            
            break            
        #else:
            #print(f'{attack_label[idx]}: Normal')
            #print(f'attack packets :{isAttack} of {len(prediction)}')

            #print("\n***Normal***\n")
    return isAlert

####################################################################################################
# Then print the output if NORMAL or ABNORMAL.
####################################################################################################
def AlertAttack(isAlert):
    message_file=open(message_file_path,"a")
    returnState = 0   
    strMsg = ""     
    if(isAlert):

        print("----------------------------------------");
        strMsg = strMsg + "\n----------------------------------------";
        message_file.write("\n----------------------------------------")        
        print("\nALERT SUSPICIOUS ACTIVITY FOUND!!!\n");
        strMsg = strMsg + "\n\nALERT SUSPICIOUS ACTIVITY FOUND!!!\n";
        message_file.write("\n\nALERT SUSPICIOUS ACTIVITY FOUND!!!\n")
        print("\nAbnormal attack!\n");
        strMsg = strMsg + "\n\nAbnormal attack!\n";
        message_file.write("\n\nAbnormal attack!\n")
        
        print("----------------------------------------");
        strMsg = strMsg + "\n----------------------------------------";
        message_file.write("\n----------------------------------------")
        returnState = -1;
    else:
        print("----------------------------------------");
        strMsg = strMsg + "\n----------------------------------------";
        message_file.write("\n----------------------------------------")
        
        print("\nNormal!\n");
        
        strMsg = strMsg + "\n\nNormal!\n";
        message_file.write("\n\nNormal!\n")
        
        print("----------------------------------------");
        strMsg = strMsg + "\n----------------------------------------\n";
        message_file.write("\n----------------------------------------")
        
        returnState = 0
    message_file.close()    
    return strMsg,returnState 

####################################################################################################
# Phase2 : main function
####################################################################################################
def beginTestforAttack(path):
    message_file = open(message_file_path, "w")
    strReturnMsg = ""
    message_file.write(strReturnMsg)
    message_file.close();
    strMsg,returnvalue = _prep_()
    strReturnMsg = strReturnMsg + strMsg
    if(returnvalue == -2 or returnvalue == 0):
        return strReturnMsg,-2
    
    strMsg, FE_val = pcaptoTSV(path)
    strReturnMsg = strReturnMsg + strMsg
    
    strMsg,df_summary = tsvTocsv(FE_val,path)
    strReturnMsg = strReturnMsg + strMsg
    
    isAlert = testForAttack(df_summary); 

    strMsg,returnValue = AlertAttack(isAlert)
    strReturnMsg = strReturnMsg + strMsg    
    
    return strReturnMsg, returnValue