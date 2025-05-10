from PyQt5.QtCore import QTimer

class CursorManager:
    def __init__(self, buttons, suggestion_buttons, update_text_callback):
        self.buttons = buttons
        self.suggestion_buttons = suggestion_buttons
        self.update_text_callback = update_text_callback
        self.row_index = 0
        self.col_index = 0
        self.mode = "row"  # First select a row, then a column
        self.scanning_area = "keyboard"  # Track which area is being scanned
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.move_cursor)
        self.timer.start(1500)  # Move every 2 seconds
        self.highlight_button()
        self.paused = False
        self.pause_timer = QTimer()
        self.pause_timer.setSingleShot(True)
        self.pause_timer.timeout.connect(self.resume_scanning)

    def move_cursor(self):
        if self.paused:
            return
            
        print(f"Cursor moving: area {self.scanning_area}, row {self.row_index}, col {self.col_index}, mode {self.mode}")  # Debugging line
        
        if self.scanning_area == "keyboard":
            if self.mode == "row":
                self.row_index = (self.row_index + 1) % len(self.buttons)  # Cycle through rows (Q -> A -> Z)
            else:
                self.col_index = (self.col_index + 1) % len(self.buttons[self.row_index])  # Cycle through row letters
        elif self.scanning_area == "suggestions":
            # Cycle through suggestion buttons
            self.col_index = (self.col_index + 1) % len(self.suggestion_buttons)
        
        self.highlight_button()

    def highlight_button(self):
        # Reset all button styles first
        for row in self.buttons:
            for button in row:
                button.setStyleSheet("")
        
        for button in self.suggestion_buttons:
            button.setStyleSheet("""
                background-color: #3498db;
                color: white;
                padding: 10px;
                font-size: 16px;
            """)
        
        # Highlight based on current scanning area
        if self.scanning_area == "keyboard":
            for row_idx, row in enumerate(self.buttons):
                for col_idx, button in enumerate(row):
                    if self.mode == "row" and col_idx == 0 and row_idx == self.row_index:
                        button.setStyleSheet("background-color: yellow;")  # Highlight first button of row
                    elif self.mode == "column" and row_idx == self.row_index and col_idx == self.col_index:
                        button.setStyleSheet("background-color: green;")  # Highlight selected column
        else:  # suggestions area
            self.suggestion_buttons[self.col_index].setStyleSheet("""
                background-color: purple;
                color: white;
                padding: 10px;
                font-size: 16px;
            """)

    def blink_detected(self):
        print(f"Blink detected! Area: {self.scanning_area}, Mode: {self.mode}")  # Debugging line
        
        # Pause scanning temporarily after a blink
        self.paused = True
        
        if self.scanning_area == "keyboard":
            if self.mode == "row":
                self.mode = "column"  # Switch to column mode after selecting row
                self.col_index = 0  # Reset column to first button
            else:
                letter = self.buttons[self.row_index][self.col_index].text()
                self.update_text_callback(letter)  # Add the letter to the generated text
                self.mode = "row"  # Reset to row selection mode
        elif self.scanning_area == "suggestions":
            # In suggestion buttons mode
            suggested_word = self.suggestion_buttons[self.col_index].text()
            if suggested_word:
                self.update_text_callback(suggested_word)
                # Switch back to keyboard scanning
                self.scanning_area = "keyboard"
                self.mode = "row"
                self.row_index = 0
                self.col_index = 0
        
        self.highlight_button()
        
        # Resume scanning after a pause (3 seconds)
        self.pause_timer.start(3000)
    
    def start_suggestion_scanning(self):
        """
        Method to start scanning suggestion buttons when suggestions are available
        """
        print("Starting suggestion scanning")  # Debugging line
        self.scanning_area = "suggestions"
        self.col_index = 0
        self.highlight_button()
    
    def resume_scanning(self):
        self.paused = False
        print("Scanning resumed")  # Debugging line