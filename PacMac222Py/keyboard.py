import tkinter as tk

class Keyboard:
    def __init__(self, root):
        self.pressed_keys = set()
        root.bind('<KeyPress>', self._on_key_press)
        root.bind('<KeyRelease>', self._on_key_release)
    
    def _on_key_press(self, event):
        self.pressed_keys.add(event.keysym.lower())
    
    def _on_key_release(self, event):
        self.pressed_keys.discard(event.keysym.lower())
    
    def is_pressed(self, key):
        return key.lower() in self.pressed_keys

# Global instance
_keyboard_instance = None

def initialize(root):
    """ Call this function from the module where Tkinter root is created. """
    global _keyboard_instance
    _keyboard_instance = Keyboard(root)

def is_pressed(key):
    """ Mimics keyboard.is_pressed() behavior. """
    return _keyboard_instance.is_pressed(key) if _keyboard_instance else False
