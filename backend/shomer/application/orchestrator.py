# shomer/application/orchestrator.py

from shomer.domain.ports.video_source import IVideoSource
from shomer.domain.ports.renderer import IRenderer
from shomer.application.detect_people import DetectPeopleUseCase
from shomer.application.detect_faces import DetectFacesUseCase


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
            faces = self.face_uc.execute(frame, people)

            # Chama render apenas com os três parâmetros esperados
            key = self.renderer.render(frame, people, faces)
            if key & 0xFF == ord("q"):
                break

        self.source.close()
        self.renderer.close()
