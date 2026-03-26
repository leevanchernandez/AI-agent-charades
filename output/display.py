import cv2

class Display:
    # Initialize the display window
    def __init__(self, window_name="Agent Charades - Live Feed"):
        # window_name is the name of the window that will be displayed
        self.window_name = window_name

    # Display the frame with the AI's guess
    def showFrame(self, raw_frame, current_guess="Waiting for game to start..."):
        """Displays the live webcam feed with the AI's guess written on it."""
        
        # Overlay the text onto the video frame
        # Parameters: image, text, bottom-left corner, font, scale, color (BGR), thickness
        cv2.putText(raw_frame, f"AI Guess: {current_guess}", (20, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Pop open the window
        cv2.imshow(self.window_name, raw_frame)
        
        # OpenCV needs this tiny pause to actually draw the window on your screen
        # It also checks if you press Esc to quit
        if cv2.waitKey(1) & 0xFF == 27:
            return False # Signal to stop the game
            
        return True # Signal to keep going

    def close(self):
        """Closes the video window."""
        cv2.destroyAllWindows()