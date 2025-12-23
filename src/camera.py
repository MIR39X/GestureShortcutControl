import cv2

class Camera:
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise Exception(f"Could not open video device {camera_index}")

    def read_frame(self):
        success, frame = self.cap.read()
        if not success:
            return None
        # Flip the frame horizontally for a later selfie-view display
        return cv2.flip(frame, 1)

    def release(self):
        self.cap.release()
