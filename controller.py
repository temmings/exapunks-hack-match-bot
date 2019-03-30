#!/usr/bin/env python
# coding: utf-8
#
import ctypes
import time
from ctypes import wintypes

# msdn.microsoft.com/en-us/library/dd375731
VK_RETURN = 0x0D
VK_A = 0x41
VK_D = 0x44
VK_J = 0x4A
VK_K = 0x4B
VK_S = 0x53
VK_W = 0x57


class Controller(object):
    @staticmethod
    def start():
        PressKey(VK_RETURN)
        time.sleep(0.01)
        ReleaseKey(VK_RETURN)

    @staticmethod
    def move_left():
        PressKey(VK_A)
        time.sleep(0.01)
        ReleaseKey(VK_A)

    @staticmethod
    def move_right():
        PressKey(VK_D)
        time.sleep(0.01)
        ReleaseKey(VK_D)

    @staticmethod
    def pop():
        PressKey(VK_J)
        time.sleep(0.01)
        ReleaseKey(VK_J)

    @staticmethod
    def push():
        PressKey(VK_J)
        time.sleep(0.01)
        ReleaseKey(VK_J)

    @staticmethod
    def swap():
        PressKey(VK_J)
        time.sleep(0.01)
        ReleaseKey(VK_J)

INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004
KEYEVENTF_SCANCODE = 0x0008

MAPVK_VK_TO_VSC = 0

user32 = ctypes.WinDLL('user32', use_last_error=True)
ULONG_PTR = wintypes.WPARAM


class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx", wintypes.LONG),
                ("dy", wintypes.LONG),
                ("mouseData", wintypes.DWORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", ULONG_PTR))


class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk", wintypes.WORD),
                ("wScan", wintypes.WORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", ULONG_PTR))

    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        # some programs use the scan code even if KEYEVENTF_SCANCODE
        # isn't set in dwFflags, so attempt to map the correct code.
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk,
                                                 MAPVK_VK_TO_VSC, 0)


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg", wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))


class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))

    _anonymous_ = ("_input",)
    _fields_ = (("type", wintypes.DWORD),
                ("_input", _INPUT))


def _check_count(result, func, args):
    if result == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    return args

user32.SendInput.errcheck = _check_count
user32.SendInput.argtypes = (wintypes.UINT,  # nInputs
                             ctypes.POINTER(INPUT),  # pInputs
                             ctypes.c_int)  # cbSize


def PressKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))
