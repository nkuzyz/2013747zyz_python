# 导入opencv工具包
import cv2
# 导入numpy
import numpy as np
# 导入姿势识别器
from poseutil import PoseDetector

# 打开视频文件
cap = cv2.VideoCapture(1)
# 姿势识别器
detector = PoseDetector()

# 方向与个数
dir = 0  # 0为躺下，1为坐起
count = 0

while True:
    # 读取摄像头，img为每帧图片
    success, img = cap.read()
    if success:
        h, w, c = img.shape
        # 识别姿势
        img = detector.find_pose(img, draw=True)
        # 获取姿势数据
        positions = detector.find_positions(img)

        if positions:
            # 获取仰卧起坐的角度
            angle = detector.find_angle(img, 11, 23, 25)
            # 进度条长度
            bar = np.interp(angle, (50, 130), (w // 2 - 100, w // 2 + 100))
            cv2.rectangle(img, (w // 2 - 100, h - 150), (int(bar), h - 100), (0, 255, 0), cv2.FILLED)
            # 角度小于55度认为坐起
            if angle <= 55:
                if dir == 0:
                    count = count + 0.5
                    dir = 1
            # 角度大于120度认为躺下
            if angle >= 120:
                if dir == 1:
                    count = count + 0.5
                    dir = 0
            cv2.putText(img, str(int(count)), (w // 2, h // 2), cv2.FONT_HERSHEY_SIMPLEX, 10, (255, 255, 255), 20, cv2.LINE_AA)

        # 打开一个Image窗口显示视频图片
        cv2.imshow('Image', img)

    else:
        # 视频结束退出
        break

    # 如果按下q键，程序退出
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# 关闭摄像头
cap.release()
# 关闭程序窗口
cv2.destroyAllWindows()