"""Visão computacional local com MediaPipe Tasks.

Requer os modelos .task instalados em desktop/models/.
"""
from pathlib import Path
import cv2
import mediapipe as mp

MODEL_DIR = Path(__file__).parent / "models"


class VisionDetector:
    def __init__(self, hands=True, face=True):
        base = mp.tasks.BaseOptions
        vision = mp.tasks.vision
        self.hand = None
        self.face = None
        if hands:
            path = MODEL_DIR / "hand_landmarker.task"
            if not path.exists():
                raise FileNotFoundError(f"Modelo ausente: {path}")
            opts = vision.HandLandmarkerOptions(
                base_options=base(model_asset_path=str(path)),
                running_mode=vision.RunningMode.IMAGE,
                num_hands=2,
            )
            self.hand = vision.HandLandmarker.create_from_options(opts)
        if face:
            path = MODEL_DIR / "face_landmarker.task"
            if not path.exists():
                self.close()
                raise FileNotFoundError(f"Modelo ausente: {path}")
            opts = vision.FaceLandmarkerOptions(
                base_options=base(model_asset_path=str(path)),
                running_mode=vision.RunningMode.IMAGE,
                num_faces=2,
            )
            self.face = vision.FaceLandmarker.create_from_options(opts)

    def annotate(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        height, width = frame.shape[:2]
        if self.hand:
            result = self.hand.detect(mp_image)
            connections = mp.solutions.hands.HAND_CONNECTIONS if hasattr(mp, "solutions") else ()
            for landmarks in result.hand_landmarks:
                for edge in connections:
                    p, q = landmarks[edge[0]], landmarks[edge[1]]
                    cv2.line(frame, (int(p.x * width), int(p.y * height)),
                             (int(q.x * width), int(q.y * height)), (0, 210, 255), 2)
                for point in landmarks:
                    cv2.circle(frame, (int(point.x * width), int(point.y * height)), 3, (20, 255, 130), -1)
        if self.face:
            result = self.face.detect(mp_image)
            for landmarks in result.face_landmarks:
                for point in landmarks:
                    cv2.circle(frame, (int(point.x * width), int(point.y * height)), 1, (255, 180, 20), -1)
        return frame

    def close(self):
        if self.hand:
            self.hand.close()
            self.hand = None
        if self.face:
            self.face.close()
            self.face = None
