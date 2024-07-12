import os
import subprocess
import time
import rtde_control
import rtde_receive
import math

# 初始化RTDE控制接口，替换成你的机器人IP地址
robot_ip = "192.168.56.10"
rtde_c = rtde_control.RTDEControlInterface(robot_ip)
# 初始化 RTDE 控制和接收接口
# rtde_c = rtde_control.RTDEControlInterface(robot_ip)
rtde_r = rtde_receive.RTDEReceiveInterface(robot_ip)
# 设置速度和加速度
speed = 0.5  # 工具速度，单位：米/秒  极限3.14
acceleration = 0.3  # 工具加速度，单位：米/秒²   极限40

# 转换角度为弧度
def degrees_to_radians(degrees):
    return [math.radians(d) for d in degrees]

# 转换毫米为米
def mm_to_millimeters(mm):
    return [m / 1000.0 for m in mm]

def move_robot_to_position(x, y, z, roll, pitch, yaw):
    # 这里实现机械臂移动的代码
    # 提取并转换坐标为米
    x, y, z = mm_to_millimeters([x, y, z])

    # 提取并转换旋转角度为弧度
    rx, ry, rz = degrees_to_radians([roll, pitch, yaw])

    tcp_pose = [x, y, z, rx, ry, rz]
    # 发送TCP移动命令，使用moveJ进行关节空间运动
    rtde_c.moveJ_IK(tcp_pose, speed, acceleration)
