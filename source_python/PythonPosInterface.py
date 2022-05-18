# -*- coding: utf-8 -*-
"""
Created on Sun May 15 21:34:58 2022

@author: BlackSheep
"""

#pip install pyserial
# https://pyserial.readthedocs.io/en/latest/shortintro.html
# https://pyserial.readthedocs.io/en/latest/pyserial_api.html

import serial
import time
import numpy as np
import pandas as pd


class imuBenchIf():
    def __init__(self, port='COM15', baud=9600, timeout=0.5):
        self.ser = serial.Serial(port, baud, timeout=timeout)
        
        
        while True:
            line = self.ser.readline()
            if "IMU" in line.decode("utf-8"):
                break
            
        print("imu bench ready")
        
    def parseFeedback(self):
        while True:
            line = self.ser.readline()
            if "ack" in line.decode("utf-8"):
                return "ack"
            if "nck" in line.decode("utf-8"):
                return "nack"
            if "done" in line.decode("utf-8"):
                return "done"
    
    def rotateArm(self, deg, block=True):
        b_string = bytes("1002 " + str(deg), 'utf-8')
        self.ser.write(b_string)
        
        while (block):
            if self.parseFeedback() == "done":
                break
        
    def rotateBase(self, deg, block=True):
        b_string = bytes("1004 " + str(deg), 'utf-8')
        self.ser.write(b_string)
        
        while (block):
            if self.parseFeedback() == "done":
                break
            
    def close(self):
        self.ser.close()
        
        
class imuInterface():
    def __init__(self, port='COM13', baud=57600, timeout=0.005):
        
        self.ser = serial.Serial(port, baud, timeout=timeout)

        b_string = bytes("#osrt", 'utf-8')
        self.ser.write(b_string)
        time.sleep(2)

            
    def close(self):
        self.ser.close()
        
        
    def getValues(self, minLen):
        
        #empty buffer
        
        line = self.ser.readlines()
        
        GyroList = []
        AccelList = []
        MagList = []

        while (len(GyroList) <= minLen) or (len(AccelList) <= minLen) or (len(MagList) <= minLen) :
            
            line = self.ser.readline()
            line = line.decode("utf-8")
            
            if "#G-R=" in line:
                
                try:
                    line = line.replace("#G-R=", "")
                    [GyroX, GyroY, GyroZ] = line.split(",")
                    GyroX = float(GyroX)
                    GyroY = float(GyroY)
                    GyroZ = float(GyroZ)
                    GyroList.append([GyroX, GyroY, GyroZ])
                    
                except:
                    print("line not complete Gyro")
                    
            if "#A-R=" in line:
                
                try:
                    line = line.replace("#A-R=", "")
                    [AccelX, AccelY, AccelZ] = line.split(",")
                    AccelX = float(AccelX)
                    AccelY = float(AccelY)
                    AccelZ = float(AccelZ)
                    AccelList.append([AccelX, AccelY, AccelZ])
                    
                except:
                    print("line not complete Accel")
                    
            if "#M-R=" in line:
                
                try:
                    line = line.replace("#M-R=", "")
                    [MagX, MagY, MagZ] = line.split(",")
                    MagX = float(MagX)
                    MagY = float(MagY)
                    MagZ = float(MagZ)
                    MagList.append([MagX, MagY, MagZ])
                
                except:
                    print("line not complete Mag")
                    
        return [GyroList, AccelList, MagList]
    
    def getMeanOfValues(self, minLen):
        
        [GyroList, AccelList, MagList] = self.getValues(minLen)
        
        GyroList = np.array(GyroList)
        AccelList = np.array(AccelList)
        MagList = np.array(MagList)
        
        GyroList = GyroList.mean(axis=0)
        AccelList = AccelList.mean(axis=0)
        MagList = MagList.mean(axis=0)
    
        return [GyroList.tolist(), AccelList.tolist(), MagList.tolist()]
    
    
benchIF = imuBenchIf()
imuIF = imuInterface()

meanListGyro = []
meanListAccel = []
meanListMag = []

noArmPos = 36
basePos = 36

for armPos in range(noArmPos//2):
    print(str(armPos) + "/" + str(noArmPos//2))
    
    print("base pos dir")
    for basePosNo in range(int(basePos)):
        benchIF.rotateBase(deg=360/basePos)
        time.sleep(2)
        
        [GyroList, AccelList, MagList] = imuIF.getMeanOfValues(20)
        
        #print("get cal data done")
        meanListGyro.append(GyroList)
        meanListAccel.append(AccelList)
        meanListMag.append(MagList)
    
    benchIF.rotateArm(deg=360/noArmPos)
    
    print("base neg dir")
    
    for basePosNo in range(int(basePos)):
        benchIF.rotateBase(deg=-360/basePos)
        time.sleep(2)
        
        [GyroList, AccelList, MagList] = imuIF.getMeanOfValues(20)

        #print("get cal data done")
        meanListGyro.append(GyroList)
        meanListAccel.append(AccelList)
        meanListMag.append(MagList)
        
    benchIF.rotateArm(deg=360/noArmPos)

    
print("move arm to start pos")
    
benchIF.rotateArm(deg=-360)

print("write csv file")
#export as csv
df = pd.DataFrame(meanListGyro)
df.to_csv("meanListGyro.csv", index=False, header=False)
df2 = pd.DataFrame(meanListAccel)
df2.to_csv("meanListAccel.csv", index=False, header=False)
df3 = pd.DataFrame(meanListMag)
df3.to_csv("meanListMag.csv", index=False, header=False)

benchIF.close()
imuIF.close()

print("test done")