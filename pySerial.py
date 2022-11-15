import serial
import time
arduino = serial.Serial(port='COM17', baudrate=115200, timeout=.1)
# def write_read(x):
#     arduino.write(bytes(x, 'utf-8'))
#     time.sleep(0.05)
#     data = arduino.readline()
#     return data
# while True:
#     num = input("Enter a number: ") # Taking input from user
#     value = write_read(num)
#     print(int(value)) # printing the value

time.sleep(5)
while True:
    # if int(arduino.read(size=1)) == 1:
    #     print("ewrew")
    # else:
    #     print("ere")
    print(arduino.readline().decode("utf-8"))
    time.sleep(0.05)