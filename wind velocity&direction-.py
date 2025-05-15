import serial
import time
import struct
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime

# RS485串口配置
SERIAL_PORT = '/dev/ttyUSB0'
BAUDRATE = 9600

# 请求帧：读取地址01，功能码03，起始寄存器0x0000，读取4个寄存器
REQUEST_FRAME = bytes.fromhex('01 03 00 00 00 04 44 09')

# 数据缓存
time_data = []
wind_speed_data = []
wind_direction_data = []

# 计算风速，风向
def parse_response(response):
    if len(response) < 13:
        print("响应长度不足")
        return None, None
    # 提取寄存器0的高字节
    reg0_high = response[3]
    reg0_low = response[4]
    wind_speed = ((reg0_high << 8) | reg0_low) / 10.0  # 单位 m/s

    # 提取寄存器2的高字节
    reg2_high = response[7]
    reg2_low = response[8]
    wind_direction = ((reg2_high << 8) | reg2_low) / 10.0  # 单位 度

    return wind_speed, wind_direction

# 串口初始化
ser = serial.Serial(
    port=SERIAL_PORT,
    baudrate=BAUDRATE,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
)

# Matplotlib绘图初始化
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
fig.suptitle("风速与风向实时监测")

def animate(i):
    ser.write(REQUEST_FRAME)
    response = ser.read(13)  # 固定长度应为13字节
    wind_speed, wind_direction = parse_response(response)

    if wind_speed is not None:
        current_time = datetime.now().strftime("%H:%M:%S")
        time_data.append(current_time)
        wind_speed_data.append(wind_speed)
        wind_direction_data.append(wind_direction)

        # 保持最多60个数据点
        time_data[:] = time_data[-60:]
        wind_speed_data[:] = wind_speed_data[-60:]
        wind_direction_data[:] = wind_direction_data[-60:]

        ax1.clear()
        ax2.clear()

        ax1.plot(time_data, wind_speed_data, 'b.-')
        ax2.plot(time_data, wind_direction_data, 'r.-')

        ax1.set_ylabel("风速 (m/s)")
        ax2.set_ylabel("风向 (°)")
        ax2.set_xlabel("时间")

        ax1.set_title("风速")
        ax2.set_title("风向")

        # 旋转横坐标标签避免重叠
        for ax in (ax1, ax2):
            ax.tick_params(axis='x', rotation=45)
            ax.grid(True)

ani = animation.FuncAnimation(fig, animate, interval=1000)

try:
    plt.tight_layout()
    plt.show()
except KeyboardInterrupt:
    print("程序终止")
finally:
    ser.close()
