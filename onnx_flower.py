import cv2
import datetime
import matplotlib.pyplot as plt

onnx_model_path = "yolov10s.onnx"
# onnx_model_path = "yoloV8_tiny.onnx"
input_shape = (640, 640)
net = cv2.dnn.readNetFromONNX(onnx_model_path)
model_classify = ["Kiwi flower"]
#用于后面保存文件方便记录一下系统时间
now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

# threshold指的是分数大于30%的才显示
def recognize(img, threshold=0.3):
    blob = cv2.dnn.blobFromImage(img, 1 / 255.0, input_shape, swapRB=True, crop=False)
    net.setInput(blob)

    output = net.forward()
    output = output.transpose((0, 2, 1))

    height, width, _ = img.shape
    x_factor, y_factor = width / input_shape[0], height / input_shape[1]

    boxes = []
    scores = []
    points = []

    for i in range(output[0].shape[0]):
        box = output[0][i]
        _, _, _, max_idx = cv2.minMaxLoc(box[4:])
        class_id = max_idx[1]
        score = box[4:][class_id]
        if score > threshold:
            x, y, w, h = box[0].item(), box[1].item(), box[2].item(), box[3].item()
            x = int((x - 0.5 * w) * x_factor)
            y = int((y - 0.5 * h) * y_factor)
            w = int(w * x_factor)
            h = int(h * y_factor)
            scores.append(score)
            boxes.append([x, y, w, h])

    # 进行非极大值抑制
    indexes = cv2.dnn.NMSBoxes(boxes, scores, 0.25, 0.45)
    if len(indexes) == 0:
        print("未检测到任何对象，程序将中断。")
        return []  # 返回一个空列表
    
    # 如果 NMS 有结果，继续处理
    for i in indexes.flatten():
        box = boxes[i]
        x, y, w, h = box
        points.append([x + w // 2, y + h // 2])
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        label = f'{model_classify[0]}: {scores[i]:.2f}'
        cv2.putText(img, label, (x, y + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # 显示并保存带有花朵框和类别的图像 可视化代码，可以注释
    # ***************************************************
    flower_img = img.copy()
    plt.figure(figsize=(15, 15))
    plt.imshow(cv2.cvtColor(flower_img, cv2.COLOR_BGR2RGB))
    #plt.savefig('flower.png', dpi=600) 
    plt.savefig(f"results/OX_{now}.png")
    plt.axis('on')
    plt.show()
    # ***************************************************
    return points

#在主函数中，图像是按照numpy数组的格式传入的，测试代码中需要使用cv2.imread重新将图像读入转为 NumPy 数组

def main():
    # 使用cv2.imread来读取图像文件
    img = cv2.imread('color_image.png')
    if img is not None:
        points = recognize(img, 0.3)
        print(points)
    else:
        print("图像读取失败，请检查文件路径是否正确。")


if __name__ == "__main__":
    main()
