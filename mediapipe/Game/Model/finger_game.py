import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np
from playsound import playsound


# Importing all images
imgBackground = cv2.imread(
    "../Resources/Background.png")
# print(imgBackground.shape)
imgBall = cv2.imread("../Resources/Ball.png",
                     cv2.IMREAD_UNCHANGED)
imgBat1 = cv2.imread("../Resources/bat1.png",
                     cv2.IMREAD_UNCHANGED)
imgBat2 = cv2.imread("../Resources/bat2.png",
                     cv2.IMREAD_UNCHANGED)


# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=2)



class finger_game_model:
    # Variables
    def __init__(self):
        self.ballPos = [100, 100]
        self.speedX = 15
        self.speedY = 15
        self.gameOver = False
        self.score = [0, 0]
        self.played = False
        self.imgGameOver = cv2.imread("../Resources/gameOver.png")

    def restart(self):
        self.ballPos = [100, 100]
        self.speedX = 15
        self.speedY = 15
        self.gameOver = False
        self.score = [0, 0]
        self.played = False
        self.imgGameOver = cv2.imread("../Resources/gameOver.png")

    # ballPos = [100, 100]
    # speedX = 15
    # speedY = 15
    # score = [0, 0]
    # gameOver = False
    def finger_game_process(self,image):
        img = image
        img = cv2.flip(img, 1)
        imgRaw = img.copy()

        # Find the hand and its landmarks
        hands, img = detector.findHands(img, flipType=False)  # with draw

        # Overlaying the background image
        # print(img.shape)
        # print(imgBackground.shape)
        img = cv2.addWeighted(img, 0.2, imgBackground, 0.8, 0)

        # Check for hands
        if hands:
            for hand in hands:
                x, y, w, h = hand['bbox']
                h1, w1, _ = imgBat1.shape
                y1 = y - h1 // 2
                y1 = np.clip(y1, 20, 415)

                if hand['type'] == "Left":
                    img = cvzone.overlayPNG(img, imgBat1, (59, y1))
                    if 59 < self.ballPos[0] < 59 + w1 and y1 < self.ballPos[1] < y1 + h1:
                        self.speedX = -self.speedX
                        playsound("../Resources/ball_collision.wav")
                        self.ballPos[0] += 30
                        self.score[0] += 1

                if hand['type'] == "Right":
                    img = cvzone.overlayPNG(img, imgBat2, (1195, y1))
                    if 1195 - 50 < self.ballPos[0] < 1195 and y1 < self.ballPos[1] < y1 + h1:
                        self.speedX = -self.speedX
                        playsound("../Resources/ball_collision.wav")
                        self.ballPos[0] -= 30
                        self.score[1] += 1

        # Game Over
        if self.ballPos[0] < 40 or self.ballPos[0] > 1200:
            self.gameOver = True

        if self.gameOver:
            img = self.imgGameOver
            cv2.putText(img, str(self.score[1] + self.score[0]).zfill(2), (585, 360), cv2.FONT_HERSHEY_COMPLEX,
                        2.5, (200, 0, 200), 5)
            if not self.played:
                playsound("../Resources/fail.mp3")
                self.played = True

        # If game not over move the ball
        else:

            # Move the Ball
            if self.ballPos[1] >= 500 or self.ballPos[1] <= 10:
                self.speedY = -self.speedY
                playsound("../Resources/success.wav")


            self.ballPos[0] += self.speedX
            self.ballPos[1] += self.speedY

            # Draw the ball
            img = cvzone.overlayPNG(img, imgBall, self.ballPos)

            cv2.putText(img, str(self.score[0]), (300, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
            cv2.putText(img, str(self.score[1]), (900, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)

        img[580:700, 20:233] = cv2.resize(imgRaw, (213, 120))
        # key = cv2.waitKey(1)
        # if key == ord('r'):
        #     self.ballPos = [100, 100]
        #     self.speedX = 15
        #     self.speedY = 15
        #     self.gameOver = False
        #     self.score = [0, 0]

        return img



