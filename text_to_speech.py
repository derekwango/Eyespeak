import pyttsx3

class TextToSpeech:
    def __init__(self, rate=150, volume=0.8):
        """
        Initialize Text-to-Speech engine
        
        :param rate: Speech rate (words per minute)
        :param volume: Volume level (0.0 to 1.0)
        """
        try:
            self.engine = pyttsx3.init()
            
            # Set properties
            self.engine.setProperty('rate', rate)
            self.engine.setProperty('volume', volume)
            
            # Optional: Choose a specific voice (optional, depends on system)
            voices = self.engine.getProperty('voices')
            # Uncomment and modify if you want a specific voice
            # self.engine.setProperty('voice', voices[1].id)  # Typically index 1 is a female voice
        except Exception as e:
            print(f"Text-to-Speech initialization error: {e}")
            self.engine = None
    
    def speak(self, text):
        """
        Convert text to speech
        
        :param text: Text to be spoken
        """
        if not self.engine:
            print("Text-to-Speech engine not initialized.")
            return
        
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Speech synthesis error: {e}")
    
    def set_rate(self, rate):
        """
        Change speech rate
        
        :param rate: New speech rate (words per minute)
        """
        if self.engine:
            self.engine.setProperty('rate', rate)
    
    def set_volume(self, volume):
        """
        Change speech volume
        
        :param volume: New volume level (0.0 to 1.0)
        """
        if self.engine:
            self.engine.setProperty('volume', volume)