import pandas as pd 
import serial
import time

def serial_monitor(port='/dev/ttyUSB0', baud_rate=115200, timeout=1):
    """ Continuously monitor serial data from the ESP32, similar to VSCode monitor. """
    esp_data = False
    data_capture =  []
    try:
        # Open the serial port with the specified settings
        with serial.Serial(port, baud_rate, timeout=None) as ser:
            print(f"Monitoring serial port {port} at {baud_rate} baud rate. Press Ctrl+C to exit.")
            while True:
                if ser.in_waiting > 0:
                    # Read the incoming data
                    data = ser.readline().decode('utf-8', errors='ignore').strip()
                    # Print the data to the console
                    if ('XstartX' in data):
                        esp_data = True 

                    elif esp_data == True:
                        try:
                            print(data, type(data))
                            data_capture.append(float(data.strip('\n').strip(',')))
                            print(type(data_capture[-1]), data_capture[-1])
                        except Exception as e:
                            print('EXception ', e, 'data', data)
                    if ('XendX' in data):
                        esp_data = None
                        df = pd.DataFrame(data_capture)
                        df.to_csv('test.csv')
                    
                    if type(esp_data) == type(None):
                        print(data)
                        # then program will end the processing 
                # time.sleep(0.001)

    except serial.SerialException as e:
        print(f"Error opening serial port {port}: {e}")
        # exit()
    except KeyboardInterrupt:
        print("\nSerial monitoring stopped.")
        try:
            esp_data = False
            df = pd.DataFrame(data_capture)
            df.to_csv('test.csv')
        except Exception as e :
            print("error on saving the csv file", e)

if __name__ == "__main__":
    # Example: Adjust port and baud_rate based on your setup
    serial_monitor(port='COM3', baud_rate=115200)
