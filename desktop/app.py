"""Interface gráfica inicial da Aray Motion."""
import sys
from PySide6.QtCore import Qt, QThread
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QHBoxLayout, QLabel,
    QMainWindow, QMessageBox, QPushButton, QVBoxLayout, QWidget,
)
from desktop.camera import CameraWorker, available_cameras
from desktop.vision import VisionDetector


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aray Motion | Controle por gestos")
        self.resize(1100, 710)
        self.thread = None
        self.worker = None
        self.detector = None
        root = QWidget()
        layout = QVBoxLayout(root)
        heading = QLabel("ARAY MOTION")
        heading.setObjectName("heading")
        layout.addWidget(heading)
        layout.addWidget(QLabel("Visão computacional local • Windows"))
        controls = QHBoxLayout()
        self.cameras = QComboBox()
        self.cameras.addItem("Selecione uma câmera", None)
        for index in available_cameras():
            self.cameras.addItem(f"Câmera {index}", index)
        controls.addWidget(self.cameras)
        self.hands = QCheckBox("Mãos")
        self.hands.setChecked(True)
        self.face = QCheckBox("Rosto")
        self.face.setChecked(True)
        controls.addWidget(self.hands)
        controls.addWidget(self.face)
        self.start_button = QPushButton("Iniciar")
        self.start_button.clicked.connect(self.start_camera)
        controls.addWidget(self.start_button)
        self.stop_button = QPushButton("Parar")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_camera)
        controls.addWidget(self.stop_button)
        layout.addLayout(controls)
        self.video = QLabel("Selecione uma câmera e pressione Iniciar")
        self.video.setAlignment(Qt.AlignCenter)
        self.video.setObjectName("video")
        self.video.setMinimumHeight(440)
        layout.addWidget(self.video, 1)
        self.status = QLabel("Pronto. Controle do sistema desativado.")
        layout.addWidget(self.status)
        self.setCentralWidget(root)
        self.setStyleSheet("""
            QMainWindow, QWidget { background: #101720; color: #f0f4fa; font-size: 14px; }
            QLabel#heading { font-size: 30px; font-weight: 800; color: #48c9ff; }
            QLabel#video { background: #0a0e15; border: 1px solid #334155; border-radius: 14px; }
            QPushButton, QComboBox { padding: 10px; background: #223244; border-radius: 7px; }
            QPushButton:hover { background: #2f5368; }
        """)

    def start_camera(self):
        if self.thread is not None:
            return
        index = self.cameras.currentData()
        if index is None:
            QMessageBox.warning(self, "Câmera", "Selecione uma câmera disponível.")
            return
        if not self.hands.isChecked() and not self.face.isChecked():
            QMessageBox.warning(self, "Detectores", "Ative ao menos um detector.")
            return
        try:
            self.detector = VisionDetector(self.hands.isChecked(), self.face.isChecked())
        except Exception as exc:
            QMessageBox.critical(self, "Modelos", str(exc))
            return
        self.thread = QThread()
        self.worker = CameraWorker(index, self.detector)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.frame_ready.connect(self.show_frame)
        self.worker.error.connect(self.show_error)
        self.worker.finished.connect(self.thread.quit)
        self.thread.finished.connect(self.on_stopped)
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.status.setText("Captura iniciada. Nenhuma ação de mouse será executada.")
        self.thread.start()

    def show_frame(self, image):
        pixmap = QPixmap.fromImage(image)
        self.video.setPixmap(pixmap.scaled(
            self.video.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def show_error(self, message):
        self.status.setText(message)
        self.stop_camera()

    def stop_camera(self):
        if self.worker:
            self.worker.stop()
        self.stop_button.setEnabled(False)

    def on_stopped(self):
        if self.detector:
            self.detector.close()
            self.detector = None
        self.worker = None
        self.thread = None
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.status.setText("Captura encerrada.")

    def closeEvent(self, event):
        if self.thread and self.thread.isRunning():
            self.stop_camera()
            self.thread.quit()
            if not self.thread.wait(5000):
                event.ignore()
                self.status.setText("Aguardando câmera encerrar; tente novamente.")
                return
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
