import cv2
import time
import threading
import sys
import os

# Force Python to look in your main agent_charades folder for your modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from capture.frame_sampler import FrameSampler
from agent.vision_agent import VisionAgent

def testLiveVision():
    print("Starting Live Vision Test...")
    print("The camera will pop up in a new window. Press 'q' on your keyboard to quit.")
    
    sampler = FrameSampler()
    vision_ai = VisionAgent()
    
    last_request_time = 0
    cooldown_seconds = 2q0 # This strictly enforces our 15 RPM limit!
    
    # This function runs in the background so your video doesn't freeze
    def call_ai(base64_img):
        print("\n[Snapping photo and sending to Gemini...]")
        description = vision_ai.describeFrame(base64_img)
        print(f"\n---> AI EYES: {description}\n")

    while True:
        raw_frame, base64_string = sampler.captureFrame()
        
        if raw_frame is None:
            continue
            
        # Show the live video on your screen
        cv2.imshow("Live Vision Test", raw_frame)
        
        # Check our timer: Has it been cooldown_seconds seconds since the last photo?
        current_time = time.time()
        if current_time - last_request_time > cooldown_seconds:
            last_request_time = current_time
            # Launch the background thread to talk to Gemini
            threading.Thread(target=call_ai, args=(base64_string,)).start()
            
        # Standard OpenCV code to safely close the window if you press 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    sampler.releaseCamera()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    testLiveVision()