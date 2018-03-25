
#Author: Mohammad Manzur Murhsid
#University of Hartford, 2017-2018


import serial # import Serial Library
import numpy as np # Import numpy
import matplotlib.pyplot as plt #import matplotlib library
from drawnow import *
from io import BytesIO

tempSensor1 =[]
tempSensor2 =[]



arduinoData = serial.Serial('/dev/ttyUSB0', 9600) #Creating our serial object named arduinoData
plt.ion() #Tell matplotlib we want interactive mode to plot live data

def SensorData():  # creates a function that makes our desired plot
    plt.subplot(2,1,1)
    plt.plot(tempSensor1)
    plt.ylim(-5, 5)
    plt.subplot(2,1,2)
    plt.plot(tempSensor2)
    f = BytesIO()
    plt.savefig(f, format="svg")
    plt.ylim(-1, 1)  # sets the y axis limits

while True: # While loop that loops forever
    while (arduinoData.inWaiting()==0): #Wait here until there is data
        pass #do nothing
    arduinoString = arduinoData.readline() #read the line of text from the serial port
    data_decode = arduinoString.replace("\x00","")  # invalid data "\x00" comes in the serial data, so we need to strip these values
                                           # and replace with blank
    data_strip = str(data_decode.strip()) # striping the invalid value
    data_value = str(data_strip) # putting the stripped value into new data array

    dataArray = data_value.split(',')  # splitting the string into two data
    sensor1 = (dataArray[0])  #converting the first element of string to floating data
    sensor2 = (dataArray[1])  #converting the second element of string to floating data
    tempSensor1.append((float(sensor1)-1.65)*10)    #building out temporary array by appending sensor1 and forcing to start from zero
    tempSensor2.append((float(sensor2)-1.65)*10)    #building out temporary array by appending sensor2 and forcing to start from zero


    drawnow(SensorData)
    plt.pause(.000001)
    # save the figure as a bytes string in the svg format.


    f = BytesIO()
    plt.savefig(f, format="svg")

    rows = zip(tempSensor1 , tempSensor2) #z)  # combines lists together

    row_arr = np.array(rows)  # creates array from list
    np.savetxt("/home/manzur/catkin_ws/src/MS_thesis/Arduino_communication/test_2.csv",
            row_arr)  # save data in file (load w/np.loadtxt())

arduinoData.close()




