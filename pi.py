import serial
import requests
import json
import time
import glob

# 서버 URL
SERVER_URL = 'http://localhost:8080/api/upload.api'

# USB포트 리스트
USB_PORTS = ['/dev/usb_hub_port1', '/dev/usb_hub_port2', '/dev/usb_hub_port3', '/dev/usb_hub_port4',
             '/dev/usb_hub_port5', '/dev/usb_hub_port6', '/dev/usb_hub_port7', '/dev/usb_hub_port8',
             '/dev/usb_hub_port9', '/dev/usb_hub_port10']

# 라즈베리파ㅣ이 IP와 MAC주소 설정
RASPBERRY_PI_IP = '192.168.1.1'
RASPBERRY_PI_MAC = '00-00-00-00-00-00'

def read_battery_data(port):
    try:
        print(f"Trying to read from {port}")
        ser = serial.Serial(port, 9600, timeout=1)
        line = ser.readline().decode('utf-8').strip()
        ser.close()
        if line:
            print(f"Data from {port}: {line}")
        else:
            print(f"No data read from {port}")
        return line
    except serial.SerialException as e:
        print(f"Error reading from {port}: {e}")
        return None

def main():
    while True:
        for i, port in enumerate(USB_PORTS, 1):
            data = read_battery_data(port)
            if data:
                try:
                    battery_data = json.loads(data)
                    battery_data.update({
                        "IP": RASPBERRY_PI_IP,
                        "MAC": RASPBERRY_PI_MAC,
                        "UsbPortLocation": str(i),
                        "UploadTime": time.strftime("%Y-%m-%d %H:%M:%S %f")
                    })
                    response = requests.post(SERVER_URL, json=battery_data)
                    if response.status_code == 200:
                        print(f"Data sent successfully from {port}")
                    else:
                        print(f"Failed to send data from {port}, status code: {response.status_code}")
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from {port}: {e}")
            else:
                print(f"No data from {port}")
        time.sleep(5)

if __name__ == '__main__':
    main()
