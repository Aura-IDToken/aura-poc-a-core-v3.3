"""
Append-only event hash log.
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class EventLogEntry:
    index: int
    event_hash: str


class AppendOnlyEventLog:
    """
    Immutable API surface for audit event hashes.
    Supports append and read-only access only.
    """

    def __init__(self):
        self._hashes = []

    def append(self, event_hash: str) -> EventLogEntry:
        if not isinstance(event_hash, str) or len(event_hash) != 64:
            raise ValueError("event_hash must be a SHA-256 hex string")
        self._hashes.append(event_hash)
        return EventLogEntry(index=len(self._hashes) - 1, event_hash=event_hash)

    def get(self, index: int) -> EventLogEntry:
        if index < 0 or index >= len(self._hashes):
            raise IndexError("event index out of range")
        return EventLogEntry(index=index, event_hash=self._hashes[index])

    def hashes(self) -> Tuple[str, ...]:
        return tuple(self._hashes)

    def __len__(self) -> int:
        return len(self._hashes)

