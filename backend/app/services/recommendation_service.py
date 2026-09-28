from __future__ import annotations

from backend.app.models.requirement import AntennaRequirement, RecommendationCandidate


class RecommendationService:
    """Scores candidate antenna families from structured requirements."""

    def recommend(self, requirement: AntennaRequirement) -> list[RecommendationCandidate]:
        directional = bool(requirement.is_directional)
        gain = float(requirement.gain_db or 0.0)
        size_budget = float(requirement.max_dimension_m or 1.0)

        candidates: list[tuple[str, float, list[str]]] = []

        if directional and gain >= 6.0 and size_budget > 0.2:
            candidates.append(("yagi_uda", 0.96, ["Strong directional gain is a priority.", "This design fits a larger directional payload."]))
        elif directional and gain >= 3.0:
            candidates.append(("monopole", 0.80, ["Directional use with moderate gain is supported.", "Simple vertical geometry remains practical."]))
        else:
            candidates.append(("dipole", 0.84, ["Balanced broadband response for a compact general-purpose design.", "Good compromise for moderate gain and simple feeding."]))

        if requirement.application.lower().find("rocket") >= 0 or requirement.application.lower().find("telemetry") >= 0:
            candidates.append(("dipole", 0.71, ["Simple resonant structure helps with rapid deployment."]))

        if requirement.application.lower().find("iot") >= 0 or requirement.application.lower().find("sensor") >= 0:
            candidates.append(("monopole", 0.88, ["Compact and practical for embedded or handheld systems."]))

        if directional and size_budget > 0.3:
            candidates.append(("yagi_uda", 0.90, ["Directional structure is favored when space allows."]))

        deduped: list[tuple[str, float, list[str]]] = []
        seen: set[str] = set()
        for family, score, reasons in candidates:
            if family in seen:
                continue
            seen.add(family)
            deduped.append((family, score, reasons))

        result: list[RecommendationCandidate] = []
        for family, score, reasons in sorted(deduped, key=lambda item: item[1], reverse=True):
            result.append(
                RecommendationCandidate(
                    family=family,
                    score=score,
                    reasons=reasons,
                    alternatives=[item[0] for item in deduped if item[0] != family],
                )
            )

        return result
