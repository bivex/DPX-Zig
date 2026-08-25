"""GoF Creational design pattern detection rules for Zig (5/5)."""

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


class SingletonGlobalInstanceRule(BaseRule):
    """Detects Singleton global state or thread-local registries."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for s in model.all_structs:
            if "Singleton" in s.name or "Registry" in s.name or "Global" in s.name:
                evidences = [
                    Evidence(
                        rule_code="CREATIONAL_SINGLETON",
                        description=f"Struct '{s.name}' implements Singleton / global coordinator pattern",
                        weight=0.88,
                        location=s.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.SINGLETON_GLOBAL_INSTANCE,
                        pattern_category=PatternCategory.CREATIONAL,
                        target_name=s.name,
                        target_kind="struct",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=s.location,
                        evidences=evidences,
                    )
                )
        return detections


class FactoryInitAllocatorRule(BaseRule):
    """Detects Factory Init Constructor ('pub fn init(allocator: Allocator, ...)') pattern."""

    FACTORY_NAME_PATTERN = re.compile(r"^(init|create|open|from[A-Z0-9_].*)$")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if self.FACTORY_NAME_PATTERN.match(fn.name) and (fn.accepts_allocator or fn.return_type not in ("void", "Nil")):
                evidences = [
                    Evidence(
                        rule_code="CREATIONAL_FACTORY_INIT",
                        description=f"Function '{fn.name}' implements Factory Init Constructor allocating and initializing resources",
                        weight=0.92,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.FACTORY_INIT_ALLOCATOR,
                        pattern_category=PatternCategory.CREATIONAL,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.92, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class AbstractFactoryVTableInterfaceRule(BaseRule):
    """Detects Abstract Factory interface returning polymorphic allocators or driver families."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for s in model.all_structs:
            if (s.is_vtable and "Factory" in s.name) or "Provider" in s.name or (s.is_vtable and any("create" in f.name or "init" in f.name for f in s.fields)):
                evidences = [
                    Evidence(
                        rule_code="CREATIONAL_ABSTRACT_FACTORY_VTABLE",
                        description=f"Struct '{s.name}' defines an Abstract Factory VTable contract producing polymorphic driver families",
                        weight=0.90,
                        location=s.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.ABSTRACT_FACTORY_VTABLE_INTERFACE,
                        pattern_category=PatternCategory.CREATIONAL,
                        target_name=s.name,
                        target_kind="struct",
                        confidence=Confidence(score=0.90, evidences=evidences),
                        primary_location=s.location,
                        evidences=evidences,
                    )
                )
        return detections


class BuilderConfigurationFlowRule(BaseRule):
    """Detects Builder pattern chaining configuration methods returning 'Self'."""

    BUILDER_METHOD = re.compile(r"^(set|with|add)[A-Z0-9_]")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if self.BUILDER_METHOD.match(fn.name) or "Builder" in fn.name:
                evidences = [
                    Evidence(
                        rule_code="CREATIONAL_BUILDER_FLOW",
                        description=f"Function '{fn.name}' implements Builder configuration flow chaining struct parameters",
                        weight=0.88,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.BUILDER_CONFIGURATION_FLOW,
                        pattern_category=PatternCategory.CREATIONAL,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class PrototypeComptimeCloneRule(BaseRule):
    """Detects Prototype deep memory cloning via an explicit allocator."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if fn.name in ("clone", "duplicate", "copy") and fn.accepts_allocator:
                evidences = [
                    Evidence(
                        rule_code="CREATIONAL_PROTOTYPE_CLONE",
                        description=f"Function '{fn.name}' implements Prototype pattern for deep cloning buffers via allocator",
                        weight=0.90,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.PROTOTYPE_COMPTIME_CLONE,
                        pattern_category=PatternCategory.CREATIONAL,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.90, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections
