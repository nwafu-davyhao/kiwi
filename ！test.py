import numpy as np
######

def check_quadrant(world_coordinates, idx, quadrants):
    # 应用偏移量#### 
    offset_x = quadrants[0] * 1000
    offset_y = quadrants[1] * 1000
    offset_z = quadrants[2] * 1000
    world_coordinates[:, 0] += offset_x
    world_coordinates[:, 1] += offset_y
    world_coordinates[:, 2] += offset_z

    # 定义象限的范围
    quadrant1 = np.logical_and(world_coordinates[:, 0] > 0, np.logical_and(world_coordinates[:, 1] > 0, world_coordinates[:, 2] > 0))
    quadrant2 = np.logical_and(world_coordinates[:, 0] < 0, np.logical_and(world_coordinates[:, 1] > 0, world_coordinates[:, 2] > 0))
    quadrant3 = np.logical_and(world_coordinates[:, 0] < 0, np.logical_and(world_coordinates[:, 1] < 0, world_coordinates[:, 2] > 0))
    quadrant4 = np.logical_and(world_coordinates[:, 0] > 0, np.logical_and(world_coordinates[:, 1] < 0, world_coordinates[:, 2] > 0))

    # 不在任何象限的提示
    not_in_any_quadrant = np.logical_not(np.logical_or(np.logical_or(quadrant1, quadrant2), np.logical_or(quadrant3, quadrant4)))
    if np.any(not_in_any_quadrant):
        print("存在不在任何象限的坐标")

    # 过滤出在对应象限的坐标
    quadrant1_coords = world_coordinates[quadrant1]
    quadrant2_coords = world_coordinates[quadrant2]
    quadrant3_coords = world_coordinates[quadrant3]
    quadrant4_coords = world_coordinates[quadrant4]
    print("第一象限坐标：", quadrant1_coords)
    print("第二象限坐标：", quadrant2_coords)
    print("第三象限坐标：", quadrant3_coords)
    print("第四象限坐标：", quadrant4_coords)

    # 返回指定象限的坐标
    if idx == 1:
        return quadrant1_coords
    elif idx == 2:
        return quadrant2_coords
    elif idx == 3:
        return quadrant3_coords
    elif idx == 4:
        return quadrant4_coords
    else:
        print("无效的象限索引，请输入 1 到 4 之间的整数。")
        return None

# asivy7_push