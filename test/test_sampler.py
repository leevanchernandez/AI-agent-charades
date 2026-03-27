import cv2
import sys
import os

# --- THE FIX ---
# This forces Python to look in your main agent_charades folder for your modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from capture.frame_sampler import FrameSampler

def testCamera():
    print("Initializing camera...")
    sampler = FrameSampler()
    
    print("Capturing frame...")
    # Unpack BOTH the raw OpenCV image and the text string
    raw_frame, base64_string = sampler.captureFrame()
    
    # We check if raw_frame exists to make sure the webcam actually fired
    if raw_frame is not None:
        print(f"Success! Captured base64 string of length: {len(base64_string)}")
        
        # Save the raw frame directly to disk!
        output_filename = "test_capture.jpg" # This will save inside the tests folder
        cv2.imwrite(output_filename, raw_frame)
        print(f"Saved test frame to '{output_filename}'. Open your folder to check it out!")
    else:
        print("Failed to capture frame. Check if another app is using your webcam.")
        
    sampler.releaseCamera()
    print("Camera released.")

if __name__ == "__main__":
    testCamera()