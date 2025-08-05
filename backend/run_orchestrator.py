# backend/run_orchestrator.py
import os
import time
from datetime import datetime

import httpx
from shomer.infrastructure.video_source.opencv_capture import OpenCVVideoSource
from shomer.infrastructure.detectors.yolo_detector import YOLOPersonDetector
from shomer.application.detect_people import DetectPeopleUseCase

def send_log_sync(count: int, details: dict = None):
    """
    Envia um registro de log de forma síncrona.
    """
    url = os.getenv("LOGS_URL", "http://localhost:8000/logs")
    payload = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "count": count,
        "details": details or {}
    }
    try:
        with httpx.Client() as client:
            resp = client.post(url, json=payload, timeout=5.0)
            resp.raise_for_status()
    except Exception as e:
        print(f"❌ Falha ao enviar log: {e}")

def run_loop():
    # Fonte de vídeo USB/webcam (índice 0)
    source = OpenCVVideoSource(0)

    # Parâmetros vindos de .env ou defaults
    model_path = os.getenv("YOLO_MODEL", "yolov8n.pt")
    conf_thr   = float(os.getenv("CONF_THRESHOLD", "0.5"))

    # Detector e caso de uso
    person_detector = YOLOPersonDetector(model_path, conf_thr)
    people_uc       = DetectPeopleUseCase(person_detector)

    print(f"▶️ Iniciando orquestrador: modelo={model_path}, thr={conf_thr}")

    while True:
        frame = source.read_frame()
        if frame is None:
            time.sleep(0.01)
            continue

        people = people_uc.execute(frame)
        # Envia log de forma síncrona (pode bloquear até ~200ms)
        send_log_sync(len(people), {"mode": "webcam"})

if __name__ == "__main__":
    run_loop()
