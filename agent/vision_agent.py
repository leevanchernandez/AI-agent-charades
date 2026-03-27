import time
import os
from google import genai
from config import GEMINI_API_KEY, VISION_MODEL


class VisionAgent:
    def __init__(self):
        # We pass the safe key from config directly into the client here
        self.client = genai.Client(api_key=GEMINI_API_KEY) 
        self.media_pipe_model = os.path.join(os.path.dirname(__file__), "gesture_recognizer.task")
            
    
    def guessFromVideo(self, video_path: str) -> str:
        """Uploads a video and asks Gemma 3 to directly guess the charade."""
        print(f"☁️ Uploading {video_path} to Google servers...")
        
        try:
            video_file = self.client.files.upload(file=video_path)
            
            while video_file.state.name == 'PROCESSING':
                print("⏳ Waiting for video processing...")
                time.sleep(2)
                video_file = self.client.files.get(name=video_file.name)
                
            # We combine the Vision and Guessing instructions into one brutal prompt
            system_prompt = (
                """
                You are playing charades.

                Your job is to infer the intended charade from a short video of a person acting without speech.

                Rules:
                - Focus on repeated body motions, hand actions, object mimicry, and interaction patterns.
                - Ignore appearance, clothing, background, and identity.
                - Infer the intended noun, verb, animal, object, or short concept being pantomimed.
                - Prefer the simplest common answer over a rare or overly specific one.
                - If multiple interpretations are possible, choose the one best supported by the motion pattern.
                - Return only one answer.
                - Output only the final guess as a short lowercase phrase.
                - No explanation.
                """
            )
            
            print(f"🚀 Asking {VISION_MODEL} to guess the charade...")
            response = self.client.models.generate_content(
                model=VISION_MODEL, 
                contents=[video_file, system_prompt]
            )
            
            return response.text.strip()
            
        except Exception as e:
            print(f"Vision API Error: {e}")
            return "Error analyzing video."