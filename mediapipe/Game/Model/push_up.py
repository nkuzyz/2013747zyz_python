import cv2
import mediapipe as mp
import numpy as np
import Game.Util.PoseModule as pm
from playsound import playsound


class push_up_model:
    def __init__(self):
        self.detector = pm.poseDetector()
        self.count = 0
        self.direction = 0
        self.form = 0
        self.feedback = "Fix Form"

    def push_up_process(self, img):
        # ret, img = cap.read()  # 1280.0 720.0
        # Determine dimensions of video - Help with creation of box in Line 43
        # width = cap.get(3)  # float `width`
        # height = cap.get(4)  # float `height`
        # print(width, height) 1280.0 720.0

        img = self.detector.findPose(img, False)
        lmList = self.detector.findPosition(img, False)
        # print(lmList)
        if len(lmList) != 0:
            # 11：left shoulder
            # 13: left elbow
            # 15: left wrist
            # 23: left hip
            # 25: left knee
            elbow = self.detector.findAngle(img, 11, 13, 15)
            shoulder = self.detector.findAngle(img, 13, 11, 23)
            hip = self.detector.findAngle(img, 11, 23, 25)

            # Percentage of success of pushup
            per = np.interp(elbow, (90, 160), (0, 100))

            # Bar to show Pushup progress
            bar = np.interp(elbow, (90, 160), (380, 50))

            # Check to ensure right self.form before starting the program
            if elbow > 160 and shoulder > 40 and hip > 160:
                self.form = 1

            # Check for full range of motion for the pushup
            if self.form == 1:
                if per == 0:
                    if elbow <= 95 and hip > 150:
                        self.feedback = "Turn Up"
                        if self.direction == 0:
                            self.count += 0.5
                            playsound("../Resources/success.wav")
                            self.direction = 1
                    else:
                        self.feedback = "Fix Form"

                if per == 100:
                    if elbow > 150 and shoulder > 40 and hip > 150:
                        self.feedback = "Turn Down"
                        if self.direction == 1:
                            self.count += 0.5
                            playsound("../Resources/success2.wav")
                            self.direction = 0
                    else:
                        self.feedback = "Fix Form"
                        # self.form = 0

            # print(self.count)

            # Draw Bar
            if self.form == 1:
                cv2.rectangle(img, (1160, 50), (1180, 380), (97, 100, 159), 3)
                cv2.rectangle(img, (1160, int(bar)), (1180, 380), (97, 100, 159), cv2.FILLED)
                cv2.putText(img, f'{int(per)}%', (1145, 430), cv2.FONT_HERSHEY_PLAIN, 2,
                            (43, 51, 62), 2)

            # Pushup counter
            cv2.rectangle(img, (0, 0), (150, 75), (255, 255, 255), cv2.FILLED)
            cv2.putText(img, str(int(self.count)), (25, 65), cv2.FONT_HERSHEY_PLAIN, 5,
                        (43, 51, 62), 5)

            # Feedback
            cv2.rectangle(img, (1100, 0), (1250, 50), (255, 255, 255), cv2.FILLED)
            cv2.putText(img, self.feedback, (1100, 40), cv2.FONT_HERSHEY_PLAIN, 2,
                        (77, 16, 24), 2)

        return img
