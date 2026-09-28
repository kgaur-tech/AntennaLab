from __future__ import annotations

from typing import Any


class DesignRepository:
    """Persisted storage contract for antenna designs and revisions."""

    def save(self, design: dict[str, Any]) -> dict[str, Any]:
        return design

    def list_recent(self) -> list[dict[str, Any]]:
        return []
