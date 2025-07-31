import cv2
import threading


class VideoCaptureThread(threading.Thread):
    def __init__(self, src=0):
        super().__init__(daemon=True)
        self.src = src
        if isinstance(src, str) and src.startswith("http"):
            self.cap = self._open_ip(src)
        else:
            self.cap = cv2.VideoCapture(int(src))
        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open video source: {src}")
        self.lock = threading.Lock()
        self.frame = None
        self.running = True

    def _open_ip(self, base_url):
        base = base_url.rstrip("/")
        for url in (base, base + "/video", base + "/mjpeg"):
            try:
                cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
                if cap.isOpened():
                    print(f"[INFO] Opened IP camera at: {url}")
                    return cap
            except Exception:
                pass
        raise RuntimeError(f"Cannot open IP camera with base URL {base_url}")

    def run(self):
        while self.running:
            try:
                ret, frm = self.cap.read()
                if ret:
                    with self.lock:
                        self.frame = frm
            except cv2.error:
                # ignora erros intermitentes do OpenCV
                continue

    def read(self):
        with self.lock:
            return self.frame.copy() if self.frame is not None else None

    def stop(self):
        self.running = False
        self.cap.release()
