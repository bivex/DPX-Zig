"""Zig Comptime Metaprogramming and Reflection rules."""

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


class ComptimeGenericTypeFunctionRule(BaseRule):
    """Detects zero-cost generic type generation functions ('fn (comptime T: type) type')."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if fn.return_type == "type" or any(p.is_comptime and p.type_name == "type" for p in fn.parameters):
                evidences = [
                    Evidence(
                        rule_code="COMPTIME_GENERIC_TYPE_FN",
                        description=f"Function '{fn.name}' generates zero-cost generic types at compile time (returns 'type')",
                        weight=0.95,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.COMPTIME_GENERIC_TYPE_FUNCTION,
                        pattern_category=PatternCategory.COMPTIME_METAPROGRAMMING,
                        target_name=fn.name,
                        target_kind="comptime",
                        confidence=Confidence(score=0.95, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class ComptimeTypeInfoReflectionRule(BaseRule):
    """Detects compile-time type introspection and reflection via '@typeInfo(T)'."""

    TYPEINFO_PATTERN = re.compile(r"@typeInfo\s*\(")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if fn.has_typeinfo or self.TYPEINFO_PATTERN.search(fn.body or ""):
                evidences = [
                    Evidence(
                        rule_code="COMPTIME_TYPEINFO_REFLECTION",
                        description=f"Function '{fn.name}' performs compile-time type reflection and introspection via '@typeInfo'",
                        weight=0.95,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.COMPTIME_TYPEINFO_REFLECTION,
                        pattern_category=PatternCategory.COMPTIME_METAPROGRAMMING,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.95, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class ComptimeStaticAssertionRule(BaseRule):
    """Detects compile-time constraint verification via '@compileError' or '@compileLog'."""

    COMPILE_ERR_PATTERN = re.compile(r"@(compileError|compileLog)\s*\(")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if self.COMPILE_ERR_PATTERN.search(fn.body or ""):
                evidences = [
                    Evidence(
                        rule_code="COMPTIME_STATIC_ASSERT",
                        description=f"Function '{fn.name}' enforces compile-time type and value constraints via '@compileError'",
                        weight=0.92,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.COMPTIME_STATIC_ASSERTION,
                        pattern_category=PatternCategory.COMPTIME_METAPROGRAMMING,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.92, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class InlineForWhileExpansionRule(BaseRule):
    """Detects unrolled compile-time loop evaluation via 'inline for' or 'inline while'."""

    INLINE_LOOP_PATTERN = re.compile(r"\binline\s+(for|while)\b")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if self.INLINE_LOOP_PATTERN.search(fn.body or ""):
                evidences = [
                    Evidence(
                        rule_code="COMPTIME_INLINE_LOOP",
                        description=f"Function '{fn.name}' unrolls loops at compile-time via 'inline for/while'",
                        weight=0.92,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.INLINE_FOR_WHILE_EXPANSION,
                        pattern_category=PatternCategory.COMPTIME_METAPROGRAMMING,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.92, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections
