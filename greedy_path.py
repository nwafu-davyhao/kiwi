import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 贪心算法规划路径
def greedy_path_planning(points):
    # 初始化路径，包含起始点
    path = [points[0].tolist()]  # 使用 tolist() 转换为列表
    # 剩余点集合，移除起始点
    remaining_points = points[1:]
    
    while len(remaining_points) > 0:
        # 计算当前点到所有剩余点的距离
        distances = np.linalg.norm(remaining_points - path[-1], axis=1)
        # 找到最近的点的索引
        nearest_index = np.argmin(distances)
        # 将最近的点添加到路径中
        path.append(remaining_points[nearest_index].tolist())
        # 从剩余点集合中移除已经选择的点
        remaining_points = np.delete(remaining_points, nearest_index, axis=0)
    
    return path

# # 假设 filtered_quadrant_coords 是一个包含三维坐标点的 NumPy 数组
# filtered_quadrant_coords = np.array([
#     [131.75875928, 761.0520078, 759.3],
#     [353.00760577, 770.91875541, 830.3],
#     [370.52463912, 723.75751177, 830.3]
# ])

# # 这是提供的 quadrants 数组
# quadrants = np.array([
#     [0.4, 0.4, 0.2, 0, 0, 1.57]
# ])

# # 这是提供的 filtered_quadrant_coords 数组
# filtered_quadrant_coords = np.array([
#     [131.75875928, 761.0520078, 759.3],
#     [353.00760577, 770.91875541, 830.3],
#     [370.52463912, 723.75751177, 830.3]
# ])

# # 提取 quadrants 数组的后三个值
# additional_columns = quadrants[:, 3:]  # 取后三个值

# # 将 additional_columns 重复以匹配 filtered_quadrant_coords 的行数
# additional_columns_repeated = additional_columns.repeat(filtered_quadrant_coords.shape[0], axis=0)

# # 将 additional_columns_repeated 追加到 filtered_quadrant_coords 的每一行
# extended_coords = np.hstack((filtered_quadrant_coords, additional_columns_repeated))

# # 打印结果
# print(extended_coords)



def visualize_path(path):
    # 创建一个新的图和三维子图
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # 提取路径中的 x, y, z 坐标
    x_coords, y_coords, z_coords = zip(*path)

    # 绘制路径点
    ax.scatter(x_coords, y_coords, z_coords, c='r', marker='o')

    # 绘制连接路径的线
    ax.plot(x_coords, y_coords, z_coords, c='b')

    # 标记每个点的索引（顺序）
    for i, (x, y, z) in enumerate(zip(x_coords, y_coords, z_coords)):
        ax.text(x, y, z, f' {i}', color='black', fontsize=9)

    # 设置坐标轴标签
    ax.set_xlabel('X coordinate')
    ax.set_ylabel('Y coordinate')
    ax.set_zlabel('Z coordinate')

    # 设置坐标轴范围与点的范围一致，以便更好地展示
    ax.set_xlim(min(x_coords), max(x_coords))
    ax.set_ylim(min(y_coords), max(y_coords))
    ax.set_zlim(min(z_coords), max(z_coords))

    # 显示图形
    plt.show()
    plt.savefig('3d_greedy_path_planning.png', dpi=600)

# 调用可视化函数
# visualize_path(planned_path)