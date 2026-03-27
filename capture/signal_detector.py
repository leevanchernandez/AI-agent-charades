import mediapipe as mp
import os

class SignalDetector:
    def __init__(self):
        # Model is located in the agent folder, so we map the path correctly
        self.media_pipe_model = os.path.join(os.path.dirname(__file__), "..", "agent", "gesture_recognizer.task")

    def mediapipepose(self, livestream) -> str:
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
