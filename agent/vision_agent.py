import time
import os
from google import genai
from config import GEMINI_API_KEY, VISION_MODEL


class VisionAgent:
    def __init__(self):
        # We pass the safe key from config directly into the client here
        self.client = genai.Client(api_key=GEMINI_API_KEY) 
        self.media_pipe_model = os.path.join(os.path.dirname(__file__), "gesture_recognizer.task")
        
        # 2. The AI's Short-Term Memory
        self.uploaded_videos = [] 
        self.past_interpretations = []
        self.wrong_guesses = []
            

    def guessFromVideo(self, new_video_path: str) -> dict:
        """Uploads the newest video, stacks it with past videos, and returns an interpretation + guess."""
        print(f"☁️ Uploading {new_video_path} to Google servers...")
        
        try:
            # 3. Upload ONLY the newest video
            video_file = self.client.files.upload(file=new_video_path)
            # Wait for the video to finish processing
            while video_file.state.name == 'PROCESSING':
                print("⏳ Waiting for video processing...")
                time.sleep(2)
                video_file = self.client.files.get(name=video_file.name)
                
            # 4. Add the new video to our running stack
            self.uploaded_videos.append(video_file)
                
            # 5. Build the dynamic prompt using YOUR custom rules + our memory system
            prompt_text = (
                "You are playing charades. Your job is to infer the intended charade from "
                "a sequence of short video clips of a person acting without speech.\n\n"
                "Rules:\n"
                "- Focus on repeated body motions, hand actions, object mimicry, and interaction patterns.\n"
                "- Ignore appearance, clothing, background, and identity.\n"
                "- Infer the intended noun, verb, animal, object, or short concept being pantomimed.\n"
                "- Prefer the simplest common answer over a rare or overly specific one.\n"
                "- If multiple interpretations are possible, choose the one best supported by the motion pattern.\n"
            )
            
            # Inject short-term memory of past clips
            if self.past_interpretations:
                prompt_text += "\nHere is what you saw in previous clips:\n"
                for i, interp in enumerate(self.past_interpretations):
                    prompt_text += f"- Clip {i+1}: {interp}\n"
                    
            # Inject memory of wrong guesses so it doesn't loop
            if self.wrong_guesses:
                prompt_text += f"\nYou already guessed these incorrectly: {', '.join(self.wrong_guesses)}. DO NOT guess these again.\n"
                
            # Enforce the strict output format so our Python code can parse it cleanly
            prompt_text += (
                "\nBased on ALL the videos, provide a brief interpretation of the newest action, "
                "followed by your new final guess.\n"
                "Format your response EXACTLY like this (no extra text, no markdown):\n"
                "Interpretation: [Your brief description of the newest motion]\n"
                "Guess: [Your short lowercase phrase]"
            )
            
            # Ask the AI to guess the charade
            print(f"🚀 Asking {VISION_MODEL} to analyze {len(self.uploaded_videos)} stacked videos...")
            # 6. The Payload: Pass ALL videos in the list, plus the text prompt at the end
            payload = self.uploaded_videos + [prompt_text]
            
            response = self.client.models.generate_content(
                model=VISION_MODEL, 
                contents=payload
            )
            text = response.text.strip()
            
            # 7. Parse the strict formatting
            try:
                # Split the response into individual lines
                interp_line = [line for line in text.split('\n') if 'Interpretation:' in line][0]
                guess_line = [line for line in text.split('\n') if 'Guess:' in line][0]
                
                # Remove the label and strip whitespace
                interp = interp_line.replace('Interpretation:', '').strip()
                guess = guess_line.replace('Guess:', '').strip()
            except Exception as e:
                # Fallback just in case the AI ignores formatting
                print(f"⚠️ Formatting parse error: {e}. Raw text: {text}")
                interp = "Could not parse formatting."
                guess = text.split('\n')[-1].replace('Guess:', '').strip()
            
            # 8. Save this attempt to memory so it knows not to guess it again next time
            self.past_interpretations.append(interp)
            self.wrong_guesses.append(guess)
            
            return {"interpretation": interp, "guess": guess}
            
        except Exception as e:
            print(f"Vision API Error: {e}")
            return {"interpretation": "Error", "guess": "Error analyzing video."}