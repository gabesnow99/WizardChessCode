# ########################################### TEST LISTS SERIAL PORT NAMES ########################################################
# import serial
# import serial.tools.list_ports

# def list_serial_ports():
#     ports = serial.tools.list_ports.comports()
#     return [port.device for port in ports]

# print(list_serial_ports())

# ########################################### TEST CHECKS ALL AVAILABLE SERIAL PORTS ########################################################

# import serial
# import time
# import sys
# import glob

# def list_serial_ports():
#     """Lists serial port names"""
#     if sys.platform.startswith('win'):
#         ports = ['COM%s' % (i + 1) for i in range(256)]
#     elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
#         # this excludes your current terminal "/dev/tty"
#         ports = glob.glob('/dev/tty[A-Za-z]*')
#     elif sys.platform.startswith('darwin'):
#         ports = glob.glob('/dev/tty.*')
#     else:
#         raise EnvironmentError('Unsupported platform')

#     result = []
#     for port in ports:
#         try:
#             s = serial.Serial(port)
#             s.close()
#             result.append(port)
#         except (OSError, serial.SerialException):
#             pass
#     return result

# def check_serial_communication(port, baudrate=9600, timeout=1):
#     try:
#         ser = serial.Serial(port, baudrate, timeout=timeout)
        
#         if ser.is_open:
#             print(f"Successfully connected to {port} at baudrate {baudrate}")
        
#         # Example: Write data to the serial port
#         ser.write(b'Hello, serial port!\n')
        
#         # Example: Read data from the serial port
#         time.sleep(2)  # Give some time for the data to be received
#         if ser.in_waiting > 0:
#             received_data = ser.read(ser.in_waiting).decode('utf-8')
#             print(f"Received data: {received_data}")
#         else:
#             print("No data received.")
        
#         # Close the serial port
#         ser.close()
#         print(f"Closed connection to {port}")

#     except serial.SerialException as e:
#         print(f"Failed to connect to {port}: {e}")

# if __name__ == "__main__":
#     available_ports = list_serial_ports()
#     if available_ports:
#         print("Available serial ports:")
#         for port in available_ports:
#             print(port)
#     else:
#         print("No available serial ports found.")
    
#     # Replace 'COM3' with the appropriate serial port for your system
#     check_serial_communication('COM3')
#     check_serial_communication('COM4')

# ########################################### TEST CHECKS THE BOTTOM OF THE SCRIPT HAS BEEN EXECUTED ########################################################
#     print('made it to the bottom of the script')
