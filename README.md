# AI Charades Bot
An AI-powered bot that plays charades in real-time by capturing live webcam feeds, processing the frames, and utilizing Google's Gemini vision capabilities to guess the actions on screen.

Prerequisites
Before you begin, ensure you have the following installed:

Python 3.8+ * A working webcam

Installation & Setup
1. Clone the repository and navigate to the project folder:

```Bash
git clone <your-repo-url>
cd <your-project-folder>
```

2. Create a virtual environment:
It is highly recommended to use a virtual environment to keep dependencies isolated.

```Bash
# Create the virtual environment
python -m venv .venv
```

# Activate the virtual environment (Windows)
```
venv\Scripts\activate
```
# Activate the virtual environment (macOS/Linux)
```
source venv/bin/activate
```
3. Install the dependencies:
With your virtual environment active, install the required libraries (including OpenCV and the Gemini SDK):

```Bash
pip install -r requirements.txt
```
# Configuration
This project requires a Gemini API key to process the video frames. Do not hardcode your API key into the script.

Create a new file in the root directory and name it .env.

Add your API key to this file like so:

```
GEMINI_API_KEY="your_actual_api_key_here"
```
(Note: Ensure that .env is added to your .gitignore file so it is not pushed to public repositories).

# Usage
To start the bot and open the live camera feed, run the main Python script from your terminal:

```Bash
python main.py
```
# Controls:
- Use a _thumbs down_ gesture to start a round
- Use a _thumbs up_ gesture to close the application.
