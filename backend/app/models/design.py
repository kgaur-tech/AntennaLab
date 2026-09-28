from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class DesignRecord:
    design_id: str
    canonical_design: dict[str, Any]
    model_id: str
    model_version: str
    design_hash: str
    created_at: str = field(default_factory=utc_now_iso)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, design: dict[str, Any], metadata: dict[str, Any] | None = None) -> "DesignRecord":
        return cls(
            design_id=str(design["design_id"]),
            canonical_design=design,
            model_id=str(design["family"]),
            model_version=str(design["model_version"]),
            design_hash=str(design["design_hash"]),
            metadata=metadata or {},
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "design_id": self.design_id,
            "canonical_design": self.canonical_design,
            "model_id": self.model_id,
            "model_version": self.model_version,
            "design_hash": self.design_hash,
            "created_at": self.created_at,
            "metadata": self.metadata,
        }


@dataclass
class DesignRevisionRecord:
    design_id: str
    requirement_snapshot: dict[str, Any]
    canonical_design_snapshot: dict[str, Any]
    analysis_summary: dict[str, Any]
    revision_id: str = field(default_factory=lambda: str(uuid4()))
    revision_number: int = 1
    created_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return {
            "revision_id": self.revision_id,
            "design_id": self.design_id,
            "revision_number": self.revision_number,
            "requirement_snapshot": self.requirement_snapshot,
            "canonical_design_snapshot": self.canonical_design_snapshot,
            "analysis_summary": self.analysis_summary,
            "created_at": self.created_at,
        }
