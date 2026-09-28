from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator


FrequencyUnit = Literal["Hz", "kHz", "MHz", "GHz", "hz", "khz", "mhz", "ghz"]
Directionality = Literal["no_preference", "omnidirectional", "directional", "highly_directional"]
Polarization = Literal["no_preference", "linear", "horizontal", "vertical", "circular", "custom"]


class RequirementSchema(BaseModel):
    application: str = Field(..., min_length=2)
    frequency_hz: float | None = Field(default=None, gt=0)
    frequency: float | None = Field(default=None, gt=0)
    frequency_unit: FrequencyUnit = "Hz"
    bandwidth_hz: float | None = Field(default=None, gt=0)
    gain_db: float | None = Field(default=None, ge=-100, le=100)
    polarization: Polarization = Field(default="linear")
    is_directional: bool = True
    directionality: Directionality = "no_preference"
    max_dimension_m: float | None = Field(default=None, gt=0)
    max_width_m: float | None = Field(default=None, gt=0)
    max_height_m: float | None = Field(default=None, gt=0)
    max_volume_m3: float | None = Field(default=None, gt=0)
    target_impedance_ohms: float = Field(default=50.0, gt=0)
    environment: str = Field(default="general")
    feed_type: str | None = Field(default=None, min_length=1)
    connector: str | None = Field(default=None, min_length=1)
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

    @model_validator(mode="after")
    def validate_weights(self) -> "RequirementSchema":
        supported = {"gain", "size", "bandwidth", "efficiency", "simplicity", "cost"}
        invalid = set(self.priority_weights) - supported
        if invalid:
            raise ValueError(f"Unsupported priority weights: {', '.join(sorted(invalid))}.")
        if any(value < 0 or value > 3 for value in self.priority_weights.values()):
            raise ValueError("Priority weights must be between 0 and 3.")
        return self

    def normalized_frequency_hz(self) -> float:
        from engineering.core.units.frequency import normalize_frequency

        if self.frequency_hz is not None:
            return normalize_frequency(self.frequency_hz, "Hz")
        if self.frequency is not None:
            return normalize_frequency(self.frequency, self.frequency_unit)
        raise ValueError("Either frequency_hz or frequency is required.")
