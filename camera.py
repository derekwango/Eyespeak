import cv2
from PyQt5.QtGui import QImage, QPixmap
from blink_detector import BlinkDetector

class Camera:
    def __init__(self, label, blink_callback):
        self.capture = cv2.VideoCapture(0)
        self.label = label
        self.blink_detector = BlinkDetector(blink_callback)
    
    def get_frame(self):
        ret, frame = self.capture.read()
        if not ret:
            return None
        
        # Mirror the image and process with blink detector
        frame = cv2.flip(frame, 1)
        frame = self.blink_detector.process_frame(frame)
        
        # Convert to RGB for display
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        return QPixmap.fromImage(QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888))
    
    def release_camera(self):
        self.capture.release()