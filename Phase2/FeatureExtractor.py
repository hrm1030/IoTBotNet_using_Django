#Check if cython code has been compiled
import os
import subprocess


#Import dependencies
import Phase2.netStat as ns
import csv
import numpy as np
from scapy.all import *
import os.path
import platform
import subprocess
import pandas as pd
message_file_path = "./homeview/static/message/phase2_output.ms";
class FE:
    def __init__(self,file_path,limit=np.inf):
        self.path = file_path
        self.limit = limit
        self.parse_type = None #unknown
        self.curPacketIndx = 0
        self.tsvin = None #used for parsing TSV file
        self.scapyin = None #used for parsing pcap with scap
        
        ### Prep pcap ##
    def _preprocess(self):    
        strprep  = self.__prep__()

        ### Prep Feature extractor (AfterImage) ###
        maxHost = 100000000000
        maxSess = 100000000000
        self.nstat = ns.netStat(np.nan, maxHost, maxSess)

        return strprep

    def _get_tshark_path(self):
        if platform.system() == 'Windows':
            return 'C:\Program Files\Wireshark\\tshark.exe'
        else:
            system_path = os.environ['PATH']
            for path in system_path.split(os.pathsep):
                filename = os.path.join(path, 'tshark')
                if os.path.isfile(filename):
                    return filename
        return ''

    def __prep__(self):
        strprep = "";
        message_file=open(message_file_path,"a")
        ### Find file: ###
        if not os.path.isfile(self.path):  # file does not exist
            print("File: " + self.path + " does not exist")
            strprep = "File: " + self.path + " does not exist";
            message_file.write(strprep)
            message_file.close()
            raise Exception()

        ### check file type ###
        type = self.path.split('.')[-1]

        self._tshark = self._get_tshark_path()
        ##If file is TSV (pre-parsed by wireshark script)
        if type == "tsv":
            self.parse_type = "tsv"

        ##If file is pcap
        elif type == "pcap" or type == 'pcapng':
            # Try parsing via tshark dll of wireshark (faster)
            if os.path.isfile(self._tshark):
                self.pcap2tsv_with_tshark()  # creates local tsv file
                self.path += ".tsv"
                self.parse_type = "tsv"
            else: # Otherwise, parse with scapy (slower)
                message_file.close()
                message_file=open(message_file_path,"a")
    
                print("tshark not found. Trying scapy...")
                strprep = strprep + "\ntshark not found. Trying scapy...";
                message_file.write(strprep)
                self.parse_type = "scapy"
        else:
            message_file.close()
            message_file=open(message_file_path,"a")
    
            print("File: " + self.path + " is not a tsv or pcap file")
            strprep = strprep + ("\nFile: " + self.path + " is not a tsv or pcap file")
            message_file.write(strprep)
            message_file.close()
            raise Exception()

        ### open readers ##
        if self.parse_type == "tsv":
            maxInt = sys.maxsize
            decrement = True
            message_file.close()
            message_file=open(message_file_path,"a")
    
            while decrement:
                # decrease the maxInt value by factor 10
                # as long as the OverflowError occurs.
                decrement = False
                try:
                    csv.field_size_limit(maxInt)
                except OverflowError:
                    maxInt = int(maxInt / 10)
                    decrement = True      
            message_file.close()
            message_file=open(message_file_path,"a")
            
            print("counting lines in file...")
            strprep = strprep + "\ncounting lines in file..."
            message_file.write("\ncounting lines in file...")
            num_lines = sum(1 for line in open(self.path))
            print("There are " + str(num_lines) + " Packets.")
            strprep = strprep + "\nThere are " + str(num_lines) + " Packets."
            message_file.write("\nThere are " + str(num_lines) + " Packets.")

            print("\n***Parsing pcap into csv file...***\n")  
            strprep = strprep + "\n\n***Parsing pcap into csv file...***\n"
            message_file.write("\n\n***Parsing pcap into csv file...***\n")
            self.limit = min(self.limit, num_lines-1)
            self.tsvinf = open(self.path, 'rt', encoding="utf8")
            self.tsvin = csv.reader(self.tsvinf, delimiter='\t')
            row = self.tsvin.__next__() #move iterator past header

        else: # scapy
            message_file.close()
            message_file=open(message_file_path,"a")
    
            print("Reading PCAP file via Scapy...")
            strprep = strprep + "\nReading PCAP file via Scapy..."
            message_file.write("\nReading PCAP file via Scapy...")
            self.scapyin = rdpcap(self.path)
            self.limit = len(self.scapyin)
            print("Loaded " + str(len(self.scapyin)) + " Packets.")
            strprep = strprep + "\nLoaded " + str(len(self.scapyin)) + " Packets."
            message_file.write("\nLoaded " + str(len(self.scapyin)) + " Packets.")
        message_file.close()
        return strprep
    def display(self):
        while(self.curPacketIndx < 5):
            x = self.get_next_vector()
            print(self.curPacketIndx)
            print(x)
    def getDataFeature(self):
        FEATURE_COLUMNS =  self.nstat.getNetStatHeaders()
        FEATURE_COLUMNS_DICT = {key: None for key in FEATURE_COLUMNS}
        return FEATURE_COLUMNS_DICT        
    def getDataFeaturePacket(self):
        FEATURE_COLUMNS =  self.nstat.getNetStatHeaders()
        FEATURE_COLUMNS_DICT = {key: None for key in FEATURE_COLUMNS}
        message_file=open(message_file_path,"a")
        df_length = 0
        resultcsvlist = []
        while(True):
            nextvector = self.get_next_vector()
            nextvector_list = list(nextvector) #numpy to list
            if not nextvector_list:
                message_file.close()
                message_file=open(message_file_path,"a") 
                df_summary = pd.DataFrame(resultcsvlist,columns = FEATURE_COLUMNS)
                message_file.close()
                return df_summary;
                #return df_summary.iloc[:,:28];
            else:
                if (df_length % 10000 == 0):
                    print(df_length)
                    message_file.write(f'\n{df_length}')
                    message_file.close()
                    message_file=open(message_file_path,"a")            
                df_length = df_length +1
                resultcsvlist.append(nextvector_list)
                #df_summary.loc[df_length] = nextvector_list
                #df_length = df_length +1
        
                
    def get_next_vector(self):
        if self.curPacketIndx == self.limit:
            if self.parse_type == 'tsv':
                self.tsvinf.close()
            return []

        ### Parse next packet ###
        if self.parse_type == "tsv":
            row = self.tsvin.__next__()
            IPtype = np.nan
            timestamp = row[0]
            framelen = row[1]
            srcIP = ''
            dstIP = ''
            if row[4] != '':  # IPv4
                srcIP = row[4]
                dstIP = row[5]
                IPtype = 0
            elif row[17] != '':  # ipv6
                srcIP = row[17]
                dstIP = row[18]
                IPtype = 1
            srcproto = row[6] + row[
                8]  # UDP or TCP port: the concatenation of the two port strings will will results in an OR "[tcp|udp]"
            dstproto = row[7] + row[9]  # UDP or TCP port
            srcMAC = row[2]
            dstMAC = row[3]
            if srcproto == '':  # it's a L2/L1 level protocol
                if row[12] != '':  # is ARP
                    srcproto = 'arp'
                    dstproto = 'arp'
                    srcIP = row[14]  # src IP (ARP)
                    dstIP = row[16]  # dst IP (ARP)
                    IPtype = 0
                elif row[10] != '':  # is ICMP
                    srcproto = 'icmp'
                    dstproto = 'icmp'
                    IPtype = 0
                elif srcIP + srcproto + dstIP + dstproto == '':  # some other protocol
                    srcIP = row[2]  # src MAC
                    dstIP = row[3]  # dst MAC

        elif self.parse_type == "scapy":
            packet = self.scapyin[self.curPacketIndx]
            IPtype = np.nan
            timestamp = packet.time
            framelen = len(packet)
            if packet.haslayer(IP):  # IPv4
                srcIP = packet[IP].src
                dstIP = packet[IP].dst
                IPtype = 0
            elif packet.haslayer(IPv6):  # ipv6
                srcIP = packet[IPv6].src
                dstIP = packet[IPv6].dst
                IPtype = 1
            else:
                srcIP = ''
                dstIP = ''

            if packet.haslayer(TCP):
                srcproto = str(packet[TCP].sport)
                dstproto = str(packet[TCP].dport)
            elif packet.haslayer(UDP):
                srcproto = str(packet[UDP].sport)
                dstproto = str(packet[UDP].dport)
            else:
                srcproto = ''
                dstproto = ''

            srcMAC = packet.src
            dstMAC = packet.dst
            if srcproto == '':  # it's a L2/L1 level protocol
                if packet.haslayer(ARP):  # is ARP
                    srcproto = 'arp'
                    dstproto = 'arp'
                    srcIP = packet[ARP].psrc  # src IP (ARP)
                    dstIP = packet[ARP].pdst  # dst IP (ARP)
                    IPtype = 0
                elif packet.haslayer(ICMP):  # is ICMP
                    srcproto = 'icmp'
                    dstproto = 'icmp'
                    IPtype = 0
                elif srcIP + srcproto + dstIP + dstproto == '':  # some other protocol
                    srcIP = packet.src  # src MAC
                    dstIP = packet.dst  # dst MAC
        else:
            return []

        self.curPacketIndx = self.curPacketIndx + 1


        ### Extract Features
        try:
            return self.nstat.updateGetStats(IPtype, srcMAC, dstMAC, srcIP, srcproto, dstIP, dstproto,
                                                 int(framelen),
                                                 float(timestamp))
        except Exception as e:
            print(e)
            return []


    def pcap2tsv_with_tshark(self):
        print('Parsing with tshark...')
        fields = "-e frame.time_epoch -e frame.len -e eth.src -e eth.dst -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e udp.srcport -e udp.dstport -e icmp.type -e icmp.code -e arp.opcode -e arp.src.hw_mac -e arp.src.proto_ipv4 -e arp.dst.hw_mac -e arp.dst.proto_ipv4 -e ipv6.src -e ipv6.dst"
        cmd =  '"' + self._tshark + '" -r '+ self.path +' -T fields '+ fields +' -E header=y -E occurrence=f > '+self.path+".tsv"
        subprocess.call(cmd,shell=True)
        print("tshark parsing complete. File saved as: "+self.path +".tsv")

    def get_num_features(self):
        return len(self.nstat.getNetStatHeaders())
