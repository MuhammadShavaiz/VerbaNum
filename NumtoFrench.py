class ArabicToFrenchFA:
    def __init__(self):
        # Initialize mappings for French numbers
        self.units = {
            0: "zéro", 1: "un", 2: "deux", 3: "trois", 4: "quatre",
            5: "cinq", 6: "six", 7: "sept", 8: "huit", 9: "neuf"
        }
        
        self.teens = {
            11: "onze", 12: "douze", 13: "treize", 14: "quatorze",
            15: "quinze", 16: "seize", 17: "dix-sept", 18: "dix-huit",
            19: "dix-neuf"
        }
        
        self.tens = {
            10: "dix", 20: "vingt", 30: "trente", 40: "quarante",
            50: "cinquante", 60: "soixante", 70: "soixante", 
            80: "quatre-vingt", 90: "quatre-vingt"
        }
    
    def convert_hundreds(self, number):
        """Convert hundreds place (100-999)."""
        if number == 0:
            return ""
            
        hundreds_digit = number // 100
        remaining = number % 100
        
        if hundreds_digit == 0:
            return self.convert_tens(remaining)
            
        hundreds = "cent" if hundreds_digit == 1 else f"{self.units[hundreds_digit]}-cent"
        
        if remaining == 0:
            # Add 's' to cent when it's exactly hundreds except for 100
            return f"{hundreds}s" if hundreds_digit > 1 else hundreds
        
        return f"{hundreds} {self.convert_tens(remaining)}"
    
    def convert_tens(self, number):
        """Convert tens place (10-99)."""
        if number < 10:
            return self.units[number]
            
        if number in self.teens:
            return self.teens[number]
            
        tens_digit = (number // 10) * 10
        units_digit = number % 10
        
        # Special cases for 70-79 and 90-99
        if tens_digit == 70 or tens_digit == 90:
            base = self.tens[tens_digit]  # "soixante" or "quatre-vingt"
            if units_digit == 0:
                return f"{base}-dix"
            elif units_digit == 1:
                return f"{base}-onze"
            else:
                return f"{base}-{self.teens[10 + units_digit]}"
        
        # Special case for 80-89
        if tens_digit == 80:
            if units_digit == 0:
                return "quatre-vingts"
            return f"quatre-vingt-{self.units[units_digit]}"
        
        # Regular cases
        if units_digit == 0:
            return self.tens[tens_digit]
        elif units_digit == 1 and tens_digit != 80:
            return f"{self.tens[tens_digit]}-et-un"
        else:
            return f"{self.tens[tens_digit]}-{self.units[units_digit]}"
    
    def convert(self, number):
        """Convert number to French words."""
        if not isinstance(number, int) or number < 0 or number > 999:
            raise ValueError("Number must be an integer between 0 and 999")
        
        if number == 0:
            return self.units[0]
        
        return self.convert_hundreds(number).strip()