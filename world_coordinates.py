import pyrealsense2 as rs
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# 喷头补偿量
pollination_distance = 100
def convert_points_to_world_coordinates(points, depth_frame, intrinsics):
    # 确保 points 是一个 NumPy 数组
    points = np.array(points, dtype=int)  # 确保 points 是整数数组
    if points.size > 0:
        # 计算深度值
        depth_values = depth_frame[points[:, 1], points[:, 0]]
    
        # 将深度值转换为世界坐标
        z = depth_values - pollination_distance
        x = (points[:, 0] - intrinsics.ppx) * z / intrinsics.fx
        y = (points[:, 1] - intrinsics.ppy) * z / intrinsics.fy
        world_points = np.vstack((x, y, z)).T
        return world_points
    else:
        # 处理 points 为空的情况，例如：
        print("未检测到点，无法进行转换操作")
        # 或者返回一个默认值或执行其他适当的逻辑

