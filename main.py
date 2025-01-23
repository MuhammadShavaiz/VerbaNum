import tkinter as tk
from tkinter import messagebox
from EngtoNum import EnglishToArabicFA, convert_to_arabic_numerals
from NumtoFrench import ArabicToFrenchFA

class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("English to French Number Converter")
        self.root.geometry("500x300")

        # Create instances of both converters
        self.english_to_arabic = EnglishToArabicFA()
        self.arabic_to_french = ArabicToFrenchFA()

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        # Label and Input for English number
        self.label = tk.Label(self.root, text="Enter a number in English words (zero - nine hundred ninety nine):")
        self.label.pack(pady=10)

        self.entry = tk.Entry(self.root, width=40)
        self.entry.pack(pady=10)

        # Button to perform the conversion
        self.convert_button = tk.Button(self.root, text="Convert to French", command=self.convert_number)
        self.convert_button.pack(pady=20)

        # Label to display the results
        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack(pady=10)

    def convert_number(self):
        english_input = self.entry.get().strip().lower()

        if english_input == "quit":
            self.root.quit()
            return

        try:
            # Convert English to Arabic numerals
            arabic_number = convert_to_arabic_numerals(english_input)

            # Convert Arabic to French
            french_output = self.arabic_to_french.convert(arabic_number)

            # Display results in the result label
            result_text = f"English: {english_input.capitalize()}\nNumber: {arabic_number}\nFrench: {french_output}"
            self.result_label.config(text=result_text)

        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()
