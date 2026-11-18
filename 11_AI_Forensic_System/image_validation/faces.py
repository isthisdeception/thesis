"""Optional face counter. Tests inject their own counter; this one runs when OpenCV is installed."""

from __future__ import annotations

from PIL import Image


def count_faces_opencv(image: Image.Image) -> int:
    """Count frontal faces with OpenCV's Haar cascade. Raises ImportError if cv2 is absent."""

    import cv2
    import numpy as np

    gray = cv2.cvtColor(np.array(image.convert("RGB")), cv2.COLOR_RGB2GRAY)
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    found = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    return int(len(found))
