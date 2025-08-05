# backend/detection.py

import cv2
import threading
from ultralytics import YOLO
from insightface.app import FaceAnalysis

YOLO_MODEL = 'yolov8n.pt'
CONF_THRESHOLD = 0.5

class Detector:
    def __init__(self, src=0):
        # captura em background
        self.cap = cv2.VideoCapture(src)
        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open source {src}")

        # contadores
        self.prev_count    = 0
        self.total_passed  = 0

        # init YOLO
        model = YOLO(YOLO_MODEL)
        model.fuse()
        if cv2.cuda.getCudaEnabledDeviceCount() > 0:
            model.model = model.model.half().to('cuda')
        self.person_model = model

        # init InsightFace (detection only)
        self.face_analyzer = FaceAnalysis(allowed_modules=['detection'])
        ctx = 0 if cv2.cuda.getCudaEnabledDeviceCount() > 0 else -1
        self.face_analyzer.prepare(ctx_id=ctx, det_size=(640, 640))

        self.lock = threading.Lock()
        self.frame = None
        self.running = True
        threading.Thread(target=self._reader, daemon=True).start()

    def _reader(self):
        while self.running:
            ok, frm = self.cap.read()
            if not ok:
                continue
            with self.lock:
                self.frame = frm

    def get_frame(self):
        with self.lock:
            return None if self.frame is None else self.frame.copy()

    def detect_and_annotate(self, frame):
        # pessoas
        res = self.person_model(frame, conf=CONF_THRESHOLD, classes=[0])[0]
        current = len(res.boxes)
        if current > self.prev_count:
            self.total_passed += current - self.prev_count
        self.prev_count = current

        for i, box in enumerate(res.boxes.xyxy):
            x1,y1,x2,y2 = map(int, box)
            cv2.rectangle(frame, (x1,y1),(x2,y2),(0,255,255),2)
            cv2.putText(frame,f"P{i+1}",(x1,y1-5),
                        cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,0),2)

        # faces
        faces = self.face_analyzer.get(frame)
        for f in faces:
            x1,y1,x2,y2 = map(int, f.bbox)
            cv2.rectangle(frame,(x1,y1),(x2,y2),(255,128,0),2)

        return frame

    def stop(self):
        self.running = False
        self.cap.release()
