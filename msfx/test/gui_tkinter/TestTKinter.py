#  Copyright (c) 2024 Miquel Sas.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from tkinter import Tk, Label, Entry, Button

def convert_to_fahrenheit():
  # Get the Celsius value from the entry field
  celsius = float(celsius_entry.get())
  # Convert Celsius to Fahrenheit
  fahrenheit = (celsius * 9/5) + 32
  # Update the fahrenheit label with the converted value
  fahrenheit_label.config(text=f"Fahrenheit: {fahrenheit:.2f}")

# Create the main window
window = Tk()
window.title("Celsius to Fahrenheit Converter")

# Create a label for Celsius input
celsius_label = Label(window, text="Enter temperature in Celsius:")
celsius_label.pack()

# Create an entry field for Celsius input
celsius_entry = Entry(window)
celsius_entry.pack()

# Create a button to trigger the conversion
convert_button = Button(window, text="Convert", command=convert_to_fahrenheit)
convert_button.pack()

# Create a label to display the Fahrenheit value
fahrenheit_label = Label(window, text="Fahrenheit:")
fahrenheit_label.pack()

# Run the main loop to keep the window open
window.mainloop()
