import serial
import sys

ser = serial.Serial('COM3')

filename = sys.argv[1]

with open(filename, 'w') as f:
    for _ in range(10):
        raw_data_line = ser.readline().decode('ascii')
        csv_data_line = ','.join(raw_data_line.split(' ')).rstrip()
        f.write(csv_data_line + '\n')

ser.flush()
ser.close()

