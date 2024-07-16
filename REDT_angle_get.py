import rtde_receive
import time
import pandas as pd
import math

# UR5机器人的IP地址
ROBOT_IP = "192.168.56.10"

# 初始化 RTDE 接收接口
rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP)

# 创建一个空的DataFrame来存储数据
columns = ["Base (deg)", "Shoulder (deg)", "Elbow (deg)", "Wrist1 (deg)", "Wrist2 (deg)", "Wrist3 (deg)"]
data = pd.DataFrame(columns=columns)

try:
    while True:
        # 获取当前关节角度（以弧度为单位）
        joint_angles_rad = rtde_r.getActualQ()
        print("当前关节角度（弧度）:", joint_angles_rad)

        # 将关节角度从弧度转换为角度
        joint_angles_deg = [math.degrees(angle) for angle in joint_angles_rad]
        print("当前关节角度（角度）:", joint_angles_deg)

        # 将关节角度格式化为小数点后一位
        formatted_angles = [round(angle, 1) for angle in joint_angles_deg]

        # 将数据添加到DataFrame
        new_row = pd.DataFrame([formatted_angles], columns=columns)
        data = pd.concat([data, new_row], ignore_index=True)

        # 暂停一秒 
        time.sleep(1)
except KeyboardInterrupt:
    # 当用户按下Ctrl+C时，保存数据到CSV文件
    data.to_csv("joint_angles_data.csv", index=False)
    print("数据已保存到 joint_angles_data.csv")