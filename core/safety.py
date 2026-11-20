"""Confirmação temporal e limitação de repetição dos comandos."""
from dataclasses import dataclass, field


@dataclass
class GestureGate:
    hold_seconds: float = 0.32
    cooldown_seconds: float = 0.55
    _candidate: str | None = field(default=None, init=False)
    _since: float = field(default=0.0, init=False)
    _last_fired: float = field(default=float("-inf"), init=False)

    def update(self, name: str | None, now: float, enabled: bool) -> bool:
        if not enabled or name is None or name == "unknown":
            self._candidate = None
            return False
        if name != self._candidate:
            self._candidate = name
            self._since = now
            return False
        if now - self._since < self.hold_seconds:
            return False
        if now - self._last_fired < self.cooldown_seconds:
            return False
        self._last_fired = now
        self._since = now
        return True

    def reset(self) -> None:
        self._candidate = None
        self._last_fired = float("-inf")
