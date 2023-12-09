import cv2
import mediapipe as mp
import pyautogui
import uuid
import os

# os.mkdir('shot')

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
mode = 0
capture = cv2.VideoCapture(0)
with mp_hands.Hands(
  model_complexity=0,
  min_detection_confidence=0.7,
  min_tracking_confidence=0.7) as hands:
  while capture.isOpened():
    success, imageraw = capture.read()
    if not success:
      print('Ignored empty webcam\'s frame')
      continue
    imageraw.flags.writeable = False
    image = cv2.cvtColor(imageraw, cv2.COLOR_BGR2RGB)
    image = cv2.flip(image, 1)
    results = hands.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    fingerCount = 0
    r = 1
    l = 0

    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        handIndex = results.multi_hand_landmarks.index(hand_landmarks)
        handLabel = results.multi_handedness[handIndex].classification[0].label

        handLandmarks = []

        for landmarks in hand_landmarks.landmark:
          handLandmarks.append([landmarks.x, landmarks.y])

        # print (handLandmarks[8])
        

        if handLabel == "Left" and handLandmarks[4][0] > handLandmarks[3][0]:
          fingerCount = fingerCount + 1
        elif handLabel == "Right" and handLandmarks[4][0] < handLandmarks[3][0]:
          fingerCount = fingerCount + 1
  
        if handLandmarks[8][1] < handLandmarks[6][1]:
              fingerCount = fingerCount + 1
              
        if handLandmarks[12][1] < handLandmarks[10][1]:
              fingerCount = fingerCount + 1

        if handLandmarks[16][1] < handLandmarks[14][1]:
          fingerCount = fingerCount + 1
          
        if handLandmarks[20][1] < handLandmarks[18][1]:
          fingerCount = fingerCount + 1

        if mode==1:
          if handLabel == "Left" and handLandmarks[4][0] > handLandmarks[3][0] and handLandmarks[8][1] < handLandmarks[6][1] and handLandmarks[12][1] > handLandmarks[10][1] and handLandmarks[16][1] > handLandmarks[14][1] and handLandmarks[20][1] > handLandmarks[18][1]:
            pyautogui.press('volumeup')
            cv2.putText(image, str('volumeup'), (0,50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (250,0,0), 2)
          
          elif handLabel == "Left" and handLandmarks[4][0] > handLandmarks[3][0] and handLandmarks[8][1] > handLandmarks[6][1] and handLandmarks[12][1] > handLandmarks[10][1] and handLandmarks[16][1] > handLandmarks[14][1] and handLandmarks[20][1] < handLandmarks[18][1]:
            pyautogui.press('volumedown')
            cv2.putText(image, str('volumedown'), (0,50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (250,0,0), 2)


        if mode ==2:  
          if handLabel == "Right" and handLandmarks[4][0] > handLandmarks[3][0] and handLandmarks[8][1] < handLandmarks[6][1] and handLandmarks[12][1] < handLandmarks[10][1] and handLandmarks[16][1] > handLandmarks[14][1] and handLandmarks[20][1] > handLandmarks[18][1]:
            cv2.imwrite(os.path.join('shot', '{}.jpg'.format(uuid.uuid1())), imageraw)
            cv2.putText(image, str('shot'), (500,50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (250,0,0), 2)
    
        if mode == 3:
          if handLabel == "Left" and handLandmarks[4][0] > handLandmarks[3][0] and handLandmarks[8][1] < handLandmarks[6][1] and handLandmarks[12][1] > handLandmarks[10][1] and handLandmarks[16][1] > handLandmarks[14][1] and handLandmarks[20][1] > handLandmarks[18][1]:
                pyautogui.press('up')
          if handLabel == "Right" and handLandmarks[8][1] < handLandmarks[6][1] :
                if handLandmarks[8][0] > 0.45:
                      pyautogui.press('right')
                      print('right')
                elif handLandmarks[8][0] < 0.45:
                      pyautogui.press('left')
                      print('left')


        mp_drawing.draw_landmarks(
          image,
          hand_landmarks,
          mp_hands.HAND_CONNECTIONS
        )


    cv2.putText(image, str(fingerCount), (300,100), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (255,255,0), 7)
    cv2.putText(image, str('mode = {}' .format(mode)), (0,475), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (250,0,0), 2)
    cv2.imshow('Apps',image)
    if cv2.waitKey(2)& 0xFF == ord('q'):
        break
    if cv2.waitKey(2)&0xFF == ord('g'):
          mode = (mode + 1)%4
          print(mode)
  capture.release()
  cv2.destroyAllWindows()


  #eiei