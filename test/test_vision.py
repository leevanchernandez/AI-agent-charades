import base64
import os
import sys

# Force Python to look in your main agent_charades folder for your modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.vision_agent import VisionAgent

def testVisionApi():
    print("Initializing Vision Agent...")
    vision_ai = VisionAgent()
    
    # Dynamically find the project root folder to locate the image
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    test_image_path = os.path.join(project_root, "test_capture.jpg")
    
    # Fallback just in case it saved directly inside the tests folder
    if not os.path.exists(test_image_path):
        test_image_path = os.path.join(os.path.dirname(__file__), "test_capture.jpg")
        
    if not os.path.exists(test_image_path):
        print(f"Error: Could not find 'test_capture.jpg'.")
        print("Please run 'python tests/test_sampler.py' first to take a picture!")
        return

    print(f"Found image at {test_image_path}. Encoding...")
    
    # 1. Read the raw bytes of the image from your hard drive
    with open(test_image_path, "rb") as image_file:
        raw_bytes = image_file.read()
        
    # 2. Convert the bytes into the base64 string our agent expects
    base64_frame = base64.b64encode(raw_bytes).decode('utf-8')
        
    print("Sending payload to Gemini API... (Waiting for response)")
    
    # 3. Make the actual API call
    ai_description = vision_ai.describeFrame(base64_frame)
    
    print("\n" + "="*20 + " AI RESPONSE " + "="*20)
    print(ai_description)
    print("="*53 + "\n")

if __name__ == "__main__":
    testVisionApi()