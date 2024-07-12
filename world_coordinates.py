import pyrealsense2 as rs
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def convert_points_to_world_coordinates(points, depth_frame, intrinsics):
    # 确保 points 是一个 NumPy 数组
    points = np.array(points, dtype=int)  # 确保 points 是整数数组
    # 计算深度值
    depth_values = depth_frame[points[:, 1], points[:, 0]]

    # 将深度值转换为世界坐标
    z = depth_values
    x = (points[:, 0] - intrinsics.ppx) * z / intrinsics.fx
    y = (points[:, 1] - intrinsics.ppy) * z / intrinsics.fy

    world_points = np.vstack((x, y, z)).T

    # # 创建一个新的图和一个三维子图
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')

    # # 绘制散点图，传入 world_points 中的 x, y, z 坐标
    # ax.scatter(world_points[:, 0], world_points[:, 1], world_points[:, 2], color='b')

    # # 标记三维坐标点的数值以及对应的二维坐标数值
    # for i, (x, y, z) in enumerate(zip(world_points[:, 0], world_points[:, 1], world_points[:, 2])):
    #     ax.text(x, y, z, f'3D: ({x:.2f}, {y:.2f}, {z:.2f})\n2D: ({points[i][0]:.0f}, {points[i][1]:.0f})', 
    #             color='black', fontsize=9, zorder=1)

    # # 设置图表标题和坐标轴标签
    # ax.set_title("3D World Coordinates with Labels")
    # ax.set_xlabel("X Coordinate")
    # ax.set_ylabel("Y Coordinate")
    # ax.set_zlabel("Z Coordinate")

    # # 设置坐标轴范围，确保所有标记都在视图中
    # ax.set_xlim(ax.get_xlim()[0], np.max(world_points[:, 0]))
    # ax.set_ylim(ax.get_ylim()[0], np.max(world_points[:, 1]))
    # ax.set_zlim(ax.get_zlim()[0], np.max(world_points[:, 2]))

    # # 显示图表
    # plt.show()
    # plt.savefig('3d_with_labels.png', dpi=600)

    return world_points

# 其他代码...










# import pyrealsense2 as rs
# import numpy as np

# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

# def convert_points_to_world_coordinates(points, depth_frame, intrinsics):
#     # 确保 points 是一个 NumPy 数组
#     points = np.array(points)
#     # 计算深度值
#     depth_values = depth_frame[points[:, 1], points[:, 0]]

#     # 将深度值转换为世界坐标
#     z = depth_values
#     x = (points[:, 0] - intrinsics.ppx) * z / intrinsics.fx
#     y = (points[:, 1] - intrinsics.ppy) * z / intrinsics.fy

#     world_points = np.vstack((x, y, z)).T

    



#     # 创建一个新的图和一个三维子图
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')

#     # 绘制散点图，传入 world_points 中的 x, y, z 坐标
#     ax.scatter(world_points[:, 0], world_points[:, 1], world_points[:, 2])

#     # 设置图表标题和坐标轴标签
#     ax.set_title("3D World Coordinates")
#     ax.set_xlabel("X Coordinate")
#     ax.set_ylabel("Y Coordinate")
#     ax.set_zlabel("Z Coordinate")

#     # 显示图表
#     plt.show()
#     plt.savefig('3d.png', dpi=600)

#     return world_points