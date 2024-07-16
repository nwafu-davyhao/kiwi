import os
import subprocess
import time
import rtde_control
import rtde_receive
import math
import rtde_io

#初始化 RTDE 控制和接收接口
robot_ip = "192.168.56.10"
rtde_c = rtde_control.RTDEControlInterface(robot_ip)
rtde_r = rtde_receive.RTDEReceiveInterface(robot_ip)
rtde_io_ = rtde_io.RTDEIOInterface(robot_ip)
# 设置速度和加速度
speed = 0.5  # 工具速度，单位：米/秒  极限3.14
acceleration = 0.3  # 工具加速度，单位：米/秒²   极限40

# 转换角度为弧度
def degrees_to_radians(degrees):
    return [math.radians(d) for d in degrees]

# 转换毫米为米
def mm_to_millimeters(mm):
    return [m / 1000.0 for m in mm]


#****************************机械臂笛卡尔坐标移动函数******************************#
def move_robot_to_position_cartesian(tcp_pose):

    # 提取并转换坐标为米
    x, y, z, roll, pitch, yaw = tcp_pose

    x, y, z = mm_to_millimeters([x, y, z])
    # 提取并转换旋转角度为弧度
    rx, ry, rz = degrees_to_radians([roll, pitch, yaw])

    tcp_pose = [x, y, z, rx, ry, rz]
    # 发送TCP移动命令，使用moveJ进行关节空间运动
    rtde_c.moveJ_IK(tcp_pose, speed, acceleration)

#****************************机械臂角度移动函数************************************#

def move_robot_to_position_angel(joint_angles_degrees):
    joint_angles_radians = [math.radians(angle) for angle in joint_angles_degrees]
    rtde_c.moveJ(joint_angles_radians, speed, acceleration)

#****************************机械臂位置检测函数***********************************#
def detecting_location():

    tcp_pose = rtde_r.getActualTCPPose()

    x, y = tcp_pose[0], tcp_pose[1]

    # 根据 x 和 y 的正负判断机械臂所在的象限
    if x >= 0 and y >= 0:
        tcp = 0  # 第一象限
    elif x < 0 and y >= 0:
        tcp = 1  # 第二象限
    elif x < 0 and y < 0:
        tcp = 2  # 第三象限
    elif x >= 0 and y < 0:
        tcp = 3  # 第四象限

     # 打印机械臂所在的象限编号
    print("机械臂当前位于第 {} 象限".format(tcp+1))
    return tcp

#****************************机械臂授粉通信程序***********************************#

def pollination_signal():
    # rtde_io.setStandardDigitalOut(7, True) # 将引脚设置为高电平
    rtde_io_.setStandardDigitalOut(7, True)
    time.sleep(0.1)
    rtde_io_.setStandardDigitalOut(7, False) # 将引脚设置为高电平
    time.sleep(0.1)

#*************************************************测试代码
def main():
   pollination_signal()
if __name__ == "__main__":
    main()