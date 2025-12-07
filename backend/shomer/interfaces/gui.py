# shomer/interfaces/gui.py
# pylint: disable=E1101,C0114,C0116,W0611,W1514,C0411,I1101
"""GUI sofisticado dark-tech para Shomer usando PyQt5."""

import csv
import os
from datetime import datetime

import cv2
from PyQt5 import QtCore, QtWidgets, QtGui


class VideoWidget(QtWidgets.QLabel):
    """Exibe frames OpenCV num QLabel com fundo e borda estilizados."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScaledContents(True)
        self.setStyleSheet(
            """
            background-color: #0f0f1e;
            border: 2px solid #2e2e44;
            border-radius: 4px;
        """
        )

    def update_frame(self, frame):
        """Converte BGR→RGB e mostra no label."""
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = QtGui.QImage(rgb.data, w, h, 3 * w, QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(img).scaled(
            self.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
        )
        self.setPixmap(pix)


class StatCard(QtWidgets.QFrame):
    """Cartão estilizado para exibir um valor numérico com label."""

    def __init__(self, title: str, color: str, parent=None):
        super().__init__(parent)
        self.setObjectName("statcard")
        self.setStyleSheet(
            f"""
            QFrame#statcard {{
                background: rgba(50,50,70,200);
                border: 1px solid {color};
                border-radius: 8px;
            }}
            QLabel#stat_title {{
                color: {color};
                font-size: 14px;
            }}
            QLabel#stat_value {{
                color: white;
                font-size: 32px;
                font-weight: bold;
            }}
        """
        )
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        self.lbl_title = QtWidgets.QLabel(title, objectName="stat_title")
        self.lbl_value = QtWidgets.QLabel("0", objectName="stat_value")
        self.lbl_title.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_value.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.lbl_title)
        layout.addWidget(self.lbl_value)

    def set_value(self, val: int):
        self.lbl_value.setText(str(val))


class ShomerWindow(QtWidgets.QWidget):
    """Janela principal dark-tech, com painel de vídeo e cartões de estatísticas."""

    def __init__(self, video_source, people_uc, face_uc):
        super().__init__()
        self.video_source = video_source
        self.people_uc = people_uc
        self.face_uc = face_uc

        self.total_passed = 0
        self.prev_count = 0

        self._setup_ui()
        self._setup_logging()
        self._start_timer()

    def _setup_ui(self):
        self.setWindowTitle("Shomer — Real-Time Detection")
        self.resize(1200, 700)
        self.setStyleSheet(
            """
            QWidget {
                background: #1e1e2f;
                color: #a0a0c0;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel#title {
                font-size: 26px;
                color: #61afef;
                font-weight: bold;
            }
        """
        )

        # Title bar
        title = QtWidgets.QLabel("Shomer — Real-Time Detection", objectName="title")
        title.setAlignment(QtCore.Qt.AlignCenter)

        # Video display
        self.video_widget = VideoWidget(self)
        self.video_widget.setMinimumSize(800, 500)

        # Stat cards: Current and Total
        self.card_current = StatCard("CURRENT", "#61afef")
        self.card_total = StatCard("TOTAL PASSED", "#c678dd")

        stats_layout = QtWidgets.QHBoxLayout()
        stats_layout.setSpacing(16)
        stats_layout.addWidget(self.card_current)
        stats_layout.addWidget(self.card_total)
        stats_layout.addStretch()

        # Export log button
        btn_export = QtWidgets.QPushButton("Export Log CSV")
        btn_export.setCursor(QtCore.Qt.PointingHandCursor)
        btn_export.setStyleSheet(
            """
            QPushButton {
                background: #61afef;
                color: #1e1e2f;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #7fbfff;
            }
        """
        )
        btn_export.clicked.connect(self._export_log)

        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addLayout(stats_layout)
        top_layout.addWidget(btn_export)

        # Main layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)
        main_layout.addWidget(title)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.video_widget, alignment=QtCore.Qt.AlignCenter)

    def _setup_logging(self):
        self.log_path = os.path.join(os.getcwd(), "shomer_log.csv")
        if not os.path.exists(self.log_path):
            with open(self.log_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "current_count", "total_passed"])

    def _start_timer(self):
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update)
        self.timer.start(int(1000 / 30))

    def _update(self):
        frame = self.video_source.read_frame()
        if frame is None:
            return

        people = self.people_uc.execute(frame)
        faces = self.face_uc.execute(frame, people)
        current = len(people)

        if current > self.prev_count:
            self.total_passed += current - self.prev_count
        self.prev_count = current

        # draw detection boxes
        for i, p in enumerate(people):
            x1, y1, x2, y2 = p.bbox
            cv2.rectangle(frame, (x1, y1), (x2, y2), (97, 175, 239), 2)
            label = f"P{i+1}"
            (lw, lh), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(
                frame, (x1, y1 - lh - 8), (x1 + lw + 8, y1), (30, 30, 47), cv2.FILLED
            )
            cv2.putText(
                frame,
                label,
                (x1 + 4, y1 - 4),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (220, 220, 255),
                2,
                cv2.LINE_AA,
            )

        for f in faces:
            x1, y1, x2, y2 = f.bbox
            cv2.rectangle(frame, (x1, y1), (x2, y2), (91, 217, 131), 2)

        # update UI stats
        self.card_current.set_value(current)
        self.card_total.set_value(self.total_passed)

        # log entry
        ts = datetime.now().isoformat(timespec="seconds")
        with open(self.log_path, "a", encoding="utf-8", newline="") as f:
            csv.writer(f).writerow([ts, current, self.total_passed])

        self.video_widget.update_frame(frame)

    def _export_log(self):
        """Abre o CSV no explorador para download/manipulação."""
        path = os.path.abspath(self.log_path)
        QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(path))
