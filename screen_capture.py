"""
Screen capture module - uses mss for fast, low-overhead screenshots.
"""

import io

import mss
import mss.tools


def capture_screen() -> bytes:
    """
    Capture the primary monitor and return the image as PNG bytes in memory.
    No file is written to disk.
    """
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Primary monitor
        screenshot = sct.grab(monitor)
        png_bytes = mss.tools.to_png(screenshot.rgb, screenshot.size)
    return png_bytes
