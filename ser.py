import serial
import time
import subprocess
from subprocess import Popen

#def read():
#	global msg, respond
ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200,timeout=0.5, writeTimeout=0)
out = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=0.5)
#out.flushOutput()
#out.write('D'.encode())
sense1 = ["/home/jj/drivers-adis16470/build/bin/adis_driver", "-p", "/dev/ttyUSB0", "-ic", 'SDM:://VEHICLE/ADISIMU/2001/IMU-R', "-r", "50"]
sense2 = ["/home/jj/drivers-adis16470/build/bin/adis_driver", "-p", "/dev/ttyUSB1", "-ic", 'SDM:://VEHICLE/ADISIMU/2001/IMU-R', "-r", "50"]
commands = [sense1, sense2]

curr_process = "None"
while 1:
	bytesToRead = ser.inWaiting()
	if bytesToRead > 0:
		line = ser.read(bytesToRead)
		msg = str(line)
		msg = msg.replace("b'","")
		msg = msg.replace("'", "")

		if(msg[:5] == "IMU 1"):
			out.flushInput()
			process = Popen(sense1)
			curr_process = "IMU1"
			out.write("CPRunnig IMU1".encode())

		if(msg[:5] == "IMU 2"):
			out.flushInput()
			process = Popen(sense2)
			curr_process = "IMU2"
			out.write("CPRunning IMU2".encode())

		if(msg[:5] == "IMU12"):
			out.flushInput()
			procs = [ Popen(i) for i in commands ]
			#for p in procs:
			#	p.wait()
			curr_process = "IMU12"
			out.write("CPRunnig IMU1&2".encode())

		if(msg[:3] == "END"):
			out.flushInput()
			if curr_process == "IMU12":
				for p in procs:
					p.kill()
			else:
				process.kill()
			out.write("CPNone".encode())

		print(msg[:6])
'''
def write():
	global out
	ser = serial.Serial
'''
