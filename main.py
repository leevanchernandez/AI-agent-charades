from capture.frame_sampler import FrameSampler
from output.display import Display
from agent.vision_agent import VisionAgent
from capture.signal_detector import SignalDetector

def runCharadesGame():
    print("Initializing Agent Charades...")
    
    sampler = FrameSampler()
    vision = VisionAgent()
    signal_detector = SignalDetector()
    ui = Display()
    
    # We will update this variable later when the AI makes real guesses
    current_ai_guess = "Thinking..." 
    
    try:
        while True:
            # Grab both the raw frame (for us) and the base64 (for the AI)
            raw_frame, base64_frame = sampler.captureFrame()
            
            if raw_frame is None:
                continue
            
            # Show the live video feed on the screen
            # If showFrame returns False (meaning you pressed 'q'), break the loop
            keep_running = ui.showFrame(raw_frame, current_ai_guess)
            if not keep_running:
                break
            
            # (AI Logic will go here later)
            mediapipe_result = signal_detector.mediapipefingercounter(raw_frame)
            current_ai_guess = f"AI sees: {mediapipe_result}"
    except KeyboardInterrupt:
        print("\nStopping game...")
    finally:
        sampler.releaseCamera()
        ui.close()
        print("Clean shutdown complete.")

if __name__ == "__main__":
    runCharadesGame()