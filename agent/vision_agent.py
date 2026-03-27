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
        self.media_pipe_pose_model = os.path.join(os.path.dirname(__file__), "pose_landmarker_heavy.task")

    def mediapipehandpose(self, livestream) -> str:
        """Uses MediaPipe to analyze the player's pose and returns a description."""
        BaseOptions = mp.tasks.BaseOptions
        GestureRecognizer = mp.tasks.vision.GestureRecognizer
        GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
        GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
        VisionRunningMode = mp.tasks.vision.RunningMode
        
        # Set up the gesture recognizer options
        options = GestureRecognizerOptions(
            base_options=BaseOptions(model_asset_path=self.media_pipe_model),
            running_mode=VisionRunningMode.IMAGE
        )
        
        # Create the recognizer
        with GestureRecognizer.create_from_options(options) as recognizer:
            # Convert the OpenCV frame to MediaPipe Image
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=livestream)
            
            # Recognize gestures
            result = recognizer.recognize(mp_image)
            
            # Check if any gestures were detected
            if result.gestures:
                # Get the top gesture (first in the list)
                top_gesture = result.gestures[0][0]
                return top_gesture.category_name
            else:
                return "No gesture detected"
            
    def mediapipebodypose(self, livestream) -> str:
        """Uses MediaPipe to analyze the player's pose and returns a description."""
        base_options = mp.tasks.BaseOptions
        options = mp.tasks.vision.PoseLandmarkerOptions(
            base_options=base_options(model_asset_path=self.media_pipe_pose_model),
            output_segmentation_masks=True)
        detector = mp.tasks.vision.PoseLandmarker.create_from_options(options)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=livestream)
        result = detector.detect(mp_image)
        if result.pose_landmarks:
            # Define body part names for the 33 landmarks
            body_parts = [
                "nose", "left_eye_inner", "left_eye", "left_eye_outer", "right_eye_inner",
                "right_eye", "right_eye_outer", "left_ear", "right_ear", "mouth_left",
                "mouth_right", "left_shoulder", "right_shoulder", "left_elbow", "right_elbow",
                "left_wrist", "right_wrist", "left_pinky", "right_pinky", "left_index",
                "right_index", "left_thumb", "right_thumb", "left_hip", "right_hip",
                "left_knee", "right_knee", "left_ankle", "right_ankle", "left_heel",
                "right_heel", "left_foot_index", "right_foot_index"
            ]
            # Calculate average visibility
            total_visibility = sum(landmark.visibility for landmark in result.pose_landmarks[0] if hasattr(landmark, 'visibility'))
            avg_visibility = total_visibility / len(result.pose_landmarks[0]) if result.pose_landmarks[0] else 0
            if avg_visibility < 0.5:
                print(f"Low confidence pose detected (avg visibility: {avg_visibility:.3f})")
                return "Low confidence pose detected"
            print(f"Detected pose with average visibility: {avg_visibility:.3f}")
            print("Detected body parts and coordinates:")
            for i, landmark in enumerate(result.pose_landmarks[0]):
                body_part = body_parts[i] if i < len(body_parts) else f"landmark_{i}"
                visibility = getattr(landmark, 'visibility', 1.0)
                print(f"{body_part}: ({landmark.x:.3f}, {landmark.y:.3f}, {landmark.z:.3f}) visibility: {visibility:.3f}")
            return f"{len(result.pose_landmarks[0])} landmarks"
        else:
            return "No pose detected"
    
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