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
    print("🔧 [DEBUG] Iniciando Shomer CLI...")
    
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
    
    print(f"📹 [DEBUG] Fonte selecionada: {args.source}")
    print(f"🌐 [DEBUG] IP URL: {args.ip_url}")

    cfg = Config.load()
    print(f"⚙️ [DEBUG] Configuração carregada: {cfg}")
    
    ip_url = args.ip_url or cfg["ip_url"]
    print(f"🌐 [DEBUG] URL final: {ip_url}")

    # Video source
    print("📹 [DEBUG] Configurando fonte de vídeo...")
    if args.source == "webcam":
        print("📹 [DEBUG] Usando webcam (índice 0)")
        video_source = OpenCVVideoSource(0)
    else:
        print(f"📹 [DEBUG] Usando IP camera: {ip_url}")
        video_source = OpenCVVideoSource(ip_url)

    # Detectores
    print("🤖 [DEBUG] Carregando detectores...")
    people_detector = YOLOPersonDetector(cfg["yolo_model"], cfg["conf_threshold"])
    print("✅ [DEBUG] Detector de pessoas carregado")
    face_detector = MediaPipeFaceDetector()
    print("✅ [DEBUG] Detector facial carregado")

    # Casos de uso
    from shomer.application.detect_people import DetectPeopleUseCase
    from shomer.application.detect_faces import DetectFacesUseCase

    people_uc = DetectPeopleUseCase(people_detector)
    face_uc = DetectFacesUseCase(face_detector)

    # Estilo Qt
    print("🎨 [DEBUG] Iniciando interface GUI...")
    os.environ["QT_QUICK_CONTROLS_STYLE"] = "Basic"
    app = QtWidgets.QApplication([])
    print("✅ [DEBUG] Aplicação Qt criada")
    window = ShomerWindow(video_source, people_uc, face_uc)
    print("✅ [DEBUG] Janela Shomer criada")
    window.show()
    print("🎨 [DEBUG] Janela exibida - iniciando loop de eventos...")
    app.exec_()
