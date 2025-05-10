import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QGridLayout, QPushButton, QFrame, QSplitter)
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon
from camera import Camera
from cursor import CursorManager
from word_prediction import WordPredictor
from text_to_speech import TextToSpeech  # New import

class LockedInUI(QWidget):
    def __init__(self):
        super().__init__()

        self.word_predictor = WordPredictor()
        self.text_to_speech = TextToSpeech()  # Initialize Text-to-Speech

        self.setWindowTitle("EyeSpeak - Eye-Controlled Communication")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f7;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel {
                color: #333333;
            }
            QPushButton {
                border-radius: 10px;
                font-weight: bold;
            }
        """)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = QLabel("EyeSpeak")
        header.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        """)
        main_layout.addWidget(header, alignment=Qt.AlignCenter)
        
        # Status indicator
        self.status_label = QLabel("Blink Detection: Active")
        self.status_label.setStyleSheet("""
            background-color: #27ae60;
            color: white;
            padding: 8px;
            border-radius: 5px;
            font-size: 14px;
        """)
        main_layout.addWidget(self.status_label, alignment=Qt.AlignRight)
        
        # Split view for camera and text content
        content_splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Camera feed
        camera_frame = QFrame()
        camera_frame.setFrameShape(QFrame.StyledPanel)
        camera_layout = QVBoxLayout(camera_frame)
        
        camera_header = QLabel("Camera Feed")
        camera_header.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        camera_layout.addWidget(camera_header)
        
        self.camera_label = QLabel()
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setMinimumSize(320, 240)
        self.camera_label.setStyleSheet("""
            background-color: #2c3e50;
            color: white;
            padding: 10px;
            border-radius: 10px;
        """)
        camera_layout.addWidget(self.camera_label)
        
        self.blink_indicator = QLabel("No blink detected")
        self.blink_indicator.setStyleSheet("""
            background-color: #e74c3c;
            color: white;
            padding: 8px;
            border-radius: 5px;
            font-size: 14px;
            margin-top: 10px;
        """)
        camera_layout.addWidget(self.blink_indicator)
        
        # Right panel - Text and keyboard
        text_frame = QFrame()
        text_frame.setFrameShape(QFrame.StyledPanel)
        text_layout = QVBoxLayout(text_frame)
        
        # Generated text area
        text_header = QLabel("Your Message")
        text_header.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        text_layout.addWidget(text_header)
        
        self.generated_text_label = QLabel("")
        self.generated_text_label.setWordWrap(True)
        self.generated_text_label.setMinimumHeight(100)
        self.generated_text_label.setStyleSheet("""
            font-size: 20px;
            padding: 15px;
            background-color: white;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            color: #333333;
        """)
        text_layout.addWidget(self.generated_text_label)
        
        # Word suggestions
        suggestion_header = QLabel("Suggestions")
        suggestion_header.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        text_layout.addWidget(suggestion_header)
        
        suggestions_layout = QHBoxLayout()
        self.suggestion_buttons = []
        
        for i in range(3):
            suggestion = QPushButton("")
            suggestion.setStyleSheet("""
                background-color: #3498db;
                color: white;
                padding: 10px;
                font-size: 16px;
            """)
            suggestions_layout.addWidget(suggestion)
            self.suggestion_buttons.append(suggestion)
        
        for button in self.suggestion_buttons:
            button.clicked.connect(self.apply_suggestion)

        text_layout.addLayout(suggestions_layout)
        
        # Add frames to splitter
        content_splitter.addWidget(camera_frame)
        content_splitter.addWidget(text_frame)
        content_splitter.setSizes([300, 700])
        
        main_layout.addWidget(content_splitter)
        
        # Keyboard section
        keyboard_header = QLabel("Virtual Keyboard")
        keyboard_header.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        main_layout.addWidget(keyboard_header)
        
        keyboard_frame = QFrame()
        keyboard_frame.setStyleSheet("""
            background-color: white;
            border-radius: 15px;
            padding: 10px;
        """)
        keyboard_layout = QVBoxLayout(keyboard_frame)
        
        # Create keyboard grid
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        
        self.keys = [
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '⌫', '␣']
        ]
        
        self.buttons = []
        
        for row_idx, row in enumerate(self.keys):
            btn_row = []
            for col_idx, key in enumerate(row):
                btn = QPushButton(key)
                btn.setFixedSize(65, 65)
                
                # Style based on key type
                if key in ['⌫', '␣']:
                    btn.setStyleSheet("""
                        background-color: #e74c3c;
                        color: white;
                        font-size: 20px;
                        border-radius: 10px;
                    """)
                else:
                    btn.setStyleSheet("""
                        background-color: #3498db;
                        color: white;
                        font-size: 20px;
                        border-radius: 10px;
                    """)
                
                grid_layout.addWidget(btn, row_idx, col_idx)
                btn_row.append(btn)
            self.buttons.append(btn_row)
        
        keyboard_layout.addLayout(grid_layout)
        main_layout.addWidget(keyboard_frame)
        
        # Controls area
        controls_layout = QHBoxLayout()
        
        speed_label = QLabel("Scanning Speed:")
        speed_label.setStyleSheet("font-size: 16px; color: #2c3e50;")
        controls_layout.addWidget(speed_label)
        
        # Create speed buttons with proper connections
        self.speed_slow_btn = QPushButton("Slow (3s)")
        self.speed_slow_btn.setStyleSheet("""
            background-color: #2c3e50;
            color: white;
            padding: 8px 15px;
            border-radius: 5px;
        """)
        self.speed_slow_btn.clicked.connect(self.set_speed_slow)
        controls_layout.addWidget(self.speed_slow_btn)
        
        self.speed_medium_btn = QPushButton("Medium (2s)")
        self.speed_medium_btn.setStyleSheet("""
            background-color: #2c3e50;
            color: white;
            padding: 8px 15px;
            border-radius: 5px;
        """)
        self.speed_medium_btn.clicked.connect(self.set_speed_medium)
        controls_layout.addWidget(self.speed_medium_btn)
        
        self.speed_fast_btn = QPushButton("Fast (1s)")
        self.speed_fast_btn.setStyleSheet("""
            background-color: #2c3e50;
            color: white;
            padding: 8px 15px;
            border-radius: 5px;
        """)
        self.speed_fast_btn.clicked.connect(self.set_speed_fast)
        controls_layout.addWidget(self.speed_fast_btn)
        
        # Add current speed indicator
        self.speed_indicator = QLabel("Current Speed: 2s")
        self.speed_indicator.setStyleSheet("""
            background-color: #3498db;
            color: white;
            padding: 8px 15px;
            border-radius: 5px;
            margin-left: 10px;
        """)
        controls_layout.addWidget(self.speed_indicator)
        
        # Spacer to push buttons to the left
        controls_layout.addStretch(1)
        
        # New buttons: Clear, Speak, and Volume Control
        clear_btn = QPushButton("Clear Text")
        clear_btn.setStyleSheet("""
            background-color: #e74c3c;
            color: white;
            padding: 8px 15px;
            border-radius: 5px;
        """)
        clear_btn.clicked.connect(self.clear_text)
        controls_layout.addWidget(clear_btn)
        
        # Speak Text Button
        speak_btn = QPushButton("Speak Text")
        speak_btn.setStyleSheet("""
            background-color: #2ecc71;
            color: white;
            padding: 8px 15px;
            border-radius: 5px;
        """)
        speak_btn.clicked.connect(self.speak_generated_text)
        controls_layout.addWidget(speak_btn)
        
        # Volume Control Buttons
        volume_down_btn = QPushButton("🔉")  # Volume down symbol
        volume_down_btn.setStyleSheet("""
            background-color: #3498db;
            color: white;
            padding: 8px 15px;
            border-radius: 5px;
        """)
        volume_down_btn.clicked.connect(self.decrease_volume)
        controls_layout.addWidget(volume_down_btn)
        
        volume_up_btn = QPushButton("🔊")  # Volume up symbol
        volume_up_btn.setStyleSheet("""
            background-color: #3498db;
            color: white;
            padding: 8px 15px;
            border-radius: 5px;
        """)
        volume_up_btn.clicked.connect(self.increase_volume)
        controls_layout.addWidget(volume_up_btn)
        
        main_layout.addLayout(controls_layout)
        
        self.setLayout(main_layout)
        
        # Initialize camera and cursor manager
        self.camera = Camera(self.camera_label, self.on_blink_detected)
        self.cursor = CursorManager(self.buttons, self.suggestion_buttons, self.update_generated_text)
        
        # Set medium speed as default (highlighted)
        self.update_speed_buttons("medium")
        
        # Camera timer for updating feed
        self.camera_timer = QTimer()
        self.camera_timer.timeout.connect(self.update_camera_feed)
        self.camera_timer.start(30)  # Update at 30ms intervals for smooth video
        
        # Word suggestion placeholders (would be replaced with actual algorithm)
        self.suggestion_buttons[0].setText("Hello")
        self.suggestion_buttons[1].setText("Thank you")
        self.suggestion_buttons[2].setText("I need")

    def speak_generated_text(self):
        """Convert generated text to speech"""
        text = self.generated_text_label.text().strip()
        if text:
            self.text_to_speech.speak(text)
    
    def increase_volume(self):
        """Increase speech volume"""
        current_volume = self.text_to_speech.engine.getProperty('volume')
        new_volume = min(1.0, current_volume + 0.1)
        self.text_to_speech.set_volume(new_volume)
        print(f"Volume increased to {new_volume:.1f}")
    
    def decrease_volume(self):
        """Decrease speech volume"""
        current_volume = self.text_to_speech.engine.getProperty('volume')
        new_volume = max(0.0, current_volume - 0.1)
        self.text_to_speech.set_volume(new_volume)
        print(f"Volume decreased to {new_volume:.1f}")

    def update_camera_feed(self):
        frame = self.camera.get_frame()
        if frame:
            self.camera_label.setPixmap(frame)

    def update_generated_text(self, letter):
        current_text = self.generated_text_label.text()
        if letter == "⌫":
            current_text = current_text[:-1]
        elif letter == "␣":
            current_text += " "
        else:
            current_text += letter
        self.generated_text_label.setText(current_text)
        
        # Visual feedback for selection
        self.blink_indicator.setText("Blink detected!")
        self.blink_indicator.setStyleSheet("""
            background-color: #27ae60;
            color: white;
            padding: 8px;
            border-radius: 5px;
            font-size: 14px;
        """)
        
        # Reset after 1 second
        QTimer.singleShot(1000, self.reset_blink_indicator)
        
        # Update suggestions (placeholder - would be replaced with actual prediction)
        if current_text:
            words = current_text.split(" ")
            last_word = words[-1] if words else ""
            
            # Simple placeholder suggestions
            if last_word:
                self.update_suggestions(last_word)

    def update_suggestions(self, current_text):
        if current_text:
            words = current_text.split(" ")
            last_word = words[-1] if words else ""

            # Get word completion, next word, and phrase suggestions
            completions, next_words, phrases = self.word_predictor.get_suggestions(last_word)

            # Choose up to 3 suggestions from the available lists
            suggestions = completions + next_words + phrases
            suggestions = suggestions[:3]  # Keep only the top 3 suggestions

            suggestion_available = False
            for i, suggestion in enumerate(self.suggestion_buttons):
                if i < len(suggestions):
                    suggestion.setText(suggestions[i])
                    suggestion.setEnabled(True)
                    suggestion.setStyleSheet("""
                        background-color: #3498db;
                        color: white;
                        padding: 10px;
                        font-size: 16px;
                    """)
                    suggestion_available = True
                else:
                    suggestion.setText("")
                    suggestion.setEnabled(False)
                    suggestion.setStyleSheet("""
                        background-color: #95a5a6;
                        color: white;
                        padding: 10px;
                        font-size: 16px;
                    """)
            
            # If suggestions are available, start suggestion scanning
            if suggestion_available:
                self.cursor.start_suggestion_scanning()
                
    def reset_blink_indicator(self):
        self.blink_indicator.setText("Waiting for blink...")
        self.blink_indicator.setStyleSheet("""
            background-color: #3498db;
            color: white;
            padding: 8px;
            border-radius: 5px;
            font-size: 14px;
        """)

    def on_blink_detected(self):
        self.cursor.blink_detected()
        
    def clear_text(self):
        self.generated_text_label.setText("")
        
    # Speed control methods
    def set_speed_slow(self):
        self.cursor.timer.stop()
        self.cursor.timer.start(3000)  # 3 seconds
        self.update_speed_buttons("slow")
        self.speed_indicator.setText("Current Speed: 3s")
        print("Speed changed to slow (3s)")
        
    def set_speed_medium(self):
        self.cursor.timer.stop()
        self.cursor.timer.start(2000)  # 2 seconds
        self.update_speed_buttons("medium")
        self.speed_indicator.setText("Current Speed: 2s")
        print("Speed changed to medium (2s)")
        
    def set_speed_fast(self):
        self.cursor.timer.stop()
        self.cursor.timer.start(1000)  # 1 second
        self.update_speed_buttons("fast")
        self.speed_indicator.setText("Current Speed: 1s")
        print("Speed changed to fast (1s)")
        
    def update_speed_buttons(self, active):
        # Reset all button styles
        base_style = """
            background-color: #2c3e50;
            color: white;
            padding: 8px 15px;
            border-radius: 5px;
        """
        
        active_style = """
            background-color: #27ae60;
            color: white;
            padding: 8px 15px;
            border-radius: 5px;
            font-weight: bold;
        """
        
        self.speed_slow_btn.setStyleSheet(base_style)
        self.speed_medium_btn.setStyleSheet(base_style)
        self.speed_fast_btn.setStyleSheet(base_style)
        
        # Highlight active button
        if active == "slow":
            self.speed_slow_btn.setStyleSheet(active_style)
        elif active == "medium":
            self.speed_medium_btn.setStyleSheet(active_style)
        elif active == "fast":
            self.speed_fast_btn.setStyleSheet(active_style)

    def apply_suggestion(self):
        sender = self.sender()  # Get the button that was clicked
        suggested_word = sender.text()
        
        if suggested_word:
            current_text = self.generated_text_label.text()
            
            # Check if there's text and if the last character isn't a space
            if current_text and not current_text.endswith(" "):
                # Find the last word boundary
                last_space_index = current_text.rfind(" ")
                
                if last_space_index == -1:  # No space found, this is the first word
                    # Replace the entire text with the suggestion
                    new_text = suggested_word
                else:
                    # Keep everything up to the last space and replace the partial word
                    new_text = current_text[:last_space_index+1] + suggested_word
            else:
                # If text ends with space or is empty, just append the new word
                new_text = current_text + suggested_word
            
            # Update the text and add a space after the suggestion
            if not new_text.endswith(" "):
                new_text += " "
            
            self.generated_text_label.setText(new_text)
            self.update_suggestions(new_text)
            
    def closeEvent(self, event):
        self.camera.release_camera()
        self.camera_timer.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LockedInUI()
    window.show()
    sys.exit(app.exec_())