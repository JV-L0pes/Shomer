# shomer/infrastructure/detectors/yolo_detector.py

from ultralytics import YOLO
from shomer.domain.ports.detector import IPersonDetector


class YOLOPersonDetector(IPersonDetector):
    def __init__(self, model_path: str, conf: float):
        # Carrega o modelo e depois fusiona, garantindo que self.model seja o wrapper YOLO
        model = YOLO(model_path)
        model.fuse()  # otimiza as camadas, mas não retorna nada
        self.model = model
        self.conf = conf

    def detect(self, frame):
        # agora self.model é o objeto YOLO
        return self.model(frame, conf=self.conf, classes=[0])[0]
