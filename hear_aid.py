import speech_recognition as sr
import tkinter as tk
from PIL import Image, ImageTk
import urllib.request
import io
import time
import threading

# ASL letter image URLs
asl_images = {
    letter: f"https://www.lifeprint.com/asl101/fingerspelling/abc-gifs/{letter.lower()}.gif"
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
}

# Setup GUI window
root = tk.Tk()
root.title("Live ASL Translator")
root.geometry("800x600")
label = tk.Label(root)
label.pack(pady=30)

status = tk.Label(root, text="Listening...", font=("Helvetica", 16))
status.pack()

def show_asl_sequence(text):
    words = text.split()
    for word in words:
        images = []
        for char in word:
            if char.isalpha():
                url = asl_images.get(char.upper())
                try:
                    with urllib.request.urlopen(url) as u:
                        raw_data = u.read()
                    im = Image.open(io.BytesIO(raw_data)).resize((100, 100))
                    photo = ImageTk.PhotoImage(im)
                    images.append(photo)
                except:
                    continue

        # Display all letters of the word side by side
        if images:
            canvas = tk.Frame(root)
            canvas.pack()
            for img in images:
                img_label = tk.Label(canvas, image=img)
                img_label.image = img  # Keep a reference
                img_label.pack(side=tk.LEFT, padx=5)
            status.config(text=f"Word: {word.upper()}")
            root.update()
            time.sleep(1.3)

            # Clear the images
            canvas.destroy()

    status.config(text="Listening...")

def listen_and_display():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)

    while True:
        try:
            with mic as source:
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
                text = recognizer.recognize_google(audio)
                print("Heard:", text)
                show_asl_sequence(text.upper())
        except sr.WaitTimeoutError:
            continue
        except sr.UnknownValueError:
            status.config(text="Could not understand")
            root.update()
            time.sleep(0.6)
        except sr.RequestError:
            status.config(text="API error")
            root.update()
            time.sleep(0.6)

# Run in background thread
threading.Thread(target=listen_and_display, daemon=True).start()

# Start GUI loop
root.mainloop()
