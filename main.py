
import numpy as np

from move import move_robot_to_position
from catch_image import capture_and_save
from onnx_flower import recognize
from world_coordinates import convert_points_to_world_coordinates
from check_quadrant import check_quadrant,filter_coordinates_within_workspace
from greedy_path import greedy_path_planning, visualize_path

#定义机器人的一些全局变量
Xaxis_offset=0.4
Yaxis_offset=0.4
Zaxis_offset=0

Roll_offset=0
Pitch_offset=0
Yaw_offset=0

def main():
    # 移动到初始化位置
    # 定义四个象限的初始化位置
    quadrants = [
        [Xaxis_offset, Yaxis_offset, Zaxis_offset, Roll_offset, Pitch_offset, Yaw_offset]  # 第1象限
        # [-Xaxis_offset, Yaxis_offset, Zaxis_offset, Roll_offset, Pitch_offset, Yaw_offset]  # 第2象限
        # [-Xaxis_offset, -Yaxis_offset, Zaxis_offset, Roll_offset, Pitch_offset, Yaw_offset]  # 第3象限
        # [Xaxis_offset, -Yaxis_offset, Zaxis_offset, Roll_offset, Pitch_offset, Yaw_offset]  # 第4象限
    ]
    
    # 遍历四个象限并移动机械臂
    for idx, tcp_pose in enumerate(quadrants, start=1):    
        # x, y, z, roll, pitch, yaw = tcp_pose
        move_robot_to_position(tcp_pose)
        print(f"移动到第{idx}象限: {tcp_pose}")
        # time.sleep(1)  # 等待机械臂移动完成，具体时间可根据实际情况调整  


        # 第一步：启动相机拍摄GRB和Depth照片，Depth图像对齐到GRB图像，保存在对应的文件夹    
        color_img_path, depth_image, depth_intrinsics = capture_and_save()

        # 第二步：读取onnx文件，识别GRB照片花朵位置
        points = recognize(color_img_path, 0.3)
        print("图像坐标：", points)

        # 第三步：花朵位置转换为世界坐标
        world_coordinates = convert_points_to_world_coordinates(points, depth_image, depth_intrinsics)
        print("世界坐标：", world_coordinates)

        # 第四步：筛选对应象限坐标，并过滤异值点，转换为机械臂坐标
        quadrant_coords = check_quadrant(world_coordinates, idx, quadrants)
        filtered_quadrant_coords = filter_coordinates_within_workspace(quadrant_coords)
        print("过滤机械臂坐标：", filtered_quadrant_coords)

        # 第五步：路径规划
        planned_path = greedy_path_planning(filtered_quadrant_coords)
        print("规划的路径:", planned_path)
        # 调用可视化函数
        visualize_path(planned_path)

        # 第六步：机械臂移动
        # 提取 quadrants 数组的后三个值
        additional_columns = quadrants[:, 3:]  # 取后三个值

        # 将 additional_columns 重复以匹配 planned_path 的行数
        additional_columns_repeated = additional_columns.repeat(planned_path.shape[0], axis=0)

        # 将 additional_columns_repeated 追加到 planned_path 的每一行
        extended_coords = np.hstack((planned_path, additional_columns_repeated))  

        # 遍历 extended_coords 中的每一行
        for row in extended_coords:
            # 将行中的值赋给对应的变量
            x, y, z, roll, pitch, yaw = row
            move_robot_to_position(x, y, z, roll, pitch, yaw)

        #第七步：机械臂最终状态
        




if __name__ == "__main__":
    main()
