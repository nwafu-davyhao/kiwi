import serial.tools.list_ports

def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    if not ports:
        print("没有发现可用串口。")
    else:
        print("可用串口如下：")
        for port in ports:
            print(f"- 设备名: {port.device} | 描述: {port.description}")

if __name__ == "__main__":
    list_serial_ports()
