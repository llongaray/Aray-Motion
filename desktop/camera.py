"""Captura em thread separada da GUI."""
import cv2
from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtGui import QImage


class CameraWorker(QObject):
    frame_ready = Signal(QImage)
    error = Signal(str)
    finished = Signal()

    def __init__(self, index: int, detector):
        super().__init__()
        self.index = index
        self.detector = detector
        self.running = True

    @Slot()
    def run(self) -> None:
        cap = cv2.VideoCapture(self.index, cv2.CAP_DSHOW)
        try:
            if not cap.isOpened():
                self.error.emit(f"Não foi possível abrir a câmera {self.index}")
                return
            while self.running:
                ok, frame = cap.read()
                if not ok:
                    self.error.emit("Falha na captura da câmera")
                    break
                frame = cv2.flip(frame, 1)
                frame = self.detector.annotate(frame)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, channels = rgb.shape
                image = QImage(rgb.data, w, h, channels * w, QImage.Format_RGB888).copy()
                self.frame_ready.emit(image)
        except Exception as exc:
            self.error.emit(f"Erro na captura: {exc}")
        finally:
            cap.release()
            self.finished.emit()

    def stop(self) -> None:
        self.running = False


def available_cameras(limit: int = 8) -> list[int]:
    indices = []
    for index in range(limit):
        capture = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        try:
            if capture.isOpened():
                indices.append(index)
        finally:
            capture.release()
    return indices
