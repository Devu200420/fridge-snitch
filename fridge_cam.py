import cv2
import pyttsx3
import time
import json
import os

# Setup
engine = pyttsx3.init()
roasts = [
    "Caught you again!",
    "You opened the fridge one more time!",
    "You're not even hungry, are you?",
    "Bro, even the fridge needs a break.",
    "Seriously? You just looked a second ago."
]
limit = 5
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

# Webcam Setup
cap = cv2.VideoCapture(0)
time.sleep(2)  # wait for camera to stabilize

print("🔍 Watching for motion... Press 'q' to quit.")

ret, frame1 = cap.read()
gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)

while True:
    ret, frame2 = cap.read()
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)

    # Difference between frames
    delta = cv2.absdiff(gray1, gray2)
    thresh = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
    motion_score = thresh.sum() / 255

    # Show video feed
    cv2.imshow("Fridge Watch", frame2)

    if motion_score > 5000:  # adjust sensitivity
        open_count += 1
        print(f"🚪 Fridge opened {open_count} times!")
        save_count(open_count)
        time.sleep(3)  # avoid multiple counts for one motion

        if open_count > limit:
            roast()

    gray1 = gray2

    # Quit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
