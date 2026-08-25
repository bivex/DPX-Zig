"""Resilience, Memory Safety, and Low-Level Hazards detection rules for Zig."""

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


class UnhandledErrorUnionCatchHazardRule(BaseRule):
    """Detects silent error suppression via '_ = func() catch {}' without recovery or logging."""

    EMPTY_CATCH_PATTERN = re.compile(r"catch\s*\{(?:\s*)\}")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if self.EMPTY_CATCH_PATTERN.search(fn.body or ""):
                evidences = [
                    Evidence(
                        rule_code="HAZARD_UNHANDLED_ERROR_CATCH",
                        description=f"Function '{fn.name}' silently swallows error union via empty 'catch {{}}' block; handle or propagate explicitly",
                        weight=0.88,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.UNHANDLED_ERROR_UNION_CATCH_HAZARD,
                        pattern_category=PatternCategory.RESILIENCE,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class MissingDeferDeinitLeakRule(BaseRule):
    """Detects heap struct initialization without matching 'defer deinit()' cleanup."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            has_init = (".init(" in fn.body or "allocator.alloc(" in fn.body or "allocator.create(" in fn.body)
            has_cleanup = (fn.defers_count >= 1 or fn.errdefers_count >= 1 or "deinit" in fn.name or "init" in fn.name or "deinit()" in fn.body)
            if has_init and not has_cleanup and fn.return_type == "void":
                evidences = [
                    Evidence(
                        rule_code="HAZARD_MISSING_DEFER_DEINIT",
                        description=f"Function '{fn.name}' initializes heap resource or struct without matching 'defer deinit()' / 'defer free()', causing potential memory leak",
                        weight=0.85,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.MISSING_DEFER_DEINIT_LEAK,
                        pattern_category=PatternCategory.RESILIENCE,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.85, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class UnreachablePanicInProductionRule(BaseRule):
    """Detects 'unreachable' or '@panic()' statements in reachable code paths."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if fn.has_unreachable or fn.has_panic or re.search(r"\b(unreachable|@panic\s*\()\b", fn.body or ""):
                kind = "@panic" if (fn.has_panic or "@panic" in fn.body) else "unreachable"
                evidences = [
                    Evidence(
                        rule_code="HAZARD_UNREACHABLE_PANIC",
                        description=f"Function '{fn.name}' contains '{kind}'; replace with explicit error union return to prevent undefined behavior in ReleaseFast",
                        weight=0.90,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.UNREACHABLE_PANIC_IN_PRODUCTION,
                        pattern_category=PatternCategory.RESILIENCE,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.90, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class RawPointerAlignmentHazardRule(BaseRule):
    """Detects unchecked '@ptrCast' or '@alignCast' without safety verification."""

    PTR_CAST_PATTERN = re.compile(r"@(?:ptrCast|alignCast)\s*\(")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if fn.has_ptrcast or self.PTR_CAST_PATTERN.search(fn.body or ""):
                evidences = [
                    Evidence(
                        rule_code="HAZARD_RAW_POINTER_ALIGNMENT",
                        description=f"Function '{fn.name}' performs raw pointer reinterpretation via '@ptrCast' / '@alignCast'",
                        weight=0.85,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.RAW_POINTER_ALIGNMENT_HAZARD,
                        pattern_category=PatternCategory.RESILIENCE,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.85, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections
