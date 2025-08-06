# backend/config.py - Configurações do Sistema

import os
from datetime import datetime, timezone, timedelta
from typing import Dict, Any

def brasilia_now():
    """Retorna o horário atual de Brasília (GMT-3)."""
    return datetime.now(timezone(timedelta(hours=-3)))

class Config:
    """Configurações centralizadas do sistema Shomer."""
    
    # Configurações de Câmera
    CAMERA_SOURCES = {
        "webcam": 0,
        "ip_camera": "http://192.168.15.5:4747/video"  # DroidCam padrão
    }
    
    # Configurações de Detecção
    YOLO_MODEL = os.getenv("YOLO_MODEL", "yolov8n.pt")
    CONF_THRESHOLD = float(os.getenv("CONF_THRESHOLD", "0.5"))
    
    # Configurações de Performance
    TARGET_FPS = int(os.getenv("TARGET_FPS", "60"))
    DETECTION_FPS = int(os.getenv("DETECTION_FPS", "30"))
    BUFFER_SIZE = int(os.getenv("BUFFER_SIZE", "1"))
    
    # Configurações do Servidor
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    
    # Configurações de Stream
    STREAM_ENABLED_BY_DEFAULT = os.getenv("STREAM_ENABLED_BY_DEFAULT", "true").lower() == "true"
    
    # Configurações do Banco de Dados
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://mongo:27017/shomerdb")
    
    @classmethod
    def get_camera_config(cls) -> Dict[str, Any]:
        """Retorna configurações de câmera."""
        return {
            "current_source": cls.CAMERA_SOURCES["webcam"],  # Começa com webcam
            "ip_url": cls.CAMERA_SOURCES["ip_camera"],
            "stream_enabled": cls.STREAM_ENABLED_BY_DEFAULT,
            "available_sources": cls.CAMERA_SOURCES
        }
    
    @classmethod
    def get_detection_config(cls) -> Dict[str, Any]:
        """Retorna configurações de detecção."""
        return {
            "yolo_model": cls.YOLO_MODEL,
            "conf_threshold": cls.CONF_THRESHOLD,
            "target_fps": cls.TARGET_FPS,
            "detection_fps": cls.DETECTION_FPS,
            "buffer_size": cls.BUFFER_SIZE
        }
    
    @classmethod
    def get_server_config(cls) -> Dict[str, Any]:
        """Retorna configurações do servidor."""
        return {
            "host": cls.HOST,
            "port": cls.PORT
        }
    
    @classmethod
    def get_database_config(cls) -> Dict[str, Any]:
        """Retorna configurações do banco de dados."""
        return {
            "mongodb_uri": cls.MONGODB_URI
        }
    
    @classmethod
    def update_ip_camera_url(cls, url: str) -> None:
        """Atualiza a URL da IP camera."""
        cls.CAMERA_SOURCES["ip_camera"] = url
    
    @classmethod
    def print_config(cls) -> None:
        """Imprime as configurações atuais."""
        print("🔧 Configurações do Sistema Shomer:")
        print(f"   📹 Câmeras disponíveis: {list(cls.CAMERA_SOURCES.keys())}")
        print(f"   🌐 IP Camera URL: {cls.CAMERA_SOURCES['ip_camera']}")
        print(f"   🤖 Modelo YOLO: {cls.YOLO_MODEL}")
        print(f"   🎯 Threshold: {cls.CONF_THRESHOLD}")
        print(f"   ⚡ FPS Alvo: {cls.TARGET_FPS}")
        print(f"   🧠 FPS Detecção: {cls.DETECTION_FPS}")
        print(f"   📦 Buffer: {cls.BUFFER_SIZE}")
        print(f"   🚀 Servidor: {cls.HOST}:{cls.PORT}")
        print(f"   ▶️  Stream padrão: {'Habilitado' if cls.STREAM_ENABLED_BY_DEFAULT else 'Desabilitado'}")
        print(f"   🗄️  MongoDB: {cls.MONGODB_URI}")

# Configurações de exemplo para diferentes cenários
class ConfigExamples:
    """Exemplos de configurações para diferentes cenários."""
    
    @staticmethod
    def droidcam_config() -> Dict[str, str]:
        """Configuração para DroidCam."""
        return {
            "ip_camera": "http://192.168.1.100:4747/video",
            "description": "DroidCam - Substitua pelo IP do seu celular"
        }
    
    @staticmethod
    def ip_webcam_config() -> Dict[str, str]:
        """Configuração para IP Webcam."""
        return {
            "ip_camera": "http://192.168.1.100:8080/video",
            "description": "IP Webcam - Substitua pelo IP do seu celular"
        }
    
    @staticmethod
    def local_webcam_config() -> Dict[str, str]:
        """Configuração para webcam local."""
        return {
            "ip_camera": "0",
            "description": "Webcam local (índice 0)"
        }

if __name__ == "__main__":
    # Imprimir configurações atuais
    Config.print_config()
    
    print("\n📋 Exemplos de configuração:")
    print("   DroidCam:", ConfigExamples.droidcam_config())
    print("   IP Webcam:", ConfigExamples.ip_webcam_config())
    print("   Webcam Local:", ConfigExamples.local_webcam_config()) 