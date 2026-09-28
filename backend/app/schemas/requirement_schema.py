from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator


FrequencyUnit = Literal["Hz", "kHz", "MHz", "GHz", "hz", "khz", "mhz", "ghz"]


class RequirementSchema(BaseModel):
    application: str = Field(..., min_length=2)
    frequency_hz: float | None = Field(default=None, gt=0)
    frequency: float | None = Field(default=None, gt=0)
    frequency_unit: FrequencyUnit = "Hz"
    bandwidth_hz: float | None = Field(default=None, gt=0)
    gain_db: float | None = Field(default=None, ge=-100, le=100)
    polarization: str = Field(default="linear")
    is_directional: bool = True
    max_dimension_m: float | None = Field(default=None, gt=0)
    target_impedance_ohms: float = Field(default=50.0, gt=0)
    environment: str = Field(default="general")
    notes: str = ""
    priority_weights: dict[str, float] = Field(default_factory=lambda: {
        "gain": 1.0,
        "size": 1.0,
        "bandwidth": 1.0,
    })
    antenna_family_preferences: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def require_frequency(self) -> "RequirementSchema":
        if self.frequency_hz is None and self.frequency is None:
            raise ValueError("Either frequency_hz or frequency is required.")
        return self

    def normalized_frequency_hz(self) -> float:
        from engineering.core.units.frequency import normalize_frequency

        if self.frequency_hz is not None:
            return normalize_frequency(self.frequency_hz, "Hz")
        if self.frequency is not None:
            return normalize_frequency(self.frequency, self.frequency_unit)
        raise ValueError("Either frequency_hz or frequency is required.")
