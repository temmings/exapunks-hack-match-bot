import time
import typing
from enum import Enum

from .controller import Controller
from .win32input import PressKey, ReleaseKey

InputIntervalSecond = typing.NewType('InputIntervalSecond', float)


class KeyCode(Enum):
    """
    reference: msdn.microsoft.com/en-us/library/dd375731
    """
    VK_RETURN = 0x0D
    VK_A = 0x41
    VK_D = 0x44
    VK_J = 0x4A
    VK_K = 0x4B
    VK_S = 0x53
    VK_W = 0x57


class Win32Controller(Controller):
    def __init__(self, interval: InputIntervalSecond):
        self.interval = interval

    def start(self):
        self.__press_key(KeyCode.VK_RETURN)

    def left(self):
        self.__press_key(KeyCode.VK_A)

    def right(self):
        self.__press_key(KeyCode.VK_D)

    def grab(self):
        self.__press_key(KeyCode.VK_J)

    def throw(self):
        self.__press_key(KeyCode.VK_J)

    def swap(self):
        self.__press_key(KeyCode.VK_K)

    def __press_key(self, code: KeyCode):
        PressKey(code.value)
        time.sleep(self.interval)
        ReleaseKey(code.value)
        time.sleep(self.interval)
