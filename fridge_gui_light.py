import tkinter as tk
import threading
import pyttsx3
import json
import os
import cv2
import time
import numpy as np

# ==== Setup ====
engine = pyttsx3.init()
limit = 5
count_file = "open_count.json"
roasts = [
    "You again?",
    "Do you really need to open it?",
    "Even the fridge is bored!",
    "Let the poor thing rest.",
    "Step away from the snacks!"
]

# ==== Load/Save Counter ====
def load_count():
    if os.path.exists(count_file):
        with open(count_file, "r") as f:
            return json.load(f).get("count", 0)
    return 0

def save_count(count):
    with open(count_file, "w") as f:
        json.dump({"count": count}, f)

def roast_user():
    for line in roasts:
        engine.say(line)
    engine.runAndWait()

# ==== Counter Logic ====
open_count = load_count()

def update_label():
    counter_label.config(text=f"Fridge opened: {open_count} times")

def open_fridge_manual():
    global open_count
    open_count += 1
    save_count(open_count)
    update_label()
    if open_count > limit:
        roast_user()

def reset_counter():
    global open_count
    open_count = 0
    save_count(open_count)
    update_label()

# ==== Light Detection Thread ====
def detect_light():
    global open_count
    cap = cv2.VideoCapture(0)
    time.sleep(2)

    prev_brightness = None
    threshold = 50  # Adjust if needed

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray)

        if prev_brightness is not None:
            change = brightness - prev_brightness
            if change > threshold:
                open_count += 1
                save_count(open_count)
                update_label()
                print(f"💡 Light detected! Count = {open_count}")
                time.sleep(3)  # Prevent rapid repeats
                if open_count > limit:
                    roast_user()

        prev_brightness = brightness
        cv2.imshow("Webcam Light Detection - Press Q to close", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def start_light_thread():
    t = threading.Thread(target=detect_light)
    t.daemon = True
    t.start()

# ==== GUI Setup ====
root = tk.Tk()
root.title("🧊 Fridge Snitch GUI + Light Detection")
root.geometry("320x250")

counter_label = tk.Label(root, text=f"Fridge opened: {open_count} times", font=("Arial", 14))
counter_label.pack(pady=20)

open_btn = tk.Button(root, text="Open Fridge (Manual)", font=("Arial", 12), command=open_fridge_manual)
open_btn.pack(pady=10)

light_btn = tk.Button(root, text="Start Light Detection (Webcam)", font=("Arial", 11), command=start_light_thread)
light_btn.pack(pady=5)

reset_btn = tk.Button(root, text="Reset Counter", font=("Arial", 10), command=reset_counter)
reset_btn.pack(pady=5)

root.mainloop()
