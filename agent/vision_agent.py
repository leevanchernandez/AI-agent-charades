import base64
from google import genai
from google.genai import types
from config import GEMINI_API_KEY
class VisionAgent:
    def __init__(self):
        # We pass the safe key from config directly into the client here
        self.client = genai.Client(api_key=GEMINI_API_KEY) 

    def describeFrame(self, base64_image: str) -> str:
        """Analyzes a frame and returns a text description of the player's action."""
        
        # Convert the base64 string back to raw bytes for the API
        image_bytes = base64.b64decode(base64_image)
        
        # We want short, punchy, action-oriented text.
        system_prompt = (
            "You are the eyes of an AI playing charades. "
            "Do NOT just describe literal body positioning (like 'arms extended' or 'fists up'). "
            "Instead, interpret the ACTION and the INTENT. "
            "What imaginary object is the person holding? What specific activity are they pantomiming? "
            "Provide one short, highly descriptive sentence. "
            "Examples: 'The person is casting an invisible fishing rod' or 'The person is swinging a baseball bat'."
        )
        # Send the image and prompt to the Gemini API
        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                # Pass the image and prompt to the API 
                # types.Part.from_bytes is used to convert the image bytes to a format that the API can understand
                contents=[
                    types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg'),
                    system_prompt
                ]
            )
            # Return the AI's response
            # .strip() removes any leading/trailing whitespace from the response
            return response.text.strip()
            
        # Catch any errors from the API
        except Exception as e:
            print(f"Vision API Error: {e}")
            return "Error: Could not analyze the frame."