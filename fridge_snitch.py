import cv2
import tkinter as tk
import time
import os
from datetime import datetime
import pyttsx3
from PIL import Image, ImageTk  # 👈 NEW for image display

# Create folder to save photos
if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

# Roast messages
roasts = [
    "Roast: Again? You’re not hungry, you’re bored!",
    "Roast: The fridge is not your therapist!",
    "Roast: Just shut the door already, midnight muncher!",
    "Roast: That snack won’t fix your GPA!",
    "Roast: Find a hobby that isn’t in the fridge!"
]

# Text-to-speech
engine = pyttsx3.init()
engine.setProperty('rate', 160)

# Counter
open_count = 0

# Tkinter GUI
root = tk.Tk()
root.title("Fridge Snitch 👀")
root.geometry("600x600")

label_status = tk.Label(root, text="Monitoring fridge...", font=("Arial", 16), wraplength=550)
label_status.pack(pady=10)

label_count = tk.Label(root, text="Fridge Opens: 0", font=("Arial", 14))
label_count.pack()

# Placeholder image label
image_label = tk.Label(root)
image_label.pack(pady=10)

# Function: speak aloud
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function: capture and show image
def capture_image(frame):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"screenshots/fridge_open_{timestamp}.png"
    cv2.imwrite(filename, frame)
    print(f"Saved photo: {filename}")

    # Display in GUI
    img = Image.open(filename)
    img = img.resize((300, 250))  # Resize to fit GUI
    img_tk = ImageTk.PhotoImage(img)

    image_label.config(image=img_tk)
    image_label.image = img_tk  # Keep a reference!

# Main loop
def detect_brightness():
    global open_count
    cap = cv2.VideoCapture(0)
    time.sleep(2)

    while True:
        ret, frame = cap.read()
        if not ret:
            label_status.config(text="❌ Camera not available!")
            break

        brightness = frame.mean()
        print("Brightness:", brightness)

        if brightness > 120:
            open_count += 1
            roast = roasts[open_count % len(roasts)]
            label_status.config(text=roast)
            label_count.config(text=f"Fridge Opens: {open_count}")
            capture_image(frame)
            speak(roast)
            root.update()
            time.sleep(3)
        else:
            label_status.config(text="Monitoring fridge...")
            root.update()

        time.sleep(1)

    cap.release()

# Start loop after 100ms
root.after(100, detect_brightness)
root.mainloop()
