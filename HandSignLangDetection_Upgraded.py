import cv2
import mediapipe as mp
import pyttsx3

engine = pyttsx3.init()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

finger_tips = [8, 12, 16, 20]
thumb_tip = 4

like_img = cv2.imread("images/like.png")
#like_img = cv2.resize(like_img, (200, 180))

dislike_img = cv2.imread("images/dislike.png")
#dislike_img = cv2.resize(dislike_img, (200, 180))
engine.say("Welcome to Terabyte Studio")
engine.say("Program and Enjoy")
engine.runAndWait()

while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    h, w, c = img.shape
    results = hands.process(img)

    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            lm_list = []
            for id, lm in enumerate(hand_landmark.landmark):
                lm_list.append(lm)
            finger_fold_status = []
            for tip in finger_tips:
                x, y = int(lm_list[tip].x * w), int(lm_list[tip].y * h)
                #print(id, ":", x, y)
                #cv2.circle(img, (x, y), 15, (220, 20, 6), cv2.FILLED)

                if lm_list[tip].x < lm_list[tip - 2].x:
                    #cv2.circle(img, (x, y), 15, (220, 20, 6), cv2.FILLED)
                    finger_fold_status.append(True)
                else:
                    finger_fold_status.append(False)

            print(finger_fold_status)

            x, y = int(lm_list[8].x * w), int(lm_list[8].y * h)
            print(x, y)

            # stop
            if lm_list[4].y < lm_list[2].y and lm_list[8].y < lm_list[6].y and lm_list[12].y < lm_list[10].y and \
                    lm_list[16].y < lm_list[14].y and lm_list[20].y < lm_list[18].y and lm_list[17].x < lm_list[0].x < \
                    lm_list[5].x:
                cv2.putText(img, "HII THERE ", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (225, 215, 0), 3)
                engine.say("Hii There")
                engine.runAndWait()
                print("HII There")
                

            # Forward
            if lm_list[3].x > lm_list[4].x and lm_list[8].y < lm_list[6].y and lm_list[12].y > lm_list[10].y and \
                    lm_list[16].y > lm_list[14].y and lm_list[20].y > lm_list[18].y:
                cv2.putText(img, "THANK YOU", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (214, 252, 0), 3)
                engine.say("Thank you")
                engine.runAndWait()
                print("Thank YOU")

            # Backward
            if lm_list[3].x > lm_list[4].x and lm_list[3].y < lm_list[4].y and lm_list[8].y > lm_list[6].y and lm_list[12].y < lm_list[10].y and \
                    lm_list[16].y < lm_list[14].y and lm_list[20].y < lm_list[18].y:
                cv2.putText(img, "I'M HUNGRY", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 250, 154), 3)
                engine.say("I'm Hungry")
                engine.runAndWait()
                print("I'M HUNGRY")

            # Left
            if lm_list[1].y < lm_list[2].y and lm_list[8].x < lm_list[6].x and lm_list[12].x > lm_list[10].x and \
                    lm_list[16].x > lm_list[14].x and lm_list[20].x > lm_list[18].x and lm_list[5].x < lm_list[0].x:
                cv2.putText(img, "I WANT WATER", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 225, 127), 3)
                engine.say("I want water")
                engine.runAndWait()
                print("I WANT WATER")

            # Right
            if lm_list[4].y < lm_list[2].y and lm_list[8].x > lm_list[6].x and lm_list[12].x < lm_list[10].x and \
                    lm_list[16].x < lm_list[14].x and lm_list[20].x < lm_list[18].x:
                cv2.putText(img, "NOO", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (138, 43, 226), 3)
                engine.say("No")
                engine.runAndWait()
                print("NOO")


            if all(finger_fold_status):
                # like
                if lm_list[thumb_tip].y < lm_list[thumb_tip - 1].y < lm_list[thumb_tip - 2].y and lm_list[0].x < lm_list[3].y:
                    print("OK")
                    cv2.putText(img, "OK", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 225), 3)
                    engine.say("Ok")
                    engine.runAndWait()
                    # h, w, c = like_img.shape
                    # img[35:h + 35, 30:w + 30] = like_img
                # Dislike
                if lm_list[thumb_tip].y > lm_list[thumb_tip - 1].y > lm_list[thumb_tip - 2].y and lm_list[0].x < lm_list[3].y:
                    cv2.putText(img, "NOT NOW", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (65 ,105, 225), 3)
                    engine.say("Not Now")
                    engine.runAndWait()
                    print("NOT NOW")
                    # h, w, c = dislike_img.shape
                    # img[35:h + 35, 30:w + 30] = dislike_img


            mp_draw.draw_landmarks(img, hand_landmark,
                                   mp_hands.HAND_CONNECTIONS,
                                   mp_draw.DrawingSpec((0, 0, 255), 6, 3),
                                   mp_draw.DrawingSpec((0, 255, 0), 4, 2)
                                   )

    cv2.imshow("Hand Sign Detection", img)
    cv2.waitKey(1)
