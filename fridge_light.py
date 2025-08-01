import cv2
import pyttsx3
import time
import json
import os
import numpy as np

# Setup
engine = pyttsx3.init()
limit = 5
roasts = [
    "The fridge light says hello... again!",
    "You're addicted to glowing food boxes.",
    "Even the fridge is like, 'not again!'",
    "Bright idea? Nope, just snacks.",
    "That's your 6th visit today, champ!"
]
count_file = "open_count.json"

# Load count
if os.path.exists(count_file):
    with open(count_file, "r") as file:
        open_count = json.load(file).get("count", 0)
else:
    open_count = 0

def save_count(count):
    with open(count_file, "w") as file:
        json.dump({"count": count}, file)

def roast():
    for r in roasts:
        engine.say(r)
    engine.runAndWait()

# Webcam setup
cap = cv2.VideoCapture(0)
time.sleep(2)  # let camera adjust

print("🔦 Watching for fridge light... Press 'q' to quit.")

prev_brightness = None
threshold = 50  # How much brightness jump to consider as "fridge opened"

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calculate average brightness
    brightness = np.mean(gray)

    if prev_brightness is not None:
        change = brightness - prev_brightness
        if change > threshold:
            open_count += 1
            print(f"💡 Fridge light detected! Count: {open_count}")
            save_count(open_count)
            time.sleep(3)  # prevent double count

            if open_count > limit:
                roast()

    prev_brightness = brightness

    # Show live feed (optional)
    cv2.imshow("Fridge Light Watch", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
