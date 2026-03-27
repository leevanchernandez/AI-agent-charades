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
    print("Starting Live Vision Video Test...")
    print("The camera will pop up. Do your charade immediately!")
    print("Recording for 5 seconds...")
    
    sampler = FrameSampler()
    vision_ai = VisionAgent()
    
    # Setup video recording variables
    video_filename = "test_charade.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = None
    
    start_time = time.time()
    is_recording = True
    request_sent = False
    
    # Background function to handle the API call so video doesn't freeze
    def callAi(video_path):
        print(f"\n[Thread] ☁️ Uploading {video_path} to Google servers...")
        print("[Thread] 🚀 Prompting AI: 'Watch this short video... guess what object, animal, or concept they are acting out...'")
        
        # Using the consolidated VisionAgent we just built!
        guess = vision_ai.guessFromVideo(video_path)
        
        print("\n" + "="*20 + " AI GUESS " + "="*20)
        print(f"🎯 {guess.upper()}")
        print("="*50 + "\n")
        print("[Webcam is still running. Press 'q' to quit.]")

    while True:
        # We only need the raw_frame now, ignore the base64 string
        raw_frame, _ = sampler.captureFrame()
        
        if raw_frame is None:
            continue
            
        # Initialize video writer once we have the first frame's dimensions
        if is_recording and video_writer is None:
            height, width, _ = raw_frame.shape
            video_writer = cv2.VideoWriter(video_filename, fourcc, 30.0, (width, height))
            
        if is_recording:
            elapsed_time = time.time() - start_time
            if elapsed_time < 5.0:
                # Write frame to the .mp4 file
                video_writer.write(raw_frame)
                
                # Draw a red recording indicator on the screen
                cv2.putText(raw_frame, f"REC: {5.0 - elapsed_time:.1f}s", (20, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                # 5 seconds are up! Stop recording.
                is_recording = False
                video_writer.release()
                print("\n✅ 5-second recording complete!")
                
        # Only send the request ONCE, immediately after recording stops
        if not is_recording and not request_sent:
            request_sent = True
            threading.Thread(target=callAi, args=(video_filename,)).start()
        
        # If we are done recording, show green processing text
        if not is_recording and request_sent:
            cv2.putText(raw_frame, "Processing video... Check terminal.", (20, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Show the live video on your screen
        cv2.imshow("Live Vision Test", raw_frame)
        
        # Standard OpenCV code to safely close the window if you press 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    # Cleanup
    if video_writer is not None and is_recording:
        video_writer.release()
    sampler.releaseCamera()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    testLiveVision()