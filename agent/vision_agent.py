import base64
from google import genai
from google.genai import types
# from config import GEMINI_API_KEY
import mediapipe as mp
import os

class VisionAgent:
    def __init__(self):
        # We pass the safe key from config directly into the client here
        # self.client = genai.Client(api_key=GEMINI_API_KEY) 
        self.media_pipe_model = os.path.join(os.path.dirname(__file__), "gesture_recognizer.task")
            
    
    # def describeFrame(self, base64_image: str) -> str:
    #     """Analyzes a frame and returns a text description of the player's action."""
        
    #     # Convert the base64 string back to raw bytes for the API
    #     image_bytes = base64.b64decode(base64_image)
        
    #     # We want short, punchy, action-oriented text.
    #     system_prompt = (
    #         "You are the eyes of an AI playing charades. "
    #         "Briefly describe the exact physical pose, gesture, or action "
    #         "the person in this image is making in one short sentence. "
    #         "Ignore the background and focus entirely on the human's movement."
    #     )
        
    #     # Send the image and prompt to the Gemini API
    #     try:
    #         response = self.client.models.generate_content(
    #             model='gemini-2.5-flash',
    #             # Pass the image and prompt to the API 
    #             # types.Part.from_bytes is used to convert the image bytes to a format that the API can understand
    #             contents=[
    #                 types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg'),
    #                 system_prompt
    #             ]
    #         )
    #         # Return the AI's response
    #         # .strip() removes any leading/trailing whitespace from the response
    #         return response.text.strip()
            
    #     # Catch any errors from the API
    #     except Exception as e:
    #         print(f"Vision API Error: {e}")
    #         return "Error: Could not analyze the frame."