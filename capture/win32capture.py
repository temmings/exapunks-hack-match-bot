import win32gui
import win32ui
from ctypes import windll

from PIL import Image

from capture.capture import Capture
from capture.window_size import WindowSize


class Win32Capture(Capture):
    WINDOW_HEADER_PX = 23
    WINDOW_BORDER_PX = 3

    def __init__(self, name: str):
        self.__name = name
        self.__image = self.__window(self.__name)

    @property
    def window_size(self):
        if (self.__image.width, self.__image.height) < WindowSize.FULL_HD:
            return WindowSize.HD_PLUS
        return WindowSize.FULL_HD

    def crop(self, rect) -> Image:
        """
        :param rect: (x0, y0, x1, y1)
        """
        return self.__window(self.__name).crop(rect)

    @staticmethod
    def __window(name: str) -> Image:
        """
        reference: https://stackoverflow.com/questions/19695214/python-screenshot-of-inactive-window-printwindow-win32gui
        """
        hwnd = win32gui.FindWindow(None, name)
        if not hwnd:
            raise Exception("can't found window: [{}]".format(name))

        save_bit_map = win32ui.CreateBitmap()
        # Change the line below depending on whether you want the whole window
        # or just the client area.
        # left, top, right, bottom = win32gui.GetClientRect(hwnd)
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        w = right - left
        h = bottom - top
        hwnd_dc = win32gui.GetWindowDC(hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_bit_map.CreateCompatibleBitmap(mfc_dc, w, h)

        save_dc = mfc_dc.CreateCompatibleDC()
        save_dc.SelectObject(save_bit_map)

        # Change the line below depending on whether you want the whole window
        # or just the client area.
        # result = windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 1) == 1
        print_window_result = windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 0) == 1

        bmp_info = save_bit_map.GetInfo()
        bmp_str = save_bit_map.GetBitmapBits(True)

        im = Image.frombuffer(
            'RGB',
            (bmp_info['bmWidth'], bmp_info['bmHeight']),
            bmp_str, 'raw', 'BGRX', 0, 1)

        win32gui.DeleteObject(save_bit_map.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwnd_dc)

        if not print_window_result:
            raise Exception("can't get window image: [{}]".format(name))

        return im
