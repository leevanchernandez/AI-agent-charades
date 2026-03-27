import cv2
import time
import threading
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from capture.frame_sampler import FrameSampler
from agent.vision_agent import VisionAgent

def testLiveVision():
    print("Starting Stateful Charades Test...")
    print("Press 'r' to start a 5-second recording round. Press 'q' to quit.")
    
    sampler = FrameSampler()
    vision_ai = VisionAgent()
    
    round_num = 0
    is_recording = False
    start_time = 0
    video_writer = None
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    current_video_filename = ""
    
    # UI Text variables
    display_status = "Press 'r' to record Round 1!"
    last_interp = ""
    last_guess = ""

    def callAi(video_path):
        nonlocal display_status, last_interp, last_guess
        display_status = f"Processing Round {round_num}..."
        
        # Call our new stateful agent!
        result = vision_ai.guessFromVideo(video_path)
        
        last_interp = result['interpretation']
        last_guess = result['guess'].upper()
        display_status = "Press 'r' to add next video, or 'q' to quit."
        
        print("\n" + "="*40)
        print(f"👀 AI SAW: {last_interp}")
        print(f"🎯 AI GUESS: {last_guess}")
        print("="*40 + "\n")

    while True:
        raw_frame, _ = sampler.captureFrame()
        if raw_frame is None:
            continue
            
        key = cv2.waitKey(1) & 0xFF
        
        # Trigger a new recording round when you press 'r'
        if key == ord('r') and not is_recording:
            round_num += 1
            current_video_filename = f"test_charade_round_{round_num}.mp4"
            
            height, width, _ = raw_frame.shape
            video_writer = cv2.VideoWriter(current_video_filename, fourcc, 30.0, (width, height))
            
            is_recording = True
            start_time = time.time()
            display_status = f"🔴 RECORDING ROUND {round_num}..."

        if is_recording:
            elapsed_time = time.time() - start_time
            if elapsed_time < 5.0:
                video_writer.write(raw_frame)
                cv2.putText(raw_frame, f"REC: {5.0 - elapsed_time:.1f}s", (20, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                is_recording = False
                video_writer.release()
                print(f"\n✅ Round {round_num} recorded! Sending to Gemini...")
                # Launch background thread so webcam doesn't freeze
                threading.Thread(target=callAi, args=(current_video_filename,)).start()

        # Draw UI
        if not is_recording:
            cv2.putText(raw_frame, display_status, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            if last_guess:
                cv2.putText(raw_frame, f"Guess: {last_guess}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                cv2.putText(raw_frame, f"Saw: {last_interp[:40]}...", (20, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        cv2.imshow("Stateful Vision Test", raw_frame)
        
        if key == ord('q'):
            break
            
    if video_writer is not None and is_recording:
        video_writer.release()
    sampler.releaseCamera()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    testLiveVision()