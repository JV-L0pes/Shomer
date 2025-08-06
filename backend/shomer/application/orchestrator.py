# shomer/application/orchestrator.py

from shomer.domain.ports.video_source import IVideoSource
from shomer.domain.ports.renderer import IRenderer
from shomer.application.detect_people import DetectPeopleUseCase
from shomer.application.detect_faces import DetectFacesUseCase
from datetime import datetime, timezone, timedelta
import httpx
import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from config import brasilia_now


async def send_log(count: int, details: dict = None):
    """
    Envia um registro de log para o backend FastAPI.
    """
    payload = {
        "timestamp": brasilia_now().isoformat() + "Z",
        "count": count,
        "details": details or {}
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "http://localhost:8000/logs",  # ou "http://mongo-network-alias:8000" no Compose
            json=payload
        )
        resp.raise_for_status()


class Orchestrator:
    def __init__(
        self,
        source: IVideoSource,
        people_uc: DetectPeopleUseCase,
        face_uc: DetectFacesUseCase,
        renderer: IRenderer,
    ):
        self.source = source
        self.people_uc = people_uc
        self.face_uc = face_uc
        self.renderer = renderer

    def run(self):
        while True:
            frame = self.source.read_frame()
            if frame is None:
                continue

            people = self.people_uc.execute(frame)
            # dispara log (contagem de pessoas)
            try:
                asyncio.create_task(send_log(len(people), {"mode": "usb_camera"}))
            except Exception as e:
                print(f"❌ Falha ao enviar log: {e}")

            faces = self.face_uc.execute(frame, people)

            # Chama render apenas com os três parâmetros esperados
            key = self.renderer.render(frame, people, faces)
            if key & 0xFF == ord("q"):
                break

        self.source.close()
        self.renderer.close()
