
import base64
import mediapipe as mp
import os
import math
from requests import options

class SignalDetector:
    def __init__(self):
        self.media_pipe_model = os.path.join(os.path.dirname(__file__), "gesture_recognizer.task")
        self.media_pipe_hand_model = os.path.join(os.path.dirname(__file__), "hand_landmarker.task")

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
    def mediapipefingercounter(self, livestream) -> str:
        def _xyz(p):
            return (p.x, p.y, p.z)

        def _dist(a, b):
            ax, ay, az = _xyz(a) if not isinstance(a, tuple) else a
            bx, by, bz = _xyz(b) if not isinstance(b, tuple) else b
            return ((ax - bx) ** 2 + (ay - by) ** 2 + (az - bz) ** 2) ** 0.5

        def _angle(a, b, c):
            ax, ay, az = _xyz(a)
            bx, by, bz = _xyz(b)
            cx, cy, cz = _xyz(c)

            ba = (ax - bx, ay - by, az - bz)
            bc = (cx - bx, cy - by, cz - bz)

            dot = ba[0]*bc[0] + ba[1]*bc[1] + ba[2]*bc[2]
            norm_ba = (ba[0]**2 + ba[1]**2 + ba[2]**2) ** 0.5
            norm_bc = (bc[0]**2 + bc[1]**2 + bc[2]**2) ** 0.5

            if norm_ba == 0 or norm_bc == 0:
                return 0.0

            cos_theta = dot / (norm_ba * norm_bc)
            cos_theta = max(-1.0, min(1.0, cos_theta))
            return math.degrees(math.acos(cos_theta))

        def _center(*pts):
            xs, ys, zs = zip(*[_xyz(p) for p in pts])
            return (sum(xs) / len(xs), sum(ys) / len(ys), sum(zs) / len(zs))

        def _is_finger_up(hand, mcp, pip, dip, tip):
            # Straight finger in 3D
            pip_angle = _angle(hand[mcp], hand[pip], hand[dip])
            dip_angle = _angle(hand[pip], hand[dip], hand[tip])

            # Tip should be farther from wrist than lower joints
            wrist_progress = (
                _dist(hand[tip], hand[0]) >
                _dist(hand[dip], hand[0]) >
                _dist(hand[pip], hand[0]) >
                _dist(hand[mcp], hand[0])
            )

            return pip_angle > 160 and dip_angle > 160 and wrist_progress

        def _is_thumb_up(hand):
            # Palm reference
            palm_center = _center(hand[0], hand[5], hand[17])
            palm_size = max(_dist(hand[0], hand[9]), _dist(hand[5], hand[17]))

            # Thumb should be fairly straight
            thumb_ip_angle = _angle(hand[2], hand[3], hand[4])

            # Thumb tip should be away from the palm, not folded across it
            thumb_far_from_palm = _dist(hand[4], palm_center) > (_dist(hand[2], palm_center) + 0.20 * palm_size)

            # Extra guard: keep folded thumbs from counting
            thumb_separated = _dist(hand[4], hand[5]) > 0.45 * palm_size

            return thumb_ip_angle > 150 and thumb_far_from_palm and thumb_separated
        #Count fingers currently held up using the hand_landmarker model
        BaseOptions = mp.tasks.BaseOptions
        HandLandmarker = mp.tasks.vision.HandLandmarker
        HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
        HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
        VisionRunningMode = mp.tasks.vision.RunningMode
        options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=self.media_pipe_hand_model),
        running_mode=VisionRunningMode.IMAGE, num_hands=2)
        with HandLandmarker.create_from_options(options) as landmarker:
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=livestream)
            result = landmarker.detect(mp_image)

            if not result.hand_landmarks:
                return "0"

            fingers = 0
            for hand_idx, hand in enumerate(result.hand_landmarks):
                handedness = result.handedness[hand_idx][0].category_name  # "Left" or "Right"

                # ----- Thumb -----
                # More reliable than only tip vs ip because it also checks ordering.
                # Right hand thumb points left in the image, Left hand thumb points right.
                if handedness == "Right":
                    if not hand[4].x < hand[3].x < hand[2].x:
                        fingers += 1
                else:  # Left
                    if not hand[4].x > hand[3].x > hand[2].x:
                        fingers += 1

                # ----- Other fingers -----
                # Stricter check: TIP above PIP and PIP above MCP
                if hand[8].y < hand[6].y < hand[5].y:    # Index
                    fingers += 1

                if hand[12].y < hand[10].y < hand[9].y:  # Middle
                    fingers += 1

                if hand[16].y < hand[14].y < hand[13].y: # Ring
                    fingers += 1

                if hand[20].y < hand[18].y < hand[17].y: # Pinky
                    fingers += 1

            return str(fingers)