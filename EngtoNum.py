class EnglishToArabicFA:
    def __init__(self):
        # Define states of the automaton
        self.states = {
            "START": self.start_state,
            "UNITS": self.units_state,
            "TENS": self.tens_state,
            "HUNDREDS": self.hundreds_state,
            "THOUSANDS": self.thousands_state,
            "FINAL": self.final_state
        }
        
        # Initialize state and accumulators
        self.reset()
        
        # Word-to-value mapping
        self.word_to_value = {
            "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
            "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
            "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
            "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
            "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
            "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90,
            "hundred": 100, "thousand": 1000
        }
    
    def reset(self):
        """Reset the automaton state and accumulators."""
        self.current_state = "START"
        self.result = 0
        self.current_group = 0  # For numbers within the current thousand group
        self.temp_value = 0     # For temporary calculations
    
    def process_word(self, word):
        """Process a single word through the automaton."""
        if word.lower() not in self.word_to_value:
            raise ValueError(f"Invalid input word: {word}")
        
        value = self.word_to_value[word.lower()]
        self.states[self.current_state](value)
    
    def start_state(self, value):
        """Initial state that routes to appropriate next state."""
        if value in range(1, 10):  # Units (1-9)
            self.temp_value = value
            self.current_state = "UNITS"
        elif value in range(10, 100):  # Tens/teens (10-99)
            self.temp_value = value
            self.current_state = "TENS"
        else:
            raise ValueError(f"Invalid start number: {value}")
    
    def units_state(self, value):
        """Handle unit values and transitions."""
        if value == 100:
            self.temp_value *= value
            self.current_state = "HUNDREDS"
        elif value == 1000:
            self.current_group += self.temp_value
            self.result += self.current_group * value
            self.current_group = 0
            self.temp_value = 0
            self.current_state = "THOUSANDS"
        else:
            raise ValueError(f"Invalid transition from UNITS state: {value}")
    
    def tens_state(self, value):
        """Handle tens values and transitions."""
        if value == 100:
            self.temp_value *= value
            self.current_state = "HUNDREDS"
        elif value == 1000:
            self.current_group += self.temp_value
            self.result += self.current_group * value
            self.current_group = 0
            self.temp_value = 0
            self.current_state = "THOUSANDS"
        elif value < 10:  # Adding units to tens
            self.temp_value += value
            self.current_state = "FINAL"
        else:
            raise ValueError(f"Invalid transition from TENS state: {value}")
    
    def hundreds_state(self, value):
        """Handle hundreds values and transitions."""
        if value == 1000:
            self.current_group += self.temp_value
            self.result += self.current_group * value
            self.current_group = 0
            self.temp_value = 0
            self.current_state = "THOUSANDS"
        elif value in range(1, 10) or value in range(10, 100):  # Adding units or tens after hundred
            self.current_group += self.temp_value
            self.temp_value = value
            self.current_state = "TENS" if value >= 10 else "UNITS"
        else:
            raise ValueError(f"Invalid transition from HUNDREDS state: {value}")
    
    def thousands_state(self, value):
        """Handle values after thousands."""
        if value in range(1, 10):  # Units after thousand
            self.temp_value = value
            self.current_state = "UNITS"
        elif value in range(10, 100):  # Tens after thousand
            self.temp_value = value
            self.current_state = "TENS"
        else:
            raise ValueError(f"Invalid transition from THOUSANDS state: {value}")
    
    def final_state(self, value=None):
        """Accumulate values in the current group."""
        self.current_group += self.temp_value
        self.temp_value = 0
    
    def finalize(self):
        """Return final converted number."""
        if self.temp_value > 0:
            self.current_group += self.temp_value
        if self.current_group > 0:
            self.result += self.current_group
        return self.result

def convert_to_arabic_numerals(sentence):
    """Convert an English number phrase to Arabic numerals."""
    fa = EnglishToArabicFA()
    words = sentence.lower().split()
    
    for word in words:
        fa.process_word(word)
    
    return fa.finalize()