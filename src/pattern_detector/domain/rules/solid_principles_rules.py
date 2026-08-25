"""SOLID principles and systems clean code rules for Zig."""

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


class MonolithicStructSrpRule(BaseRule):
    """Detects monolithic structs declaring excessive fields (>= 12), violating SRP."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for s in model.all_structs:
            if s.total_fields_count >= 12:
                evidences = [
                    Evidence(
                        rule_code="SRP_MONOLITHIC_STRUCT",
                        description=f"Struct '{s.name}' declares {s.total_fields_count} fields; consider decomposing into cohesive sub-structs",
                        weight=0.88,
                        location=s.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.MONOLITHIC_STRUCT_SRP,
                        pattern_category=PatternCategory.PRINCIPLE,
                        target_name=s.name,
                        target_kind="struct",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=s.location,
                        evidences=evidences,
                    )
                )
        return detections


class FatVTableInterfaceIspRule(BaseRule):
    """Detects fat VTable structs declaring excessive function pointers (>= 10), violating ISP."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for s in model.all_structs:
            if s.is_vtable:
                fn_count = sum(1 for f in s.fields if "fn(" in f.type_name or "*const fn" in f.type_name)
                if fn_count >= 10:
                    evidences = [
                        Evidence(
                            rule_code="ISP_FAT_VTABLE_INTERFACE",
                            description=f"VTable struct '{s.name}' defines {fn_count} function pointers; decompose into specialized role interfaces",
                            weight=0.88,
                            location=s.location,
                        )
                    ]
                    detections.append(
                        Detection(
                            pattern_type=PatternType.FAT_VTABLE_INTERFACE_ISP,
                            pattern_category=PatternCategory.PRINCIPLE,
                            target_name=s.name,
                            target_kind="struct",
                            confidence=Confidence(score=0.88, evidences=evidences),
                            primary_location=s.location,
                            evidences=evidences,
                        )
                    )
        return detections


class ManualTypeSwitchOcpRule(BaseRule):
    """Detects monolithic switch statements (>= 8 prongs) violating Open-Closed Principle."""

    PRONG_PATTERN = re.compile(r"^\s*[a-zA-Z0-9_.,\s|.]+\s*=>\s*", re.MULTILINE)

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            matches = len(self.PRONG_PATTERN.findall(fn.body or ""))
            if matches >= 8 and "switch (" in fn.body:
                evidences = [
                    Evidence(
                        rule_code="OCP_MANUAL_TYPE_SWITCH",
                        description=f"Function '{fn.name}' contains {matches} switch prongs; refactor with comptime generic dispatch or VTable polymorphism",
                        weight=0.88,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.MANUAL_TYPE_SWITCH_OCP,
                        pattern_category=PatternCategory.PRINCIPLE,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections
