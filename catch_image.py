import pyrealsense2 as rs
import numpy as np
import cv2
import time

def capture_and_save():
    # 配置 RealSense 管道
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)  
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
# **********************************************************************************888
    # # 开启设备并获取设备列表
    # pipeline_profile = pipeline.start(config)

    # # 获取设备
    # device = pipeline_profile.get_device()

    # # 获取设备高级模式设置
    # advanced_mode = device.as_advanced_mode()

    # # 设置激光投射器功率为 0 来关闭它
    # # 注意：激光投射器的选项可能因相机型号而异，这里使用的是 "r200.laser_power" 作为示例
    # if advanced_mode.is_option_supported("r200.laser_power"):
    #     laser_power_option = advanced_mode.get_option(rs.option.r200_laser_power)
    #     advanced_mode.set_option(rs.option.r200_laser_power, 0)
# **********************************************************************************888
    # 启动管道
    pipeline.start(config)

    # 获取相机内参
    profile = pipeline.get_active_profile()
    depth_intrinsics = profile.get_stream(rs.stream.depth).as_video_stream_profile().get_intrinsics()

    # 对齐对象
    align_to = rs.stream.color
    align = rs.align(align_to)
    # 等待1秒
    time.sleep(2)

    try:
        while True:  
            # 获取帧
            frames = pipeline.wait_for_frames()

            # 对齐帧
            aligned_frames = align.process(frames)

            # 获取对齐后的深度和彩色图像
            depth_frame = aligned_frames.get_depth_frame()
            color_frame = aligned_frames.get_color_frame()

            if depth_frame and color_frame:
                # 将图像转换为 numpy 数组
                depth_image = np.asarray(depth_frame.get_data(), dtype=np.float32)
                color_image = np.asanyarray(color_frame.get_data())
                depth_image_unit16 = depth_image.astype(np.uint16)

                # 应用伪彩色到深度图像
                depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_HOT)

                # 创建窗口显示图像
                cv2.namedWindow('Color Image', cv2.WINDOW_AUTOSIZE)
                cv2.namedWindow('Aligned Depth Image', cv2.WINDOW_AUTOSIZE)

                # 显示图像
                cv2.imshow('Color Image', color_image)
                cv2.imshow('Aligned Depth Image', depth_colormap)

                # ********************************不要按键，直接保存********************************************
                # # 保存图像
                # cv2.imwrite('color_image.png', color_image)
                # cv2.imwrite('depth_image_16bit.png', depth_image_unit16)  # 保存 16 位深度图
                # # 断开相机数据流
                # pipeline.stop()
                # # 退出循环
                # break
                
                # **********************************要按S键，再保存******************************************
                # 等待按键操作
                key = cv2.waitKey(1)
                if key & 0xFF == ord('s'):
                    # 保存图像
                    cv2.imwrite('color_image.png', color_image)
                    cv2.imwrite('depth_image_16bit.png', depth_image_unit16)  # 保存 16 位深度图
                    
                    # 断开相机数据流
                    pipeline.stop()
                    # 传回两张图片
                    return color_image, depth_image, depth_intrinsics
                    # 退出循环
                    break
                elif key & 0xFF == ord('q') or key == 27:
                    cv2.destroyAllWindows()
                    break
    finally:
        # 销毁所有窗口
        cv2.destroyAllWindows()

# def main():
#     color_image, depth_image_unit16, depth_frame = capture_and_save()

# if __name__ == "__main__":
#     main()