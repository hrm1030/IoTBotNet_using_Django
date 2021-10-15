import sys
import Train_Model.trainmodel as tm
import Pcap_Parser.test as ta
import os

class MainScreen:
    def __init__(self):
        self.homeScreen()
    '''to display error in home screen'''
    def homeError(self):
        print("\nWrong choice . pls try again !");
        self.homeScreen();

    def quitSystem(self):
        print("Your choice is to Quit");
        print("Quiting....");
        print("End of Program");
        

    def returnToMenu(self):
        key = input("Would you like to return to main menu?(Y/y):");
        
        if key == "Y" or key == "y":
            self.homeScreen()
        else:
            self.quitSystem()   
         

    def testforAttacks(self):
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        
        i =0
        fileList = []
        print("\n-----------pcap file list----------")
        for line in files:
            type = line.split('.')[-1]
            if(type == "pcap"):
                fileList.append(line)
                i = i+1
                print(f'[{i}]. {line}')
        
            
        if(len(fileList) == 0):
            print("there is no any pcap file in current directory. please copy test pcap file to current directory")
            self.returnToMenu()
            
        print(f'\n')
        
        key = input("choose the test pcap file number:");
        pcapnumber = 0
        try:
            pcapnumber = int(key)
            it_is = True
        except ValueError:
            it_is = False
            
        if(pcapnumber > 0 and pcapnumber <= len(fileList) and it_is):
            print(fileList[pcapnumber-1])
            ta.testforattack(fileList[pcapnumber-1])
            
        else:
            print("try again!!!")
        self.returnToMenu()


    def trainModel(self):
        tm.beginTrain()
        self.returnToMenu()
        

    def Reset(self):
        print("Reset.")
        for idx in range(8):
            Pkl_Filename = f'ml_model/Pickle_RL_Model{idx+1}.pkl' ;
            os.remove(Pkl_Filename)
        self.returnToMenu()

    '''to display home screen'''
    def homeScreen(self):
        print("\n\n----------------------------------")
        print("Abnormal Attack Detector @ 2021");
        print("----------------------------------")
        print("[1] Test For Attacks");
        print("[2] Train Fhe Model");
        print("[3] Reset The Data In Models");
        print("[4] Exit");
        print("----------------------------------")
        
        key = input("Give your choice numbers :");
        
        if key == "1":
            self.testforAttacks()
        elif key == "2":
            self.trainModel()
        elif key == "3":
            self.Reset()
        elif key == "4":
            self.quitSystem()
        else:
            self.homeError()
if __name__ == "__main__":
    home =  MainScreen();
