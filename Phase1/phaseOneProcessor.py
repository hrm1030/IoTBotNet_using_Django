'''
To do this, I want you to start doing these requirements for the features:
1. Please combine all files of dataset in one file.
2. Seperate each Attack with a benign data (Example: Attack1 + Benign, Attack2 + Benign + ......).
3. Then do sampling to the data, so Attack and Benign will have similar number (Balanced data).
4. Now, apply Feature Selection technique to each section of Attack.
5. Train the selected algorithms
6. Test them and show accuracy and false positive (Please show the accuracies of each algorithm).

'''
#print("\nImporting Packages...##",end=" ")
import pandas as pd
import numpy as np
import time
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.utils import shuffle
import os

message_file_path = "./homeview/static/message/phase1_output.ms";
####################################################################################################
#1. Please combine all files of dataset in one file.
#2. Seperate each Attack with a benign data (Example: Attack1 + Benign, Attack2 + Benign + ......).
####################################################################################################
def combineTrainDataSet(mode):
    message_file = open(message_file_path, "a")
    strStatusMsg = "";
    dataset_url = "./dataset";

    print("IMPORT DONE.\n")
    strStatusMsg = strStatusMsg + "\nIMPORT DONE.\n"
    message_file.write("\nIMPORT DONE.\n");
    print("Reading Data...##\n",end=" ")
    
    # Loading benign_traffic
    print("\t Reading benign_traffic...##\n",end=" ")

    strStatusMsg = strStatusMsg + "\n\t Reading benign_traffic...##\n"
    message_file.write("\n\t Reading benign_traffic...##\n");
    message_file.close()
    message_file=open(message_file_path,"a")
    
    cdata_1=pd.read_csv(dataset_url+"/benign/benign_traffic_11.csv")
    cdata_2=pd.read_csv(dataset_url+"/benign/benign_traffic_21.csv")
    cdata_3=pd.read_csv(dataset_url+"/benign/benign_traffic_31.csv")
    cdata_4=pd.read_csv(dataset_url+"/benign/benign_traffic_41.csv")
    cdata_5=pd.read_csv(dataset_url+"/benign/benign_traffic_51.csv")
    cdata_6=pd.read_csv(dataset_url+"/benign/benign_traffic_61.csv")
    cdata_7=pd.read_csv(dataset_url+"/benign/benign_traffic_71.csv")
    cdata_8=pd.read_csv(dataset_url+"/benign/benign_traffic_81.csv")
    cdata_9=pd.read_csv(dataset_url+"/benign/benign_traffic_91.csv")
    cdata=pd.concat([cdata_1,cdata_2,cdata_3,cdata_4,cdata_5,cdata_6,cdata_7,cdata_8,cdata_9],axis=0) # cdata: all benign_traffic
    cdata = shuffle(cdata);
    attack=cdata
    if mode == 1 : #Attack1 
        print("\t Reading Ack Attack...##\n")
        strStatusMsg = strStatusMsg + "\n\t Reading Ack Attack...##\n"
        message_file.write("\n\t Reading Ack Attack...##\n"); 
        message_file.close()
        message_file=open(message_file_path,"a")
    
        ack_1=pd.read_csv(dataset_url+"/attack/ack/ack_1.csv")
        ack_2=pd.read_csv(dataset_url+"/attack/ack/ack_2.csv")
        ack_3=pd.read_csv(dataset_url+"/attack/ack/ack_3.csv")
        ack_4=pd.read_csv(dataset_url+"/attack/ack/ack_4.csv")
        ack_5=pd.read_csv(dataset_url+"/attack/ack/ack_5.csv")
        ack_6=pd.read_csv(dataset_url+"/attack/ack/ack_6.csv")
        ack_7=pd.read_csv(dataset_url+"/attack/ack/ack_7.csv")
        ack=pd.concat([ack_1,ack_2,ack_3,ack_4,ack_5,ack_6,ack_7],axis=0)
        
        attack=shuffle(ack)
        
        
    if mode == 2 : #Attack2
        print("\t Reading combo Attack...##\n")
        strStatusMsg = strStatusMsg + "\n\t Reading combo Attack...##\n"
        message_file.write("\n\t Reading combo Attack...##\n");
        message_file.close()
        message_file=open(message_file_path,"a")
        combo_1=pd.read_csv(dataset_url+"/attack/combo/combo_1.csv")
        combo_2=pd.read_csv(dataset_url+"/attack/combo/combo_2.csv")
        combo_3=pd.read_csv(dataset_url+"/attack/combo/combo_3.csv")
        combo_4=pd.read_csv(dataset_url+"/attack/combo/combo_4.csv")
        combo_5=pd.read_csv(dataset_url+"/attack/combo/combo_5.csv")
        combo_6=pd.read_csv(dataset_url+"/attack/combo/combo_6.csv")
        combo_7=pd.read_csv(dataset_url+"/attack/combo/combo_7.csv")
        combo_8=pd.read_csv(dataset_url+"/attack/combo/combo_8.csv")
        combo_9=pd.read_csv(dataset_url+"/attack/combo/combo_9.csv")
        
        combo=pd.concat([combo_1,combo_2, combo_3,combo_4,combo_5,combo_6,combo_7,combo_8,combo_9],axis=0)
        
        attack=shuffle(combo)
        
        
        
    if mode == 3 : #Attack3
        
        print("\t Reading junk Attack...##\n")
        strStatusMsg = strStatusMsg + "\n\t Reading junk Attack...##\n"
        message_file.write("\n\t Reading junk Attack...##\n");
        message_file.close()
        message_file=open(message_file_path,"a")
    
        junk_1=pd.read_csv(dataset_url+"/attack/junk/junk_1.csv")
        junk_2=pd.read_csv(dataset_url+"/attack/junk/junk_2.csv")
        junk_3=pd.read_csv(dataset_url+"/attack/junk/junk_3.csv")
        junk_4=pd.read_csv(dataset_url+"/attack/junk/junk_4.csv")
        junk_5=pd.read_csv(dataset_url+"/attack/junk/junk_5.csv")
        junk_6=pd.read_csv(dataset_url+"/attack/junk/junk_6.csv")
        junk_7=pd.read_csv(dataset_url+"/attack/junk/junk_7.csv")
        junk_8=pd.read_csv(dataset_url+"/attack/junk/junk_8.csv")
        junk_9=pd.read_csv(dataset_url+"/attack/junk/junk_9.csv")
        
        junk=pd.concat([junk_1,junk_2, junk_3,junk_4,junk_5,junk_6,junk_7,junk_8,junk_9],axis=0)
        
        attack=shuffle(junk)
        
    
    if mode == 4: #Attack4
        print("\t Reading scan Attack...##\n")
        strStatusMsg = strStatusMsg + "\n\t Reading scan Attack...##\n"
        message_file.write("\n\t Reading scan Attack...##\n");
        message_file.close()
        message_file=open(message_file_path,"a")
    
        scan_11=pd.read_csv(dataset_url+"/attack/scan/scan_11.csv")
        scan_12=pd.read_csv(dataset_url+"/attack/scan/scan_12.csv")
        
        scan_21=pd.read_csv(dataset_url+"/attack/scan/scan_21.csv")
        scan_22=pd.read_csv(dataset_url+"/attack/scan/scan_22.csv")
        scan_3=pd.read_csv(dataset_url+"/attack/scan/scan_31.csv")
        scan_41=pd.read_csv(dataset_url+"/attack/scan/scan_41.csv")
        scan_42=pd.read_csv(dataset_url+"/attack/scan/scan_42.csv")
        scan_51=pd.read_csv(dataset_url+"/attack/scan/scan_51.csv")
        scan_52=pd.read_csv(dataset_url+"/attack/scan/scan_52.csv")
        scan_61=pd.read_csv(dataset_url+"/attack/scan/scan_61.csv")
        scan_62=pd.read_csv(dataset_url+"/attack/scan/scan_62.csv")
        scan_7=pd.read_csv(dataset_url+"/attack/scan/scan_91.csv")
        
        scan_81=pd.read_csv(dataset_url+"/attack/scan/scan_71.csv")
        scan_82=pd.read_csv(dataset_url+"/attack/scan/scan_72.csv")
        scan_91=pd.read_csv(dataset_url+"/attack/scan/scan_81.csv")
        scan_92=pd.read_csv(dataset_url+"/attack/scan/scan_82.csv")
        
        scan=pd.concat([scan_11,scan_12,scan_21,scan_22,scan_3,scan_41,scan_42,
                        scan_51,scan_52,scan_61,scan_62,scan_7,scan_81,scan_82,scan_91,scan_92],axis=0)
        
        attack=shuffle(scan)
       
        
    if mode == 5: #Attack5
        
        print("\t Reading syn Attack...##\n")
        strStatusMsg = strStatusMsg + "\n\t Reading syn Attack...##\n"
        message_file.write("\n\t Reading syn Attack...##\n");
        message_file.close()
        message_file=open(message_file_path,"a")
    
        syn_1=pd.read_csv(dataset_url+"/attack/syn/syn_1.csv")
        syn_2=pd.read_csv(dataset_url+"/attack/syn/syn_2.csv")
        syn_3=pd.read_csv(dataset_url+"/attack/syn/syn_3.csv")
        syn_4=pd.read_csv(dataset_url+"/attack/syn/syn_4.csv")
        syn_5=pd.read_csv(dataset_url+"/attack/syn/syn_5.csv")
        syn_6=pd.read_csv(dataset_url+"/attack/syn/syn_6.csv")
        syn_7=pd.read_csv(dataset_url+"/attack/syn/syn_7.csv")
        
        syn=pd.concat([syn_1,syn_2,syn_4,syn_5,syn_6,syn_3,syn_7],axis=0)
        
        attack=shuffle(syn)
        

    if mode == 6: #Attack6
        
        print("\t Reading tcp Attack...##\n")
        strStatusMsg = strStatusMsg + "\n\t Reading tcp Attack...##\n"
        message_file.write("\n\t Reading tcp Attack...##\n");
        message_file.close()
        message_file=open(message_file_path,"a")
    
        tcp_1=pd.read_csv(dataset_url+"/attack/tcp/tcp_1.csv")
        tcp_2=pd.read_csv(dataset_url+"/attack/tcp/tcp_2.csv")
        tcp_3=pd.read_csv(dataset_url+"/attack/tcp/tcp_3.csv")
        tcp_4=pd.read_csv(dataset_url+"/attack/tcp/tcp_4.csv")
        tcp_5=pd.read_csv(dataset_url+"/attack/tcp/tcp_5.csv")
        tcp_6=pd.read_csv(dataset_url+"/attack/tcp/tcp_6.csv")
        tcp_7=pd.read_csv(dataset_url+"/attack/tcp/tcp_7.csv")
        tcp_8=pd.read_csv(dataset_url+"/attack/tcp/tcp_8.csv")
        tcp_9=pd.read_csv(dataset_url+"/attack/tcp/tcp_9.csv")
        
        tcp=pd.concat([tcp_1,tcp_2, tcp_3,tcp_4,tcp_5,tcp_6,tcp_7,tcp_8,tcp_9],axis=0)
        
        attack=shuffle(tcp)
    
    if mode == 7: #Attack7
        print("\t Reading udp Attack...##\n")
        strStatusMsg = strStatusMsg + "\n\t Reading udp Attack...##\n"
        message_file.write("\n\t Reading udp Attack...##\n");
        message_file.close()
        message_file=open(message_file_path,"a")
    
        udp_11=pd.read_csv(dataset_url+"/attack/udp/udp_11.csv")
        udp_12=pd.read_csv(dataset_url+"/attack/udp/udp_12.csv")
        
        udp_21=pd.read_csv(dataset_url+"/attack/udp/udp_21.csv")
        udp_22=pd.read_csv(dataset_url+"/attack/udp/udp_22.csv")
        udp_3=pd.read_csv(dataset_url+"/attack/udp/udp_31.csv")
        udp_41=pd.read_csv(dataset_url+"/attack/udp/udp_41.csv")
        udp_42=pd.read_csv(dataset_url+"/attack/udp/udp_42.csv")
        udp_51=pd.read_csv(dataset_url+"/attack/udp/udp_51.csv")
        udp_52=pd.read_csv(dataset_url+"/attack/udp/udp_52.csv")
        udp_61=pd.read_csv(dataset_url+"/attack/udp/udp_61.csv")
        udp_62=pd.read_csv(dataset_url+"/attack/udp/udp_62.csv")
        udp_7=pd.read_csv(dataset_url+"/attack/udp/udp_91.csv")
        udp_81=pd.read_csv(dataset_url+"/attack/udp/udp_71.csv")
        udp_82=pd.read_csv(dataset_url+"/attack/udp/udp_72.csv")
        udp_91=pd.read_csv(dataset_url+"/attack/udp/udp_81.csv")
        udp_92=pd.read_csv(dataset_url+"/attack/udp/udp_82.csv")
        
        udp=pd.concat([udp_11,udp_12,udp_21,udp_22,udp_3,udp_41,udp_42,
                        udp_51,udp_52,udp_61,udp_62,udp_7,udp_81,udp_82,udp_91,udp_92],axis=0)
        
        attack=shuffle(udp)
    
    
    
    if mode == 8: #Attack8
        print("\t Reading udpplain Attack...##\n")
        strStatusMsg = strStatusMsg + "\n\t Reading udpplain Attack...##\n"
        message_file.write("\n\t Reading udpplain Attack...##\n");
        message_file.close()
        message_file=open(message_file_path,"a")
    
        udpplain_1=pd.read_csv(dataset_url+"/attack/udpplain/udpplain_1.csv")
        udpplain_2=pd.read_csv(dataset_url+"/attack/udpplain/udpplain_2.csv")
        udpplain_3=pd.read_csv(dataset_url+"/attack/udpplain/udpplain_3.csv")
        udpplain_4=pd.read_csv(dataset_url+"/attack/udpplain/udpplain_4.csv")
        udpplain_5=pd.read_csv(dataset_url+"/attack/udpplain/udpplain_5.csv")
        udpplain_6=pd.read_csv(dataset_url+"/attack/udpplain/udpplain_6.csv")
        udpplain_7=pd.read_csv(dataset_url+"/attack/udpplain/udpplain_7.csv")
        
        udpplain=pd.concat([udpplain_1,udpplain_2,udpplain_3,udpplain_4,udpplain_5,udpplain_6,udpplain_7],axis=0)
        
        attack=shuffle(udpplain)
       
    print("Read SucessFull.\n")

    strStatusMsg = strStatusMsg + "\nRead SucessFull.\n"
    message_file.write("\nRead SucessFull.\n");
    message_file.close()
    return cdata,attack,strStatusMsg

####################################################################################################
#3. Then do sampling to the data, so Attack and Benign will have similar number (Balanced data).
####################################################################################################

def samplingdataset(cdata,attack):
    message_file = open(message_file_path,"a") 
    strStatusMsg = ""
    print("\n***Number of Benign before balance.")    
    strStatusMsg = strStatusMsg + "\n\n***Number of Benign before balance."
    message_file.write("\n\n***Number of Benign before balance.")
    nlenbenign = int(cdata[cdata.columns[0]].count() )
    
    print("benign SHape: ",cdata.shape)
    strStatusMsg = strStatusMsg + f'\nbenign SHape: {cdata.shape}';
    message_file.write(f'\nbenign SHape: {cdata.shape}')
    print("\n***Number of Attack before balance.")    
    strStatusMsg = strStatusMsg + "\n\n***Number of Attack before balance.";
    message_file.write("\n\n***Number of Attack before balance.")
    nlenattack = int(attack[attack.columns[0]].count() )
    print("attack SHape: ",attack.shape)
    strStatusMsg = strStatusMsg + f'\nattack SHape: {attack.shape}';
    message_file.write(f'\nattack SHape: {attack.shape}')
    
    
    message_file.close()
    message_file=open(message_file_path,"a")
    
    #Then do sampling to the data, so Attack and Benign will have similar number (Balanced data).
    nBalancedNumber = 0
    if nlenattack < nlenbenign :
        nBalancedNumber = nlenattack 
        cdata = cdata[:nBalancedNumber+100]
    else:
        nBalancedNumber = nlenbenign
        attack = attack[:nBalancedNumber+100]
    #cdata = cdata[:nBalancedNumber]
    #attack = attack[:nBalancedNumber]
     
    print("\nNumber of Benign After balance.")  
    strStatusMsg = strStatusMsg + "\nNumber of Benign After balance.";  
    message_file.write("\nNumber of Benign After balance.")
    
    #checking the dimensions
    print("benign SHape: ",cdata.shape)
    strStatusMsg = strStatusMsg + f'\nbenign SHape: {cdata.shape}';
    message_file.write(f'\nbenign SHape: {cdata.shape}')
    
    print("\nNumber of Attack After balance.")    
    strStatusMsg = strStatusMsg + "\nNumber of Attack After balance."; 
    message_file.write("\nNumber of Attack After balance.") 
    
    #print(cdata.head())
    print("attack Shape : ",attack.shape)
    message_file.write(f'\nattack SHape: {attack.shape}')
    
    
    #Tagging benign as 0 and Attack as 1
    
    attack['Out']=1
    cdata['Out']=0
    
    #combining two DataFrames
    comb=pd.concat([cdata,attack],axis=0)
    print("The COMBINED shape : ",comb.shape)
    strStatusMsg = strStatusMsg + f'\nCOMBINED SHape: {comb.shape}';
    message_file.write(f'\nCOMBINED SHape: {comb.shape}')    
    comb=shuffle(comb)
    message_file.close()
    return comb, strStatusMsg

####################################################################################################
# to get training data and test data from dataset    
####################################################################################################
def getTrainingdata(comb1,Output):    
    #Testing/Training Data
    Xtrain,Xtest,Ytrain,Ytest=train_test_split(comb1,Output,test_size=0.3,random_state=47)##########################
    
    return Xtrain,Xtest,Ytrain,Ytest

####################################################################################################
# to get importance features using randomforest
####################################################################################################
def featureimportance_selection(mode,comb1,Output):    
    #Testing/Training Data

    from sklearn.ensemble import RandomForestClassifier
    
    path_mode_feature = f'ml_model/Feature-Importance{mode}.fs'
    if os.path.isfile(path_mode_feature):
        imFeatureList = []
        with open(path_mode_feature, "r") as f:
            for line in f:
                imFeatureList.append((line.strip()))        
    else:
        Xtrain,Xtest,Ytrain,Ytest= getTrainingdata(comb1,Output)
        clf = RandomForestClassifier()
        clf.fit(Xtrain, Ytrain)
        importances = pd.DataFrame({"feature":comb1.columns,"important_feature":comb1.columns,"importance":np.round(clf.feature_importances_,3)})
        importances = importances.sort_values("importance",ascending=False).set_index("feature")
        importances = importances.head(30)
        imFeatureList = importances.index.tolist()
        with open(path_mode_feature, "w") as f:
            for s in imFeatureList:
                f.write((s) +"\n")
    return comb1[imFeatureList]


####################################################################################################
#4. Now, apply Feature Selection technique to each section of Attack.
####################################################################################################
def featureSelection(mode,comb):  
    message_file = open(message_file_path,"a")  
    Output=comb['Out']
    strStatusMsg = ""
    
    comb=comb.drop(['Out'],axis=1)
    comb=comb.drop(['HpHp_L0.01_pcc'],axis=1)
    
     #apply Feature Selection technique to each section of Attack.
    comb1=featureimportance_selection(mode,comb,Output)
    
    Output=np.array(Output).flatten()
    print("After remove: ",comb.shape)
    strStatusMsg = strStatusMsg + f'\nAfter remove: {comb.shape}';
    message_file.write(f'\nAfter remove: {comb.shape}')
    print("\nThe OUTPUt is : \n",Output)
    strStatusMsg = strStatusMsg + f'\nThe OUTPUt is : {Output}';
    message_file.write(f'\nThe OUTPUt is : {Output}')
    print("\nOutput SHAPE : ",Output.shape)
    strStatusMsg = strStatusMsg + f'\nCOMBINED SHape: {Output.shape}';
    message_file.write(f'\nCOMBINED SHape: {Output.shape}')
   
    print("\nOutput SHAPE : ",comb1.shape)
    #comb_norm_arra=np.array(comb_norm)
    message_file.write(f'\nOutput SHape: {comb1.shape}')
    #print("After Norm : ",comb_norm_arra.shape)
    message_file.close()
    return comb1,Output,strStatusMsg


####################################################################################################
#5. Train the selected algorithms
#6. Test them and show accuracy  (Please show the accuracies of each algorithm).
####################################################################################################
def training_model(Xtrain,Xtest,Ytrain,Ytest,mode = 1):
    message_file = open(message_file_path,"a")
    attack_label = ["Ack","Combo","Junk","Scan","Syn","Tcp","Udp","Udpplain"] #attack_label: Attack list 

    attack_label_classifier = ["DecisionTreeRegressor","GaussianNB Classifier Model","RandomForestClassifier"] #classifier name
    strStatusMsg = ""
    print("\n\n************Attck "+str(mode)+" ("+attack_label[mode -1]+") ***************** \n")
    strStatusMsg = strStatusMsg + "\n\n************Attck "+str(mode)+" ("+attack_label[mode -1]+") ***************** \n"
    message_file.write("\n\n************Attck "+str(mode)+" ("+attack_label[mode -1]+") ***************** \n")
    nmodelNum = 0 
    
    fMaxProbValue = 0.0
    import pickle
    from sklearn.metrics import accuracy_score
    #model 1: DecisionTreeRegressor Naive Bayes Training
    from sklearn.tree import DecisionTreeRegressor

    print("\n\tRunning DecisionTreeRegressor . . . \n")
    strStatusMsg = strStatusMsg + "\n\tRunning DecisionTreeRegressor . . . \n"
    message_file.write("\n\tRunning DecisionTreeRegressor . . . \n")
    model_first=DecisionTreeRegressor()
    model_first.fit(Xtrain,Ytrain)
    
    message_file.close()
    message_file=open(message_file_path,"a")
    
    print(model_first.score(Xtest,Ytest)*100)
    modelFirstProb = model_first.score(Xtest,Ytest)
    print("Accuracy Score First MODEL is : ",modelFirstProb)
    strStatusMsg = strStatusMsg + f'Accuracy Score First MODEL is : {modelFirstProb}'
    message_file.write(f'Accuracy Score First MODEL is : {modelFirstProb}')
    #prediction_first=model_first.predict(readTemp())
    
    #print(prediction_first)
    if(fMaxProbValue < modelFirstProb) :   
         model = model_first;
         fMaxProbValue = modelFirstProb
         nmodelNum = 1
    
    message_file.close()
    message_file=open(message_file_path,"a")
     
    
    # #model2: Perceptron Classifier Training
    # from sklearn.linear_model import Perceptron
    # print("\n\tRunning Perceptron . . . \n")
    # strStatusMsg = strStatusMsg + "\n\tRunning Perceptron . . . \n"
    
    # model_second=Perceptron(eta0=0.2,max_iter=1000,tol=1e-3,verbose=0,early_stopping = True ,validation_fraction=0.1)
    # model_second.fit(Xtrain,Ytrain)
    # prediction_second=model_second.predict(Xtest)
    # print(model_second.score(Xtest,Ytest)*100)
    # modelSecondProb = accuracy_score(prediction_second,Ytest)
    # print("Accuracy Score Second MODEL is : ",modelSecondProb)
    # strStatusMsg = strStatusMsg + f'\nAccuracy Score Second MODEL is : {modelSecondProb}'
    # if(fMaxProbValue < modelSecondProb) :
    #      model = model_second
    #      fMaxProbValue = modelSecondProb
    #      nmodelNum = 2
    
    #model2: GaussianNB Classifier Training
    from sklearn.naive_bayes import GaussianNB
    print("\n\tRunning GaussianNB . . . \n")
    strStatusMsg = strStatusMsg + "\n\tRunning GaussianNB . . . \n"
    message_file.write("\n\tRunning GaussianNB . . . \n")

    message_file.close()
    message_file=open(message_file_path,"a")
    
    model_second=GaussianNB()
    model_second.fit(Xtrain,Ytrain)
    prediction_second=model_second.predict(Xtest)
    print(model_second.score(Xtest,Ytest)*100)
    modelSecondProb = accuracy_score(prediction_second,Ytest)
    print("Accuracy Score Second MODEL is : ",modelSecondProb)
    strStatusMsg = strStatusMsg + f'\nAccuracy Score Second MODEL is : {modelSecondProb}'
    message_file.write(f'\nAccuracy Score Second MODEL is : {modelSecondProb}')
    if(fMaxProbValue < modelSecondProb) :
         model = model_second
         fMaxProbValue = modelSecondProb
         nmodelNum = 2
    message_file.close()
    message_file=open(message_file_path,"a")
         
    #model3: RandomForestClassifier Training
    from sklearn.ensemble import RandomForestClassifier
    print("\n\tRunning RandomForestClassifier . . .\n")
    strStatusMsg = strStatusMsg + "\n\tRunning RandomForestClassifier . . . \n"
    message_file.write("\n\tRunning RandomForestClassifier . . . \n")
    model_third = RandomForestClassifier()
    message_file.close()
    message_file=open(message_file_path,"a")
    
    model_third.fit(Xtrain,Ytrain)
    model = model_third  
    
    prediction_third=model_third.predict(Xtest)
    print(model_third.score(Xtest,Ytest)*100)
    modelThirdProb = accuracy_score(prediction_third,Ytest)
    print("Accuracy Score Third MODEL is : ",accuracy_score(prediction_third,Ytest))
    
    strStatusMsg = strStatusMsg + f'\nAccuracy Score Third MODEL is : {modelThirdProb}'
    message_file.write(f'\nAccuracy Score Third MODEL is : {modelThirdProb}')
    if(fMaxProbValue <= modelThirdProb) :   
         model = model_third
         fMaxProbValue = modelThirdProb
         nmodelNum = 3
    message_file.close()
    message_file=open(message_file_path,"a")
      
    print("\n>>>>>>>>>>>Selected model : "+attack_label_classifier[nmodelNum-1])
    strStatusMsg = strStatusMsg + "\n\n>>>>>>>>>>>Selected model : "+attack_label_classifier[nmodelNum-1]
    message_file.write("\n\n>>>>>>>>>>>Selected model : "+attack_label_classifier[nmodelNum-1])
    print("\n>>>>>>>>>>>>>>>>Accuracy Value : "+str(fMaxProbValue) +"\n");
    strStatusMsg = strStatusMsg + "\n>>>>>>>>>>>>>>>>Accuracy Value : "+str(fMaxProbValue) +"\n"
    message_file.write("\n>>>>>>>>>>>>>>>>Accuracy Value : "+str(fMaxProbValue) +"\n")
    message_file.close()
    message_file=open(message_file_path,"a")
    
    Pkl_Filename = f'ml_model/Pickle_RL_Model{mode}.pkl' ;
    print(Pkl_Filename);

    with open(Pkl_Filename, 'wb') as file:  
        pickle.dump(model, file)
    
    '''
    from matplotlib import pyplot as plt
    Ytest_p=Ytest[:100]
    prediction_third_p=prediction_third[:100]
    plt.xlabel('X(Time->)')
    plt.ylabel('0 For Clean Traffic(LOW) and Threat Traffic as 1(HIGH)')

    plt.plot(prediction_third_p,'r-',label="Predicted Attack")
    plt.plot(Ytest_p,'b--',label="Test Data")
    plt.legend(loc='upper left')
    plt.show()
    '''
    message_file.close()
    return nmodelNum,strStatusMsg

####################################################################################################
#  Phase 1: main function
####################################################################################################
def beginTrain():
     print("\n\n\tRunning main.py\n")
     strMsg = "\n\tRunning main.py\n"
     attack_size = 1
     start = time.time()
     message_file = open(message_file_path, "w")
     message_file.write(strMsg)
     message_file.close()

     for idx in range(attack_size):
         strStatusMsg = ""
         cdata,attack,strReturnMsg = combineTrainDataSet(idx+1)
         strStatusMsg = strStatusMsg + strReturnMsg
         comb,strReturnMsg = samplingdataset(cdata,attack)
         strStatusMsg = strStatusMsg + strReturnMsg
         comb1,Output,strReturnMsg = featureSelection(idx+1,comb)
         strStatusMsg = strStatusMsg + strReturnMsg
         Xtrain,Xtest,Ytrain,Ytest =getTrainingdata(comb1,Output)
         modelnum, strReturnMsg = training_model(Xtrain,Xtest,Ytrain,Ytest,idx+1)
         strStatusMsg = strStatusMsg + strReturnMsg
         strMsg = strMsg + strStatusMsg
     end = time.time()
     print("elapsed time for parsing:"+str(end-start))
     
     return "Success",strMsg



