# simulate the keylogger and mouselogger

import pyautogui
import pynput
import time
import threading

def get_key(key):
    key = key.strip("'").split(".")
    if len(key) == 1:
        return pynput.keyboard.KeyCode.from_char(key[0])
    return getattr(pynput.keyboard.Key, key[1])

def keylogger_thread():
    print("running keylogger.txt")
    with open("keylogger.txt", "r") as f:
        for line in f:
            line_parts = line.split()

            if line_parts[0] == "START":
                pynput.keyboard.Controller().press(get_key(line_parts[1]))
            elif line_parts[0] == "END":
                time.sleep(float(line_parts[2]))
                pynput.keyboard.Controller().release(get_key(line_parts[1]))
            elif line_parts[0] == "IDLE":
                time.sleep(float(line_parts[1]))

def mouselogger_thread():
    print("running mouselogger.txt")
    with open("mouselogger.txt", "r") as f:
        for line in f:
            pass

def run():
    time.sleep(3)
    keyboard_thread = threading.Thread(target=keylogger_thread)
    mouse_thread = threading.Thread(target=mouselogger_thread)
    keyboard_thread.start()
    mouse_thread.start()
    keyboard_thread.join()
    mouse_thread.join()

if __name__ == "__main__":
    run()