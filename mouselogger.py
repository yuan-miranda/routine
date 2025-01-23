# I think pynput is not working in 3.13.1
# PS C:\Users\yuane\OneDrive\Documents\vscode\1 OUTDATED REPO\routine> python .\mouselogger.py     
# mouselogger.py is listening
# Unhandled exception in listener callback
# Traceback (most recent call last):
#   File "C:\Users\yuane\AppData\Local\Programs\Python\Python313\Lib\site-packages\pynput\_util\win32.py", line 386, in _handler
#     converted = self._convert(code, msg, lpdata)
#   File "C:\Users\yuane\AppData\Local\Programs\Python\Python313\Lib\site-packages\pynput\_util\win32.py", line 401, in _convert
#     raise NotImplementedError()
# NotImplementedError

# During handling of the above exception, another exception occurred:

# Traceback (most recent call last):
#   File "C:\Users\yuane\AppData\Local\Programs\Python\Python313\Lib\site-packages\pynput\_util\__init__.py", line 229, in inner
#     return f(self, *args, **kwargs)
#   File "C:\Users\yuane\AppData\Local\Programs\Python\Python313\Lib\site-packages\pynput\_util\win32.py", line 390, in _handler
#     self._handle(code, msg, lpdata)
#     ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
# TypeError: '_thread._ThreadHandle' object is not callable

import pynput
import time

idle_duration = 0
left_click_pressed_duration = {}
right_click_pressed_duration = {}
middle_click_pressed_duration = {}

# START x y button
# END x y button duration
# SCROLL x y dx dy
# MOVE x y
# IDLE duration

def handle_click(x, y, button, pressed, click_pressed_duration):
    if pressed:
        click_pressed_duration[button] = {"start": time.time(), "end": 0}
        with open("mouselogger.txt", "a") as f:
            f.write(f"START {x} {y} {button}\n")
    else:
        click_pressed_duration[button]["end"] = float("{:0.2f}".format(time.time() - click_pressed_duration[button]["start"]))
        with open("mouselogger.txt", "a") as f:
            f.write(f"END {x} {y} {button} {click_pressed_duration[button]['end']}\n")

def on_click(x, y, button, pressed):
    global left_click_pressed_duration, right_click_pressed_duration, middle_click_pressed_duration
    reset_idle_timer()

    if button == pynput.mouse.Button.left:
        handle_click(x, y, button, pressed, left_click_pressed_duration)
    elif button == pynput.mouse.Button.right:
        handle_click(x, y, button, pressed, right_click_pressed_duration)
    elif button == pynput.mouse.Button.middle:
        handle_click(x, y, button, pressed, middle_click_pressed_duration)

def on_scroll(x, y, dx, dy):
    reset_idle_timer()
    with open("mouselogger.txt", "a") as f:
        f.write(f"SCROLL {x} {y} {dx} {dy}\n")

def on_move(x, y):
    reset_idle_timer()
    with open("mouselogger.txt", "a") as f:
        f.write(f"MOVE {x} {y}\n")

def start_idle_timer():
    global idle_duration
    idle_duration = time.time()

def end_idle_timer():
    global idle_duration
    idle_duration = float("{:0.2f}".format(time.time() - idle_duration))
    with open("mouselogger.txt", "a") as f:
        f.write(f"IDLE {idle_duration}\n")

def reset_idle_timer():
    end_idle_timer()
    start_idle_timer()

def run():
    time.sleep(3)
    with pynput.mouse.Listener(on_click=on_click, on_scroll=on_scroll, on_move=on_move) as listener:
        print("mouselogger.py is listening")
        start_idle_timer()
        listener.join()

if __name__ == "__main__":
    run()