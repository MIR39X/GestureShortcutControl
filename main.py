# This Python code snippet is using the OpenCV library (`cv2`) and the MediaPipe library (`mediapipe`)
# to perform hand gesture recognition using a webcam feed. Here is a breakdown of what the code is
# doing:
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time
import json
import pyautogui


pyautogui.FAILSAFE = True

base_options = python.BaseOptions(
    model_asset_path='hand_landmarker.task'
    )

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1
)

detector = vision.HandLandmarker.create_from_options(options)
# hands = mp_hands.Hands(
#     static_image_mode=False,
#     max_num_hands=2,
#     min_detection_confidence=0.7,
#     min_tracking_confidence=0.7
# )


cap = cv2.VideoCapture(0)
fingers = []

last_gesture = None
last_time = 0
COOLDOWN = 2.0 #seconds 

def get_gesture(fingers):
    if fingers == [1,1,1,1,1]:
         return "OPEN_PALM"
    elif fingers == [0,0,0,0,0]:
        return "FIST"
    elif fingers == [0,1,1,0,0]:
        return "TWO_FINGERS"
    elif fingers == [1,0,0,0,0]:
         return "THUMB"
    else:
        return "UNKNOWN"
    

with open("config.json", "r") as f:
    gesture_map = json.load(f)
    
prev_wrist_x = None
prev_wrist_y = None

SWIPE_THRESHOLD = 0.08   # tune later



while True:
    success, frame = cap.read()
    if not success:
        print("Failed to capture image")
        break
    
    frame = cv2.flip(frame, 1) # Mirror the frame
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )
    result = detector.detect(mp_image)
    gesture = "UNKNOWN"

    
    # gesture = get_gesture(fingers)
    
    cv2.putText(
        frame,
        f"Gesture: {gesture}",
        (30,120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (255,255,255),
        2
    )
    if result.hand_landmarks:
        for hand_landmarks in result.hand_landmarks:
            wrist = hand_landmarks[0]
            current_x = wrist.x
            current_y = wrist.y
            
            swipe = None
            if prev_wrist_x is not None and prev_wrist_y is not None:
                dx = current_x - prev_wrist_x
                dy = current_y - prev_wrist_y
                
                if abs(dx) > abs(dy):
                    if dx > SWIPE_THRESHOLD:
                        swipe = "SWIPE_RIGHT"
                    elif dx < -SWIPE_THRESHOLD:
                        swipe = "SWIPE_LEFT"
                else:
                    if dy > SWIPE_THRESHOLD:
                        swipe = "SWIPE_DOWN"
                    elif dy < -SWIPE_THRESHOLD:
                        swipe = "SWIPE_UP"
            prev_wrist_x = current_x
            prev_wrist_y = current_y

            fingers = []
           
            #Thumb
            thumb_tip = hand_landmarks[4]
            thumb_pip = hand_landmarks[3]
            
            if thumb_tip.x < thumb_pip.x:
                fingers.append(1)
            else:
                fingers.append(0)
            # ROOKIE MISTAKE fingers.append(1 if thumb_tip.x < thumb_pip.x else 0)
            
            # Index Finger
            index_tip = hand_landmarks[8]
            index_pip = hand_landmarks[6]
            fingers.append(1 if index_tip.y < index_pip.y else 0)
            
            # Middle finger
            middle_tip = hand_landmarks[12]
            middle_pip = hand_landmarks[10]
            fingers.append(1 if middle_tip.y < middle_pip.y else 0)
            
            # RING finger
            r_tip = hand_landmarks[16]
            r_pip = hand_landmarks[14]
            fingers.append(1 if r_tip.y < r_pip.y else 0)
            
            # Pinky finger
            pinky_tip = hand_landmarks[20]
            pinky_pip = hand_landmarks[18]
            fingers.append(1 if pinky_tip.y < pinky_pip.y else 0)

            gesture = get_gesture(fingers)
    
            gesture = get_gesture(fingers)
            event = swipe if swipe else gesture

            # SO like it should not spam like a simp spam texting to his ignorant gf
            # COOLDOWN var default 1 sec (its good) 
            current_time = time.time()
            
            if event and event != "UNKNOWN":
                if event != last_gesture and (current_time - last_time) > COOLDOWN:
                    if event in gesture_map:
                        # keys = gesture_map[event]
                        pyautogui.hotkey(*gesture_map[event])

                    last_gesture = event
                    last_time = current_time
            
            # Finger Array - Good for like to see fingers are OKAY
            # cv2.putText(
            #     frame,
            #     f"Fingers: {fingers}",
            #     (30,80),
            #     cv2.FONT_HERSHEY_SIMPLEX,
            #     0.8,
            #     (255,255,0),
            #     2  
            # )
             
            
            #Initially when I was testing 
            # middle_tip = hand_landmarks[12]
            # middle_pip = hand_landmarks[10]
            
            # if middle_tip.y < middle_pip.y:
            #     cv2.putText(frame, "FUCK YOU BITCHASS", (30,50),
            #                 cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            # else:
            #     cv2.putText(frame, "NAH YOU GOOD", (30,50),
            #                 cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)
            
            for landmark in hand_landmarks:
              h, w, _ = frame.shape
              x = int(landmark.x * w)
              y = int(landmark.y * h)
              cv2.circle(frame, (x,y), 5, (0, 255, 0), -1)
              
    #ignore this fucking code because google removed type shi 
    # so I had to call cv api type shi
    # rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # results = hands.process(rgb_frame)
    # if results.multi_hand_landmarks:
    #     for hand_landmarks in results.multi_hand_landmarks:
    #         mp_draw.draw_landmarks
    #         (
    #             frame,
    #             hand_landmarks, mp_hands.HAND_CONNECTIONS
    #         )
    
    
    
    cv2.imshow("Webcam Feed", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()