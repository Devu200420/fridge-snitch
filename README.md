# fridge-snitch
A fun motion-detection app that roasts you when you open the fridge

How It Works

1. Webcam is kept on and checks brightness every second
2. When fridge opens (light appears), brightness increases
3. The app:
   - Increments a counter
   - Picks a random roast
   - Speaks it aloud using offline text-to-speech
   - Prints count + roast in terminal

Technologies Used

- `OpenCV` – to access the webcam and get brightness
- pyttsx3` – for text-to-speech (offline)
Demo link:
https://youtu.be/cIpHeEjLJeY

