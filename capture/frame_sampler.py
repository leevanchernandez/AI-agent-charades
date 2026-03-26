import cv2
import base64

class FrameSampler:
    def __init__(self, camera_index=0):
        # camera_index = 0 -> use default webcam
        self.camera_index = camera_index
        
        # Initialize the webcam using openCV VideoCapture method
        self.video_capture = cv2.VideoCapture(self.camera_index)
        
    def captureFrame(self):
        """Grabs a frame, returning BOTH the raw image for the UI and base64 for the AI."""
        
        # ret is a boolean that indicates whether the frame was captured successfully
        # frame is the actual image data
        ret, frame = self.video_capture.read()
        
        # If the frame was not captured successfully, print an error message and return None
        if not ret:
            print("Error: Could not read frame from webcam.")
            return None, None
            
        # Encode the frame as a JPEG image
        # _ is a placeholder for the return value that we don't need
        # buffer is the encoded image data
        _, buffer = cv2.imencode('.jpg', frame)
        
        # Convert the buffer to a base64 string
        base64_string = base64.b64encode(buffer).decode('utf-8')
        
        # Return the raw frame and the base64 string
        return frame, base64_string
        
    def releaseCamera(self):
        """Releases the webcam resource."""
        self.video_capture.release()