"""Interpretação de gestos a partir de landmarks 2D normalizados.

Pontos seguem a convenção MediaPipe Hand Landmarker: polegar ponta=4,
indicador ponta=8, indicador MCP=5 e polegar MCP=2.
"""
from dataclasses import dataclass
from math import hypot
from typing import Sequence


@dataclass(frozen=True)
class Point:
    x: float
    y: float


@dataclass(frozen=True)
class Gesture:
    name: str
    confidence: float
    cursor: Point | None = None


def distance(a: Point, b: Point) -> float:
    return hypot(a.x - b.x, a.y - b.y)


def interpret_hand(points: Sequence[Point], pinch_ratio: float = 0.35) -> Gesture:
    """Identifica pinça ou movimento apontado usando escala da palma.

    Não injeta eventos no sistema. Retorna uma intenção, a ser validada
    por confirmação temporal e permissão explícita no adaptador de comandos.
    """
    if len(points) != 21:
        raise ValueError("Uma mão deve possuir exatamente 21 landmarks")
    if pinch_ratio <= 0:
        raise ValueError("pinch_ratio deve ser positivo")
    palm = distance(points[0], points[9])
    if palm < 1e-6:
        return Gesture("unknown", 0.0)
    ratio = distance(points[4], points[8]) / palm
    tip = points[8]
    if ratio < pinch_ratio:
        return Gesture("pinch", min(1.0, (pinch_ratio - ratio) / pinch_ratio), tip)
    return Gesture("point", min(1.0, ratio / (2 * pinch_ratio)), tip)
