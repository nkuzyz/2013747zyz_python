from Game.Util.pose_util import FullBodyPoseEmbedder
from Game.Util.pose_util import PoseClassificationVisualizer
from Game.Util.pose_util import EMADictSmoothing
from Game.Util.pose_util import RepetitionCounter
from Game.Util.pose_util import PoseClassifier
from mediapipe.python.solutions import pose as mp_pose
import os
import numpy as np
from matplotlib import pyplot as plt
# import tqdm

from mediapipe.python.solutions import drawing_utils as mp_drawing

import cv2

video_cap = cv2.VideoCapture(1)
class_name = 'down'

# Get some video parameters to generate output video with classificaiton.
# 使用get()获取视频帧数(opencv3以上版本)
video_n_frames = video_cap.get(cv2.CAP_PROP_FRAME_COUNT)
# video_fps = video_cap.get(cv2.CAP_PROP_FPS)
video_width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
video_height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Initilize tracker, classifier and counter.
# Do that before every video as all of them have state.

# Folder with pose class CSVs. That should be the same folder you using while
# building classifier to output CSVs.
pose_samples_folder = 'squat_csvs_out'

# Initialize tracker.
pose_tracker = mp_pose.Pose()

# Initialize embedder.
# 人体姿态编码
pose_embedder = FullBodyPoseEmbedder()

# Initialize classifier.
# Ceck that you are using the same parameters as during bootstrapping.
# 人体姿态分类
pose_classifier = PoseClassifier(
    pose_samples_folder=pose_samples_folder,
    pose_embedder=pose_embedder,
    top_n_by_max_distance=30,
    top_n_by_mean_distance=10)

# # Uncomment to validate target poses used by classifier and find outliers.
# outliers = pose_classifier.find_pose_sample_outliers()
# print('Number of pose sample outliers (consider removing them): ', len(outliers))

# Initialize EMA smoothing.
# 姿态分类结果平滑
pose_classification_filter = EMADictSmoothing(
    window_size=10,
    alpha=0.2)

# 指定动作的两个阈值
# 动作计数器
repetition_counter = RepetitionCounter(
    class_name=class_name,
    enter_threshold=6,
    exit_threshold=4)

# Initialize renderer.
# 可视化模块
pose_classification_visualizer = PoseClassificationVisualizer(
    class_name=class_name,
    plot_x_max=400,
    # Graphic looks nicer if it's the same as `top_n_by_mean_distance`.
    plot_y_max=10)

output_frame = None
while True:
    # Get next frame of the video.
    success, input_frame = video_cap.read()
    if not success:
        break

    # Run pose tracker.
    input_frame = cv2.cvtColor(input_frame, cv2.COLOR_BGR2RGB)
    result = pose_tracker.process(image=input_frame)
    pose_landmarks = result.pose_landmarks

    # Draw pose prediction.
    output_frame = input_frame.copy()
    if pose_landmarks is not None:
        mp_drawing.draw_landmarks(
            image=output_frame,
            landmark_list=pose_landmarks,
            connections=mp_pose.POSE_CONNECTIONS)

    if pose_landmarks is not None:
        # Get landmarks.
        frame_height, frame_width = output_frame.shape[0], output_frame.shape[1]
        pose_landmarks = np.array([[lmk.x * frame_width, lmk.y * frame_height, lmk.z * frame_width]
                                   for lmk in pose_landmarks.landmark], dtype=np.float32)
        assert pose_landmarks.shape == (33, 3), 'Unexpected landmarks shape: {}'.format(pose_landmarks.shape)

        # Classify the pose on the current frame.
        pose_classification = pose_classifier(pose_landmarks)

        # Smooth classification using EMA.
        pose_classification_filtered = pose_classification_filter(pose_classification)

        # Count repetitions.
        repetitions_count = repetition_counter(pose_classification_filtered)
    else:
        # No pose => no classification on current frame.
        pose_classification = None

        # Still add empty classification to the filter to maintaing correct
        # smoothing for future frames.
        pose_classification_filtered = pose_classification_filter(dict())
        pose_classification_filtered = None

        # Don't update the counter presuming that person is 'frozen'. Just
        # take the latest repetitions count.
        repetitions_count = repetition_counter.n_repeats

    # Draw classification plot and repetition counter.
    output_frame = pose_classification_visualizer(
        frame=output_frame,
        pose_classification=pose_classification,
        pose_classification_filtered=pose_classification_filtered,
        repetitions_count=repetitions_count)

    # Save the output frame.
    output_frame = cv2.cvtColor(np.array(output_frame), cv2.COLOR_RGB2BGR)
    cv2.imshow("Image", output_frame)
    key = cv2.waitKey(1)






# Release MediaPipe resources.
pose_tracker.close()

