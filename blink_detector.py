import cv2
import mediapipe as mp
import numpy as np
from scipy.spatial import distance as dist

class BlinkDetector:
    def __init__(self, callback):
        self.callback = callback
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_face_detection = mp.solutions.face_detection
        
        # Initialize face mesh and face detection
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            min_detection_confidence=0.5, 
            min_tracking_confidence=0.5
        )
        self.face_detector = self.mp_face_detection.FaceDetection(
            min_detection_confidence=0.5
        )
        
        # More sophisticated blink detection parameters
        self.EAR_THRESHOLD = 0.2  # Lowered threshold for more sensitivity
        self.CONSEC_FRAMES_THRESHOLD = 1  # Minimum frames to consider a blink
        self.MAX_BLINK_FRAMES = 3  # Maximum frames for a blink to prevent false positives
        
        # Tracking variables
        self.blink_counter = 0
        self.total_blinks = 0
        self.current_blink_state = False

    def eye_aspect_ratio(self, eye):
        """
        Calculate the Eye Aspect Ratio (EAR) with improved vertical landmark measurement
        """
        # Vertical eye landmarks (both top and bottom points)
        A = dist.euclidean(eye[1], eye[5])  # Top-left to bottom-left
        B = dist.euclidean(eye[2], eye[4])  # Top-right to bottom-right
        
        # Horizontal eye landmark (width)
        C = dist.euclidean(eye[0], eye[3])  # Left to right corner
        
        # Calculate EAR
        ear = (A + B) / (2.0 * C)
        return ear

    def process_frame(self, frame):
        # Convert frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detect faces
        face_results = self.face_detector.process(rgb_frame)
        
        # Detect face mesh landmarks
        mesh_results = self.face_mesh.process(rgb_frame)
        
        # Draw face rectangle if face is detected
        if face_results.detections:
            for detection in face_results.detections:
                # Get bounding box
                bbox = detection.location_data.relative_bounding_box
                h, w, _ = frame.shape
                
                # Convert to pixel coordinates
                x = int(bbox.xmin * w)
                y = int(bbox.ymin * h)
                width = int(bbox.width * w)
                height = int(bbox.height * h)
                
                # Draw rectangle around face
                cv2.rectangle(frame, (x, y), (x + width, y + height), 
                              (0, 255, 0), 2)  # Green rectangle
        
        # Process face landmarks and blink detection
        if mesh_results.multi_face_landmarks:
            for face_landmarks in mesh_results.multi_face_landmarks:
                # Extract precise eye landmarks for left and right eyes
                left_eye = np.array([(face_landmarks.landmark[i].x * frame.shape[1], 
                                      face_landmarks.landmark[i].y * frame.shape[0]) 
                                     for i in [33, 160, 158, 133, 153, 144]])
                right_eye = np.array([(face_landmarks.landmark[i].x * frame.shape[1], 
                                       face_landmarks.landmark[i].y * frame.shape[0]) 
                                      for i in [362, 385, 387, 263, 373, 380]])
                
                # Calculate Eye Aspect Ratio for both eyes
                left_ear = self.eye_aspect_ratio(left_eye)
                right_ear = self.eye_aspect_ratio(right_eye)
                
                # Average EAR of both eyes
                avg_ear = (left_ear + right_ear) / 2.0
                
                # Draw eye landmarks for debugging
                for (x, y) in left_eye:
                    cv2.circle(frame, (int(x), int(y)), 2, (255, 0, 0), -1)
                for (x, y) in right_eye:
                    cv2.circle(frame, (int(x), int(y)), 2, (0, 255, 0), -1)
                
                # Blink detection logic with improved accuracy
                if avg_ear < self.EAR_THRESHOLD:
                    self.blink_counter += 1
                    
                    # Detect blink with more robust conditions
                    if (self.blink_counter >= self.CONSEC_FRAMES_THRESHOLD and 
                        self.blink_counter <= self.MAX_BLINK_FRAMES):
                        
                        if not self.current_blink_state:
                            # Ensure it's a new blink
                            self.total_blinks += 1
                            print(f"Blink detected! Total blinks: {self.total_blinks}")
                            self.callback()
                            self.current_blink_state = True
                else:
                    # Reset blink counter when eyes are open
                    self.blink_counter = 0
                    self.current_blink_state = False
        
        return frame