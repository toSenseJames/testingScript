import serial
import time
import sys

print(sys.platform)
if sys.platform == "win32":
    timer = time.clock
else:
    timer = time.time

# Sample programs that can be selected during the loading prompt
# Can be changed to other impedance values if desired
program1 = ['9.7', '9.72','9.75','9.72']
program2 = ['20', '20.1', '20.2', '20.3', '20.4', '20.5', '20.4', '20.3', '20.2', '20.1']

print("Program key:")
print("1: 19.76 to 20.2 Ohms, 1 step")
print("2: 20 to 20.5 Ohms, 5 steps")

try:
    waveformFile = open('Example Waveform.csv', 'r')
except FileNotFoundError:
    print("CSV not present in directory.")
else:
    print("Other: Read from Example Waveform.csv in script directory.")

program = int(input("Enter program number: "))
delay = float(input("Enter pulse delay time: "))
text = input("Data printout? Y/N: ")

index = 0
startTime = timer()
ser = serial.Serial('COM3',115200,timeout=0)

if program == 1:
    waveform = program1
    print("Program 1 selected.")
elif program == 2:
    waveform = program2
    print("Program 2 selected.")

while 1:
    newTime = timer()
    if (newTime - startTime) > delay:
        startTime = newTime
        if program == 1 or program == 2:
            value = '1' + str(waveform[index])
            if index < len(waveform) - 1:
                index = index + 1
            else:
                index = 0
        else:
            value = '1' + waveformFile.readline()
        ser.write(value.encode())

    if text == "Y":
        if ser.in_waiting > 0:
            try:
                dataFeed = ser.readline()
                dataFeed = dataFeed.rstrip()
                print(dataFeed)
            except ser.SerialTimeoutException:
                print('Data could not be read')
        
    time.sleep(0.01)