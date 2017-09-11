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
program1 = [19.76, 20.20]
program2 = [31.73, 32.13]
program3 = [19.68, 19.96]
program4 = [31.52, 31.73]
#program2 = ['20', '20.1', '20.2', '20.3', '20.4', '20.5', '20.4', '20.3', '20.2', '20.1']

print("Program key:")
print("1: 19.76 to 20.2 Ohms (0.5), 1 step")
print("2: 31.73 to 32.13 Ohms (0.4), 1 step")
print("3: 19.68 to 19.96 Ohms (0.25), 1 step")
print("4: 31.52 to 31.73 Ohms (0.2), 1 step")

waveformFile = None
try:
    waveformFile = open('Example Waveform 2.csv', 'r')
except IOError:
    print("CSV not present in directory.")
else:
    print("Other: Read from Example Waveform.csv in script directory.")

program = int(input("Enter program number: "))
#delay = float(input("Enter pulse delay time (times below 0.1s may not operate correctly): "))
delay = 0.5
text = raw_input("Data printout? Y/N: ")
text = text.strip().lower()
index = 0
startTime = timer()

if sys.platform == "win32":
    ser = serial.Serial('COM6', 115200, timeout=0)
else:
    # ser = serial.Serial('/dev/cu.usbserial-A5053GIU', 115200, timeout=0)
    ser = serial.Serial('/dev/cu.usbmodem40111221', 115200, timeout=0)
    print(dir(ser))

if program == 1:
    waveform = program1
    print("Program 1 selected.")
elif program == 2:
    waveform = program2
    print("Program 2 selected.")
elif program == 3:
    waveform = program3
    print("Program 3 selected.")
elif program == 4:
    waveform = program4
    print("Program 4 selected.")

while 1:
    newTime = timer()
    if (newTime - startTime) > delay:
        startTime = newTime
        if program < 5:
            value = '1' + str(waveform[index])
            index = (index + 1) % len(waveform)
        else:
            value = '1' + waveformFile.readline()
        ser.write(value.encode())

    if text == "y":
        if ser.in_waiting > 0:
            line = []
            try:
                b = ser.read()
                while b != '\n':
                    line.append(b)
                    b = ser.read()
                # dataFeed = ser.readline()
                # dataFeed = dataFeed.rstrip()
                print(''.join(line))
            except serial.SerialTimeoutException:
                print('Data could not be read')
    else:
        ser.reset_input_buffer()

    time.sleep(0.001)

# end of file