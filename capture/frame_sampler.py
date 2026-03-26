import cv2
import base64

class FrameSampler:
    def __init__(self, camera_index=0):
        # camera_index 0 is usually the default built-in laptop webcam
        self.camera_index = camera_index
        self.video_capture = cv2.VideoCapture(self.camera_index)
        
    def captureFrame(self):
        """Grabs a single frame from the webcam and encodes it for the AI."""
        ret, frame = self.video_capture.read()
        
        if not ret:
            print("Error: Could not read frame from webcam.")
            return None
            
        # Compress and encode the frame as a JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        
        # Convert the raw bytes to a base64 string
        base64_string = base64.b64encode(buffer).decode('utf-8')
        
        return base64_string
        
    def releaseCamera(self):
        """Frees up the webcam resource when the game is over."""
        self.video_capture.release()