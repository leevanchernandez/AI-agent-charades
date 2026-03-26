import time
# We will uncomment these as they get built
from capture.frame_sampler import FrameSampler
# from context.context_buffer import ContextBuffer
# from agent.vision_agent import VisionAgent
# from agent.guess_engine import GuessEngine

def runCharadesGame():
    print("Initializing Agent Charades...")
    sampler = FrameSampler()
    
    # Partner A can work on getting this dummy loop to process real vision data
    # Partner B can work on hooking up the audio/UI outputs to this loop
    
    try:
        while True:
            base64_frame = sampler.captureFrame()
            if not base64_frame:
                continue
                
            print("Frame captured! (Waiting for Vision/Guess modules...)")
            
            # TODO: Add vision description logic here
            # TODO: Add guess engine logic here
            # TODO: Add UI/Voice output here
            
            time.sleep(1) # Temporary rate limit
            
    except KeyboardInterrupt:
        print("\nStopping game...")
    finally:
        sampler.releaseCamera()
        print("Clean shutdown complete.")

if __name__ == "__main__":
    runCharadesGame()