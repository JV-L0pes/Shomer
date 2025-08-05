# shomer/interfaces/cli.py

import argparse
import os
from PyQt5 import QtWidgets

from shomer.interfaces.config import Config
from shomer.infrastructure.video_source.opencv_capture import OpenCVVideoSource
from shomer.infrastructure.detectors.yolo_detector import YOLOPersonDetector
from shomer.infrastructure.detectors.mp_detector import MediaPipeFaceDetector
from shomer.interfaces.gui import ShomerWindow


def build_and_run():
    """Constrói dependências e inicia o frontend PyQt."""
    parser = argparse.ArgumentParser(description="Shomer Real-Time Detector")
    parser.add_argument(
        "--source",
        "-s",
        choices=["webcam", "ip"],
        default="webcam",
        help="Fonte: 'webcam' ou 'ip' (DroidCam)",
    )
    parser.add_argument(
        "--ip-url", default=None, help="URL do stream IP (sobrescreve config)"
    )
    args = parser.parse_args()

    cfg = Config.load()
    ip_url = args.ip_url or cfg["ip_url"]

    # Video source
    if args.source == "webcam":
        video_source = OpenCVVideoSource(0)
    else:
        video_source = OpenCVVideoSource(ip_url)

    # Detectores
    people_detector = YOLOPersonDetector(cfg["yolo_model"], cfg["conf_threshold"])
    face_detector = MediaPipeFaceDetector()

    # Casos de uso
    from shomer.application.detect_people import DetectPeopleUseCase
    from shomer.application.detect_faces import DetectFacesUseCase

    people_uc = DetectPeopleUseCase(people_detector)
    face_uc = DetectFacesUseCase(face_detector)

    # Estilo Qt
    os.environ["QT_QUICK_CONTROLS_STYLE"] = "Basic"
    app = QtWidgets.QApplication([])
    window = ShomerWindow(video_source, people_uc, face_uc)
    window.show()
    app.exec_()
