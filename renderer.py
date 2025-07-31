# renderer.py
import cv2


class Renderer:
    def __init__(self):
        # Window setup: normal + fullscreen
        self.window_name = "Shomer - Real-time Detection"
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(
            self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN
        )

        # Text style
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.7
        self.thickness = 2
        self.padding = 8

        # Color palette (BGR)
        self.body_color = (0, 255, 255)  # yellow for person
        self.face_color = (255, 128, 0)  # orange for face
        self.bg_color = (0, 0, 0)  # black for backgrounds
        self.count_color = (255, 255, 255)  # white for count text

    def draw(self, frame, bodies, faces):
        h, w, _ = frame.shape

        # — Draw each person box + label —
        for i, box in enumerate(bodies.boxes.xyxy):
            x1, y1, x2, y2 = map(int, box)
            # draw person box
            cv2.rectangle(frame, (x1, y1), (x2, y2), self.body_color, self.thickness)

            # label above box
            label = f"Person {i+1}"
            (lw, lh), _ = cv2.getTextSize(
                label, self.font, self.font_scale, self.thickness
            )
            bx1 = x1
            by2 = y1 - self.padding
            by1 = by2 - lh - self.padding
            bx2 = bx1 + lw + self.padding * 2

            # background for label
            cv2.rectangle(frame, (bx1, by1), (bx2, by2), self.body_color, cv2.FILLED)
            # put label text
            tx = bx1 + self.padding
            ty = by2 - self.padding // 2
            cv2.putText(
                frame,
                label,
                (tx, ty),
                self.font,
                self.font_scale,
                self.bg_color,
                self.thickness,
                cv2.LINE_AA,
            )

        # — Draw face boxes —
        # faces is now a list of (x1,y1,x2,y2) tuples
        if isinstance(faces, list):
            for fx1, fy1, fx2, fy2 in faces:
                cv2.rectangle(
                    frame, (fx1, fy1), (fx2, fy2), self.face_color, self.thickness
                )
        else:
            # fallback if still using MediaPipe object
            if hasattr(faces, "detections") and faces.detections:
                for det in faces.detections:
                    bbox = det.location_data.relative_bounding_box
                    x1 = int(bbox.xmin * w)
                    y1 = int(bbox.ymin * h)
                    x2 = x1 + int(bbox.width * w)
                    y2 = y1 + int(bbox.height * h)
                    cv2.rectangle(
                        frame, (x1, y1), (x2, y2), self.face_color, self.thickness
                    )

        # — Draw total count at top‑right —
        count = len(bodies.boxes.xyxy)
        count_text = f"{count} people"
        (cw, ch), _ = cv2.getTextSize(
            count_text, self.font, self.font_scale, self.thickness
        )
        cx2 = w - self.padding
        cy1 = self.padding
        cx1 = cx2 - cw - self.padding * 2
        cy2 = cy1 + ch + self.padding * 2

        cv2.rectangle(frame, (cx1, cy1), (cx2, cy2), self.bg_color, cv2.FILLED)
        tx = cx1 + self.padding
        ty = cy2 - self.padding // 2
        cv2.putText(
            frame,
            count_text,
            (tx, ty),
            self.font,
            self.font_scale,
            self.count_color,
            self.thickness,
            cv2.LINE_AA,
        )

        # — Show frame and return key —
        cv2.imshow(self.window_name, frame)
        return cv2.waitKey(1)

    def close(self):
        cv2.destroyAllWindows()
