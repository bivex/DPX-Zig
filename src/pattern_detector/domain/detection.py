"""Detection models and aggregate reporting for Zig."""

from __future__ import annotations

from dataclasses import dataclass, field
from pattern_detector.domain.pattern import PATTERN_CATALOG
from pattern_detector.domain.value_objects import (
    Confidence,
    ConfidenceLevel,
    Evidence,
    PatternCategory,
    PatternType,
    SourceLocation,
)


@dataclass
class Detection:
    """Individual pattern detection or hazard finding in Zig."""

    pattern_type: PatternType
    pattern_category: PatternCategory
    target_name: str
    target_kind: str  # "struct", "union", "enum", "fn", "module", "simd", "comptime"
    confidence: Confidence
    primary_location: SourceLocation | None = None
    related_locations: list[SourceLocation] = field(default_factory=list)
    evidences: list[Evidence] = field(default_factory=list)

    @property
    def level(self) -> ConfidenceLevel:
        return self.confidence.level

    @property
    def summary(self) -> str:
        pdef = PATTERN_CATALOG.get(self.pattern_type)
        if pdef:
            return pdef.description
        return f"Zig architectural pattern: {self.pattern_type.value}"

    def to_dict(self) -> dict:
        return {
            "pattern_type": self.pattern_type.value,
            "category": self.pattern_category.value,
            "target_name": self.target_name,
            "target_kind": self.target_kind,
            "confidence": {
                "score": self.confidence.score,
                "percentage": self.confidence.percentage_str,
                "level": self.confidence.level.value,
            },
            "location": str(self.primary_location) if self.primary_location else None,
            "related_locations": [str(loc) for loc in self.related_locations],
            "evidences": [
                {
                    "rule_code": ev.rule_code,
                    "description": ev.description,
                    "weight": ev.weight,
                    "location": str(ev.location) if ev.location else None,
                }
                for ev in self.evidences
            ],
            "summary": self.summary,
        }


@dataclass
class DetectionReport:
    """Aggregate scan result containing all detections across a Zig project."""

    project_path: str
    scanned_files_count: int
    detections: list[Detection] = field(default_factory=list)
    elapsed_seconds: float = 0.0

    @property
    def total_detections_count(self) -> int:
        return len(self.detections)

    @property
    def summary_by_category(self) -> dict[str, int]:
        summary: dict[str, int] = {cat.value: 0 for cat in PatternCategory}
        for det in self.detections:
            summary[det.pattern_category.value] = summary.get(det.pattern_category.value, 0) + 1
        return summary

    def to_dict(self) -> dict:
        return {
            "project_path": self.project_path,
            "scanned_files_count": self.scanned_files_count,
            "total_detections_count": self.total_detections_count,
            "elapsed_seconds": round(self.elapsed_seconds, 4),
            "summary_by_category": self.summary_by_category,
            "detections": [d.to_dict() for d in self.detections],
        }
