import re
import os
from collections import Counter
import json

class WordPredictor:
    def __init__(self, custom_phrases_file=None):
        # Dictionary to store word frequencies
        self.word_frequencies = Counter()
        
        # Dictionary to store next word predictions based on current word
        self.next_word_predictions = {}
        
        # List of common phrases
        self.phrases = []
        
        # Load common English words and their frequencies
        self._load_common_words()
        
        # Load custom phrases if provided
        if custom_phrases_file and os.path.exists(custom_phrases_file):
            self._load_custom_phrases(custom_phrases_file)
    
    def _load_common_words(self):
        # This is a simplified list - in practice, you'd want a more comprehensive dataset
        common_words = {
            "the": 100, "be": 99, "to": 98, "of": 97, "and": 96, "a": 95, "in": 94, "that": 93,
            "have": 92, "I": 91, "it": 90, "for": 89, "not": 88, "on": 87, "with": 86, "he": 85,
            "as": 84, "you": 83, "do": 82, "at": 81, "this": 80, "but": 79, "his": 78, "by": 77,
            "from": 76, "they": 75, "we": 74, "say": 73, "her": 72, "she": 71, "or": 70,
            "an": 69, "will": 68, "my": 67, "one": 66, "all": 65, "would": 64, "there": 63,
            "their": 62, "what": 61, "so": 60, "up": 59, "out": 58, "if": 57, "about": 56,
            "who": 55, "get": 54, "which": 53, "go": 52, "me": 51, "when": 50, "make": 49,
            "can": 48, "like": 47, "time": 46, "no": 45, "just": 44, "him": 43, "know": 42,
            "take": 41, "people": 40, "into": 39, "year": 38, "your": 37, "good": 36,
            "some": 35, "could": 34, "them": 33, "see": 32, "other": 31, "than": 30,
            "then": 29, "now": 28, "look": 27, "only": 26, "come": 25, "its": 24,
            "over": 23, "think": 22, "also": 21, "back": 20, "after": 19, "use": 18,
            "two": 17, "how": 16, "our": 15, "work": 14, "first": 13, "well": 12,
            "way": 11, "even": 10, "new": 9, "want": 8, "because": 7, "any": 6,
            "these": 5, "give": 4, "day": 3, "most": 2, "us": 1
        }
        
        # Common word pairs for next word prediction
        common_pairs = {
            "I": ["am", "will", "have", "can", "need", "want", "think", "know"],
            "would": ["like", "you", "be", "have", "need"],
            "thank": ["you", "him", "her", "them"],
            "can": ["you", "I", "we", "they", "help"],
            "please": ["help", "bring", "take", "give", "let", "allow"],
            "need": ["help", "to", "a", "some", "water", "rest"],
            "want": ["to", "a", "some", "you", "help"],
            "how": ["are", "is", "do", "did", "can", "would", "about"],
            "could": ["you", "I", "we", "they", "help", "please"],
            "hello": ["there", "everyone", "world"],
            "good": ["morning", "afternoon", "evening", "night", "day", "job"],
            "feel": ["like", "good", "bad", "sick", "tired", "happy"]
        }
        
        # Load common phrases for accessibility communication
        common_phrases = [
            "I need help",
            "Can you help me",
            "I'm feeling tired",
            "I would like some water",
            "Please adjust my position",
            "Thank you for your help",
            "Can you call the nurse",
            "I need to use the bathroom",
            "I'm uncomfortable",
            "I'm feeling better today",
            "Can you turn on the TV",
            "I would like to rest now",
            "Please open the window",
            "It's too cold in here",
            "It's too hot in here",
            "I'm hungry",
            "I'm thirsty",
            "Good morning",
            "Good night",
            "I love you",
            "I miss you",
            "How are you today",
            "I need my medication"
        ]
        
        # Store word frequencies
        self.word_frequencies.update(common_words)
        
        # Store word pairs for next word prediction
        self.next_word_predictions = common_pairs
        
        # Store common phrases
        self.phrases = common_phrases
    
    def _load_custom_phrases(self, filename):
        try:
            with open(filename, 'r') as file:
                custom_data = json.load(file)
                
                # Add custom word frequencies if present
                if 'word_frequencies' in custom_data:
                    for word, freq in custom_data['word_frequencies'].items():
                        self.word_frequencies[word] = freq
                
                # Add custom next word predictions if present
                if 'next_word_predictions' in custom_data:
                    for word, predictions in custom_data['next_word_predictions'].items():
                        if word in self.next_word_predictions:
                            self.next_word_predictions[word].extend(predictions)
                        else:
                            self.next_word_predictions[word] = predictions
                
                # Add custom phrases if present
                if 'phrases' in custom_data:
                    self.phrases.extend(custom_data['phrases'])
        except Exception as e:
            print(f"Error loading custom phrases: {e}")
    
    def save_custom_data(self, filename):
        """Save learned word frequencies, predictions and phrases to a file"""
        data = {
            'word_frequencies': dict(self.word_frequencies),
            'next_word_predictions': self.next_word_predictions,
            'phrases': self.phrases
        }
        
        try:
            with open(filename, 'w') as file:
                json.dump(data, file, indent=2)
            return True
        except Exception as e:
            print(f"Error saving custom data: {e}")
            return False
    
    def learn_from_text(self, text):
        """Learn word frequencies and patterns from provided text"""
        # Tokenize the text into words
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Update word frequencies
        for word in words:
            self.word_frequencies[word] += 1
        
        # Update next word predictions
        for i in range(len(words) - 1):
            current_word = words[i]
            next_word = words[i + 1]
            
            if current_word not in self.next_word_predictions:
                self.next_word_predictions[current_word] = []
                
            if next_word not in self.next_word_predictions[current_word]:
                self.next_word_predictions[current_word].append(next_word)
    
    def add_phrase(self, phrase):
        """Add a new phrase to the suggestions"""
        if phrase and phrase not in self.phrases:
            self.phrases.append(phrase)
            # Also learn from this phrase
            self.learn_from_text(phrase)
    
    def get_word_completions(self, partial_word, max_suggestions=3):
        """Get word completion suggestions and return only the missing portion."""
        if not partial_word:
            return []
        
        partial_word = partial_word.lower()
        suggestions = []
        
        for word in self.word_frequencies:
            if word.startswith(partial_word) and word != partial_word:
                suggestions.append((word, self.word_frequencies[word]))
        
        suggestions.sort(key=lambda x: x[1], reverse=True)
        
        # Return only the missing part of the word to avoid duplication
        return [word[len(partial_word):] for word, _ in suggestions[:max_suggestions]]
    
    def get_next_word_suggestions(self, current_word, max_suggestions=3):
        """Get suggestions for the next word based on the current word"""
        if not current_word:
            # Return most common words if no current word
            most_common = self.word_frequencies.most_common(max_suggestions)
            return [word for word, _ in most_common]
            
        current_word = current_word.lower()
        
        if current_word in self.next_word_predictions:
            # If we have specific predictions for this word, return those
            suggestions = self.next_word_predictions[current_word]
            return suggestions[:max_suggestions]
        else:
            # Otherwise return most common words
            most_common = self.word_frequencies.most_common(max_suggestions)
            return [word for word, _ in most_common]
    
    def get_phrase_suggestions(self, partial_text, max_suggestions=3):
        """Get phrase suggestions based on partial text"""
        if not partial_text:
            # Return some default phrases if no text
            return self.phrases[:max_suggestions]
            
        partial_text = partial_text.lower()
        
        # Find phrases that start with the partial text
        matching_phrases = []
        for phrase in self.phrases:
            if phrase.lower().startswith(partial_text):
                matching_phrases.append(phrase)
                
        # If we don't have enough matches, add phrases that contain the partial text
        if len(matching_phrases) < max_suggestions:
            for phrase in self.phrases:
                if partial_text in phrase.lower() and phrase not in matching_phrases:
                    matching_phrases.append(phrase)
                    if len(matching_phrases) >= max_suggestions:
                        break
        
        return matching_phrases[:max_suggestions]
    
    def get_suggestions(self, text, max_suggestions=3):
        """Get combined suggestions based on current text"""
        if not text:
            return [], [], []
            
        # Split text into words
        words = text.split()
        
        # Handle word completion for the last word
        word_completions = []
        if words and not text.endswith(" "):
            partial_word = words[-1]
            word_completions = self.get_word_completions(partial_word, max_suggestions)
        
        # Handle next word suggestions
        next_word_suggestions = []
        if not words or text.endswith(" "):
            # Suggest based on the last word if text ends with space
            last_word = words[-1] if words else ""
            next_word_suggestions = self.get_next_word_suggestions(last_word, max_suggestions)
        
        # Get phrase suggestions
        phrase_suggestions = self.get_phrase_suggestions(text, max_suggestions)
        
        return word_completions, next_word_suggestions, phrase_suggestions