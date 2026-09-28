from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


FrequencyUnit = Literal["Hz", "kHz", "MHz", "GHz", "hz", "khz", "mhz", "ghz"]

class DesignCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    antenna_type: str = Field(..., min_length=1)
    frequency: float | None = Field(default=None, gt=0)
    frequency_unit: FrequencyUnit = "Hz"
    frequency_hz: float | None = Field(default=None, gt=0)
    application: str | None = None
    polarization: str = "linear"
    max_dimension_m: float | None = Field(default=None, gt=0)
    target_impedance_ohms: float | None = Field(default=None, gt=0)
    mounting: str | None = None
    platform: str | None = None
    gain_db: float | None = Field(default=None, ge=-100, le=100)
    bandwidth_hz: float | None = Field(default=None, gt=0)
    director_count: int | None = Field(default=None, ge=1, le=20)
    director_lengths_m: list[float] | None = None
    element_spacings_m: list[float] | None = None
    reflector_length_m: float | None = Field(default=None, gt=0)
    driven_element_length_m: float | None = Field(default=None, gt=0)
    element_radius_m: float | None = Field(default=None, gt=0)

    @model_validator(mode="after")
    def require_frequency(self) -> "DesignCreateRequest":
        if self.frequency is None and self.frequency_hz is None:
            raise ValueError("Either frequency or frequency_hz is required.")
        if self.director_lengths_m is not None and any(value <= 0 for value in self.director_lengths_m):
            raise ValueError("director_lengths_m values must be greater than zero.")
        if self.element_spacings_m is not None and any(value <= 0 for value in self.element_spacings_m):
            raise ValueError("element_spacings_m values must be greater than zero.")
        return self

    def to_engineering_requirements(self) -> dict[str, Any]:
        payload = self.model_dump(exclude_none=True)
        payload["frequency_hz"] = self.frequency_hz if self.frequency_hz is not None else self.frequency
        payload["frequency_unit"] = "Hz" if self.frequency_hz is not None else self.frequency_unit
        payload.pop("frequency", None)
        payload.pop("antenna_type", None)
        return payload


class RequirementValidationRequest(DesignCreateRequest):
    pass


class RequirementValidationResponse(BaseModel):
    success: bool = True
    data: dict[str, Any]
