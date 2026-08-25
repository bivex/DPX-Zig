"""SIMD, Concurrency, and Low-Level Hardware acceleration rules for Zig."""

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


class SimdVectorAccelerationRule(BaseRule):
    """Detects hardware vector parallelism utilizing '@Vector(N, T)' intrinsics."""

    SIMD_PATTERN = re.compile(r"@Vector\s*\(\s*\d+\s*,\s*[a-zA-Z0-9_.]+\s*\)")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if fn.has_simd or self.SIMD_PATTERN.search(fn.body or "") or any("@Vector" in p.type_name for p in fn.parameters):
                evidences = [
                    Evidence(
                        rule_code="SIMD_VECTOR_ACCELERATION",
                        description=f"Function '{fn.name}' executes vectorized SIMD operations using '@Vector' intrinsics",
                        weight=0.95,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.SIMD_VECTOR_ACCELERATION,
                        pattern_category=PatternCategory.SIMD_HARDWARE_SYSTEMS,
                        target_name=fn.name,
                        target_kind="simd",
                        confidence=Confidence(score=0.95, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class InlineAssemblyIntrinsicRule(BaseRule):
    """Detects direct CPU instruction execution via 'asm volatile'."""

    ASM_PATTERN = re.compile(r"\basm\s+(volatile\s*)?\(")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if fn.has_inline_asm or self.ASM_PATTERN.search(fn.body or ""):
                evidences = [
                    Evidence(
                        rule_code="HARDWARE_INLINE_ASM",
                        description=f"Function '{fn.name}' executes direct CPU machine instructions via inline assembly ('asm volatile')",
                        weight=0.95,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.INLINE_ASSEMBLY_INTRINSIC,
                        pattern_category=PatternCategory.SIMD_HARDWARE_SYSTEMS,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.95, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class CInteropTranslateCRule(BaseRule):
    """Detects seamless C header translation via '@cImport' and '@cInclude'."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for imp in model.all_imports:
            if imp.is_c_import:
                evidences = [
                    Evidence(
                        rule_code="C_INTEROP_TRANSLATE_C",
                        description=f"Direct C ABI translation binding imported from '{imp.path_or_pkg}' via '@cImport'",
                        weight=0.95,
                        location=imp.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.C_INTEROP_TRANSLATE_C,
                        pattern_category=PatternCategory.SIMD_HARDWARE_SYSTEMS,
                        target_name=imp.alias or imp.path_or_pkg,
                        target_kind="module",
                        confidence=Confidence(score=0.95, evidences=evidences),
                        primary_location=imp.location,
                        evidences=evidences,
                    )
                )
        return detections
