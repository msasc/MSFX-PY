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

from tkinter import Tk, Label, Frame, BOTH, StringVar, Button
import time

def simulate_process():
  # Simulate a process that takes 20 seconds
  for i in range(20):
    time.sleep(1)
    # Update status bar text
    status_var.set(f"Simulating process... {i+1}/20")
  status_var.set("Process completed!")

# Create the main window
window = Tk()
window.title("Process Monitor")

# Create the content frame
content_frame = Frame(window)
content_frame.pack(fill=BOTH, expand=True)

# Create a label to display some content
content_label = Label(content_frame, text="This is some content while the process runs.")
content_label.pack()

# Create the status bar frame
status_bar = Frame(window, relief="sunken", bd=1)
status_bar.pack(side="bottom", fill=BOTH)

# Create a string variable to hold the status message
status_var = StringVar()
status_var.set("Waiting for process to start...")

# Create a label for the status bar
status_label = Label(status_bar, textvariable=status_var)
status_label.pack(side="left", padx=5)

# Button to trigger the process simulation
start_button = Button(content_frame, text="Start Process", command=simulate_process)
start_button.pack()

# Run the main loop
window.mainloop()
