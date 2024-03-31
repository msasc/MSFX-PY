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

from tkinter import Tk, Label, Frame, BOTH, ttk, Button
import time

def simulate_process():
    # Get reference to progress bar
    progress_bar = progress_var.get()

    # Simulate a process that takes 20 seconds
    for i in range(20):
        time.sleep(1)
        # Update progress bar value
        progress_bar['value'] = i + 1
    window.update()  # Update UI for smooth progress bar animation

# Create the main window
window = Tk()
window.title("Process Monitor")

# Create the content frame
content_frame = Frame(window)
content_frame.pack(fill=BOTH, expand=True)  # Corrected fill attribute

# Create a label to display some content
content_label = Label(content_frame, text="This is some content while the process runs.")
content_label.pack()

# Create the progress bar frame
progress_bar_frame = Frame(window)
progress_bar_frame.pack(fill=BOTH)  # Corrected fill attribute

# Create a progress bar with maximum value of 20
progress_var = ttk.Progressbar(progress_bar_frame, orient="horizontal", mode="determinate", maximum=20)
progress_var.pack(padx=5, pady=5)

# Button to trigger the process simulation
start_button = Button(content_frame, text="Start Process", command=simulate_process)
start_button.pack()

# Run the main loop
window.mainloop()
