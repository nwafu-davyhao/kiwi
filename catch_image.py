import pyrealsense2 as rs
import numpy as np
import cv2
import time
import datetime

def capture_and_save():
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    # 配置 RealSense 管道
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)  
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
    # 启动管道
    pipeline.start(config)
    # 获取相机内参
    profile = pipeline.get_active_profile()
    depth_intrinsics = profile.get_stream(rs.stream.depth).as_video_stream_profile().get_intrinsics()
    # 对齐对象
    align_to = rs.stream.color
    align = rs.align(align_to)
    # 等待n秒
    time.sleep(2)
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
        depth_image_unit16 = depth_image.astype(np.uint16) #把深度图像存储为16位，方便后续处理
        cv2.imwrite('color_image.png', color_image)
        cv2.imwrite(f"results/CL_{now}.png",color_image)
        cv2.imwrite('depth_image.png', depth_image_unit16)  # 保存 16 位深度图
        cv2.imwrite(f"results/DP_{now}.png", depth_image_unit16)  # 保存 16 位深度图
        # 断开相机数据流
        pipeline.stop()
         #传回两张图片和相机内参
        return color_image, depth_image, depth_intrinsics
   
# ***********************函数测试代码*********************

# def main():
#     capture_and_save()

# if __name__ == "__main__":
#     main()

# ********************可视化测试代码**********************
def main():
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)  
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

    try:
        pipeline.start(config) 
        align_to = rs.stream.color
        align = rs.align(align_to)
        
        while True:
            frames = pipeline.wait_for_frames()
            aligned_frames = align.process(frames)
            
            depth_frame = aligned_frames.get_depth_frame()
            color_frame = aligned_frames.get_color_frame()
            
            if depth_frame and color_frame:
                # 将图像转换为 numpy 数组
                depth_image = np.asarray(depth_frame.get_data(), dtype=np.float32)
                color_image = np.asanyarray(color_frame.get_data())
                
                # 应用伪彩色到深度图像
                depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.	COLORMAP_VIRIDIS )
               
                # 创建窗口显示图像
                cv2.namedWindow('Color Image', cv2.WINDOW_AUTOSIZE)
                cv2.namedWindow('Aligned Depth Image', cv2.WINDOW_AUTOSIZE)
                
                # 显示图像
                cv2.imshow('Color Image', color_image)
                cv2.imshow('Aligned Depth Image', depth_colormap)
                
                # 等待按键操作
                key = cv2.waitKey(1)
                if key & 0xFF == ord('s'):
                    # 保存图像
                    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                    cv2.imwrite('color_image.png', color_image)
                    cv2.imwrite(f"results/CL_{now}.png",color_image)
                    depth_image_unit16 = depth_image.astype(np.uint16) #保存前转16位可以提高一下可视化质量
                    cv2.imwrite('depth_image.png', depth_image_unit16)  # 保存 16 位深度图
                    cv2.imwrite(f"results/DP_{now}.png", depth_image_unit16)  # 保存 16 位深度图
                    print("Images saved.")
                    cv2.destroyAllWindows()
                    break

                elif key & 0xFF == ord('q') or key == 27:
                    cv2.destroyAllWindows()
                    pipeline.stop()
                    break
                
    except Exception as e:
        print(f"An error occurred: {e}")
        pipeline.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
