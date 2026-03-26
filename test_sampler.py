import cv2
import base64
import numpy as np
from capture.frame_sampler import FrameSampler

def testCamera():
    print("Initializing camera...")
    # Initialize the sampler we just built
    sampler = FrameSampler()
    
    print("Capturing frame...")
    b64_string = sampler.captureFrame()
    
    if b64_string:
        print(f"Success! Captured base64 string of length: {len(b64_string)}")
        
        # Decode the base64 string back into raw bytes
        img_data = base64.b64decode(b64_string)
        
        # Convert bytes to a numpy array, then to an OpenCV image
        np_arr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        # Save it to disk so you can visually verify it
        output_filename = "test_capture.jpg"
        cv2.imwrite(output_filename, img)
        print(f"Saved test frame to '{output_filename}'. Open your folder to check it out!")
    else:
        print("Failed to capture frame. Check if another app is using your webcam.")
        
    sampler.releaseCamera()
    print("Camera released.")

if __name__ == "__main__":
    testCamera()