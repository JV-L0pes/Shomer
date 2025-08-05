# shomer/infrastructure/presenters/opencv_renderer.py

import cv2
from typing import List
from shomer.domain.ports.renderer import IRenderer
from shomer.domain.entities.person import Person
from shomer.domain.entities.face import Face


class OpenCVRenderer(IRenderer):
    def __init__(self, title: str, colors: dict):
        self.window = title
        cv2.namedWindow(self.window, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(
            self.window, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN
        )
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.scale = 0.8
        self.thick = 2
        self.pad = 10
        self.colors = colors

    def render(self, frame, people: List[Person], faces: List[Face]) -> int:
        h, w = frame.shape[:2]

        # 1) Draw person boxes and labels (e.g., "P1", "P2")
        for i, p in enumerate(people):
            x1, y1, x2, y2 = p.bbox
            cv2.rectangle(frame, (x1, y1), (x2, y2), self.colors["person"], self.thick)
            label = f"P{i+1}"
            (lw, lh), _ = cv2.getTextSize(label, self.font, self.scale, self.thick)
            # background for label
            bg_x1 = x1
            bg_y1 = max(y1 - lh - self.pad, 0)
            bg_x2 = x1 + lw + 2 * self.pad
            bg_y2 = y1
            cv2.rectangle(
                frame, (bg_x1, bg_y1), (bg_x2, bg_y2), self.colors["person"], cv2.FILLED
            )
            # text
            tx = bg_x1 + self.pad // 2
            ty = bg_y2 - self.pad // 2
            cv2.putText(
                frame,
                label,
                (tx, ty),
                self.font,
                self.scale,
                self.colors["text"],
                self.thick,
                cv2.LINE_AA,
            )

        # 2) Draw face boxes
        for f in faces:
            x1, y1, x2, y2 = f.bbox
            cv2.rectangle(frame, (x1, y1), (x2, y2), self.colors["face"], self.thick)

        # 3) Draw total count in top-left with safe margins
        total = len(people)
        text = f"Total: {total}"
        (tw, th), _ = cv2.getTextSize(text, self.font, self.scale, self.thick)
        # place 20px below top to ensure visible
        text_x = self.pad
        text_y = th + self.pad * 2
        # background box
        cv2.rectangle(
            frame,
            (text_x - self.pad // 2, text_y - th - self.pad // 2),
            (text_x + tw + self.pad // 2, text_y + self.pad // 2),
            self.colors["bg"],
            cv2.FILLED,
        )
        # text
        cv2.putText(
            frame,
            text,
            (text_x, text_y),
            self.font,
            self.scale,
            self.colors["text"],
            self.thick,
            cv2.LINE_AA,
        )

        # 4) Show and return key
        cv2.imshow(self.window, frame)
        return cv2.waitKey(1)

    def close(self):
        cv2.destroyAllWindows()
