# Tracks keyboard and mouse activity and provides a simple interface for sharing state
from pynput import keyboard, mouse
import threading
import time

class ActivityMonitor:
    def __init__(self, idle_threshold=60):
        self.last_activity = time.time()
        self.idle_threshold = idle_threshold
        self.active = True
        self.listener_kb = keyboard.Listener(on_press=self.on_activity)
        self.listener_mouse = mouse.Listener(on_move=self.on_activity, on_click=self.on_activity, on_scroll=self.on_activity)

    def on_activity(self, *args, **kwargs):
        self.last_activity = time.time()

    def start(self):
        self.listener_kb.start()
        self.listener_mouse.start()
        threading.Thread(target=self.monitor_loop, daemon=True).start()

    def monitor_loop(self):
        while self.active:
            time.sleep(1)

    def get_idle_time(self):
        return time.time() - self.last_activity

    def stop(self):
        self.active = False
        self.listener_kb.stop()
        self.listener_mouse.stop()
