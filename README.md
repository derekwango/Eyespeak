# Eyespeak
EyeSpeak is an assistive communication system designed to help individuals with severe mobility impairments communicate using eye blinking patterns. The system captures blinks through a webcam and translates them into letters, enabling users to form words and sentences without physical movement.

#Project Goal
The main objective of EyeSpeak is to provide a low-cost, accessible communication platform for people with motor disabilities by leveraging blink detection and pattern recognition.

# Features
Real-time eye blink detection using a webcam

Blink pattern encoding system (e.g., short and long blinks)

Real-time decoding and character mapping

On-screen display of decoded text

Optional text-to-speech output

Technologies Used
Python

OpenCV (video capture and image processing)

Dlib or Mediapipe (facial and eye landmark detection)

Tkinter or PyQt (graphical user interface)

pyttsx3 (text-to-speech, optional)

# How It Works
The system uses a webcam to continuously capture video of the user's face.

Facial landmarks are used to detect eye states and calculate blink duration.

Short and long blinks are classified based on duration thresholds.

Blinks are interpreted as binary patterns or Morse-like codes to form characters.

Characters are combined into readable text displayed in the UI.

Optionally, the system can vocalize the output text using text-to-speech.

## Project Structure

```text
eyespeak/
├── eyespeak.py          # Main application script
├── blink_detector.py    # Blink detection logic
├── encoder.py           # Blink-to-character conversion
├── gui.py               # User interface code
├── utils.py             # Utility functions
├── requirements.txt
└── README.md

# Future Enhancements
Add predictive text using natural language processing

Allow user-specific blink timing calibration

Support for additional languages and input modes

Integration with IoT devices for accessibility (e.g., alarms, messaging)

# Contributions
Contributions are welcome. Please submit a pull request or open an issue to suggest improvements.

# License
This project is licensed under the MIT License.


