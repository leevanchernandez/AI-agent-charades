import time
from google import genai
from config import GEMINI_API_KEY, VISION_MODEL

class VisionAgent:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        
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
                "You are an expert at playing charades. Watch this short video "
                "of a person pantomiming a word. Based ONLY on their continuous motions "
                "and physical actions, guess what object, animal, or concept they are acting out. "
                "Provide ONLY the final guess as a single word or short phrase. "
                "Do NOT explain your reasoning. Do NOT use punctuation."
            )
            
            print("🚀 Asking Gemma 3 27B to guess the charade...")
            response = self.client.models.generate_content(
                model=VISION_MODEL, 
                contents=[video_file, system_prompt]
            )
            
            return response.text.strip()
            
        except Exception as e:
            print(f"Vision API Error: {e}")
            return "Error analyzing video."