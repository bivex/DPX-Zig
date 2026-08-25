"""Zig Idiomatic Systems Architecture detection rules."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BaseRule
from pattern_detector.domain.value_objects import (
    Confidence,
    Evidence,
    PatternCategory,
    PatternType,
)


class ExplicitAllocatorPassingRule(BaseRule):
    """Detects explicit passing of 'allocator: std.mem.Allocator' eliminating hidden allocations."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if fn.accepts_allocator:
                evidences = [
                    Evidence(
                        rule_code="ZIG_EXPLICIT_ALLOCATOR",
                        description=f"Function '{fn.name}' requires explicit 'std.mem.Allocator' parameter, eliminating hidden heap allocations",
                        weight=0.95,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.EXPLICIT_ALLOCATOR_PASSING,
                        pattern_category=PatternCategory.ZIG_IDIOMATIC,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.95, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class DeferErrdeferRaiiRule(BaseRule):
    """Detects deterministic resource deallocation and rollback via 'defer' and 'errdefer'."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if fn.defers_count >= 1 or fn.errdefers_count >= 1:
                desc = (
                    f"Function '{fn.name}' enforces deterministic resource cleanup with {fn.defers_count} 'defer' and {fn.errdefers_count} 'errdefer' rollback statements"
                )
                evidences = [
                    Evidence(
                        rule_code="ZIG_DEFER_ERRDEFER_RAII",
                        description=desc,
                        weight=0.95,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.DEFER_ERRDEFER_RAII,
                        pattern_category=PatternCategory.ZIG_IDIOMATIC,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.95, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class ErrorUnionTryCatchRule(BaseRule):
    """Detects explicit error sets and error unions (!T) with compiler-checked 'try' propagation."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if fn.return_type.startswith("!") or fn.tries_count >= 1 or fn.catches_count >= 1:
                evidences = [
                    Evidence(
                        rule_code="ZIG_ERROR_UNION_TRY",
                        description=f"Function '{fn.name}' implements explicit error set handling via error union '{fn.return_type}' and 'try'/'catch'",
                        weight=0.92,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.ERROR_UNION_TRY_CATCH,
                        pattern_category=PatternCategory.ZIG_IDIOMATIC,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.92, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class TaggedUnionExhaustiveSwitchRule(BaseRule):
    """Detects type-safe sum types ('union(enum)') decomposed via exhaustive 'switch'."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for u in model.all_unions:
            if u.is_tagged:
                evidences = [
                    Evidence(
                        rule_code="ZIG_TAGGED_UNION_SUM_TYPE",
                        description=f"Tagged union '{u.name}' defines type-safe Algebraic Data Type with {len(u.fields)} variant(s) tagged by '{u.tag_type}'",
                        weight=0.95,
                        location=u.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.TAGGED_UNION_EXHAUSTIVE_SWITCH,
                        pattern_category=PatternCategory.ZIG_IDIOMATIC,
                        target_name=u.name,
                        target_kind="union",
                        confidence=Confidence(score=0.95, evidences=evidences),
                        primary_location=u.location,
                        evidences=evidences,
                    )
                )
        return detections


class PackedExternStructLayoutRule(BaseRule):
    """Detects exact bitfield packing ('packed struct') or C ABI compatibility ('extern struct')."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for s in model.all_structs:
            if s.kind in ("packed struct", "extern struct"):
                evidences = [
                    Evidence(
                        rule_code="ZIG_MEMORY_LAYOUT_STRUCT",
                        description=f"Struct '{s.name}' explicitly specifies hardware/ABI memory layout using '{s.kind}'",
                        weight=0.95,
                        location=s.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.PACKED_EXTERN_STRUCT_LAYOUT,
                        pattern_category=PatternCategory.ZIG_IDIOMATIC,
                        target_name=s.name,
                        target_kind="struct",
                        confidence=Confidence(score=0.95, evidences=evidences),
                        primary_location=s.location,
                        evidences=evidences,
                    )
                )
        return detections


class OpaqueTypeCHandleRule(BaseRule):
    """Detects unsized opaque struct ('opaque {}') representing foreign or encapsulated pointers."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for s in model.all_structs:
            if s.kind == "opaque":
                evidences = [
                    Evidence(
                        rule_code="ZIG_OPAQUE_HANDLE",
                        description=f"Type '{s.name}' is declared as 'opaque {{}}' representing an encapsulated foreign/C ABI handle",
                        weight=0.95,
                        location=s.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.OPAQUE_TYPE_C_HANDLE,
                        pattern_category=PatternCategory.ZIG_IDIOMATIC,
                        target_name=s.name,
                        target_kind="struct",
                        confidence=Confidence(score=0.95, evidences=evidences),
                        primary_location=s.location,
                        evidences=evidences,
                    )
                )
        return detections
