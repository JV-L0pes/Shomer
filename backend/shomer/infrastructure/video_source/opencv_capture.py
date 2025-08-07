"""Implementação de IVideoSource usando OpenCV em thread separada."""

import threading

import cv2

from shomer.domain.ports.video_source import IVideoSource


class OpenCVVideoSource(IVideoSource, threading.Thread):
    """Captura contínua de vídeo (webcam ou IP) em background thread."""

    def __init__(self, src):
        threading.Thread.__init__(self, daemon=True)
        self.src = src
        backend = (
            cv2.CAP_DSHOW
            if isinstance(src, int) or str(src).isdigit()
            else cv2.CAP_FFMPEG
        )
        self.cap = cv2.VideoCapture(src, backend)
        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open source {src}")
        # Mantém buffer mínimo
        try:
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        except Exception:
            # nem todos backends suportam buffersize
            pass

        self.lock = threading.Lock()
        self.frame = None
        self.running = True
        self.start()

    def run(self):
        """Loop de captura que sempre grava o último frame."""
        while self.running:
            ret, frm = self.cap.read()
            if not ret:
                continue
            with self.lock:
                self.frame = frm

    def read_frame(self):
        """Retorna o frame mais recente ou None."""
        with self.lock:
            return self.frame.copy() if self.frame is not None else None

    def close(self):
        """Para a thread e libera recursos."""
        self.running = False
        self.cap.release()
