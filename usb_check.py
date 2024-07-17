import serial
import serial.tools.list_ports

def list_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def read_battery_data(port):
    try:
        ser = serial.Serial(port, 9600, timeout=1)
        line = ser.readline().decode('utf-8').strip()
        ser.close()
        if line:
            print(f"Data from {port}: {line}")
        else:
            print(f"No data from {port}")
    except serial.SerialException as e:
        print(f"Error reading from {port}: {e}")

if __name__ == "__main__":
    ports = list_ports()
    for port in ports:
        read_battery_data(port)

# ACM usb 수동 더미데이터 체크 파일입니다.
