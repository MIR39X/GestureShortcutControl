import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

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
    
    if result.hand_landmarks:
        for hand_landmarks in result.hand_landmarks:
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
            
            cv2.putText(
                frame,
                f"Fingers: {fingers}",
                (30,80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255,255,0),
                2  
            )
             
            
            
            
            
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