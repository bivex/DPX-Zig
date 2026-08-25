"""GoF Structural design pattern detection rules for Zig (7/7)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BaseRule
from pattern_detector.domain.value_objects import (
    Confidence,
    Evidence,
    PatternCategory,
    PatternType,
)


class AdapterWrapperTypeRule(BaseRule):
    """Detects Adapter pattern wrapping third-party or foreign C structures."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for s in model.all_structs:
            if "Adapter" in s.name or "Wrapper" in s.name:
                evidences = [
                    Evidence(
                        rule_code="STRUCTURAL_ADAPTER",
                        description=f"Struct '{s.name}' adapts external or low-level types to idiomatic Zig interface contracts",
                        weight=0.88,
                        location=s.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.ADAPTER_WRAPPER_TYPE,
                        pattern_category=PatternCategory.STRUCTURAL,
                        target_name=s.name,
                        target_kind="struct",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=s.location,
                        evidences=evidences,
                    )
                )
        return detections


class BridgeVTableDriverRule(BaseRule):
    """Detects Bridge pattern decoupling domain logic from platform hardware drivers via VTable."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for s in model.all_structs:
            has_driver = any("Driver" in f.type_name or "Backend" in f.type_name or "Engine" in f.type_name or "vtable" in f.name.lower() for f in s.fields)
            if (has_driver and not s.is_vtable) or "Bridge" in s.name:
                evidences = [
                    Evidence(
                        rule_code="STRUCTURAL_BRIDGE_DRIVER",
                        description=f"Struct '{s.name}' decouples high-level abstraction from platform driver implementors via VTable bridge",
                        weight=0.88,
                        location=s.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.BRIDGE_VTABLE_DRIVER,
                        pattern_category=PatternCategory.STRUCTURAL,
                        target_name=s.name,
                        target_kind="struct",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=s.location,
                        evidences=evidences,
                    )
                )
        return detections


class CompositeRecursiveTaggedUnionRule(BaseRule):
    """Detects Composite recursive AST or tree hierarchies in tagged unions."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for u in model.all_unions:
            is_recursive = any(u.name in f.type_name or "[]" in f.type_name for f in u.fields)
            if (is_recursive and u.is_tagged) or "Tree" in u.name or "Composite" in u.name:
                evidences = [
                    Evidence(
                        rule_code="STRUCTURAL_COMPOSITE_UNION",
                        description=f"Tagged union '{u.name}' implements Composite pattern with recursive tree/AST node variants",
                        weight=0.92,
                        location=u.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.COMPOSITE_RECURSIVE_TAGGED_UNION,
                        pattern_category=PatternCategory.STRUCTURAL,
                        target_name=u.name,
                        target_kind="union",
                        confidence=Confidence(score=0.92, evidences=evidences),
                        primary_location=u.location,
                        evidences=evidences,
                    )
                )
        return detections


class DecoratorAllocatorWrapperRule(BaseRule):
    """Detects Decorator pattern wrapping an Allocator or Reader/Writer stream."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for s in model.all_structs:
            wraps_alloc = any("Allocator" in f.type_name or "child_allocator" in f.name for f in s.fields)
            wraps_stream = any("reader" in f.name or "writer" in f.name for f in s.fields)
            if wraps_alloc or (wraps_stream and ("Decorator" in s.name or "Logging" in s.name or "Counting" in s.name)):
                evidences = [
                    Evidence(
                        rule_code="STRUCTURAL_DECORATOR_WRAPPER",
                        description=f"Struct '{s.name}' decorates and augments an underlying Allocator/Stream with cross-cutting behavior",
                        weight=0.90,
                        location=s.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.DECORATOR_ALLOCATOR_WRAPPER,
                        pattern_category=PatternCategory.STRUCTURAL,
                        target_name=s.name,
                        target_kind="struct",
                        confidence=Confidence(score=0.90, evidences=evidences),
                        primary_location=s.location,
                        evidences=evidences,
                    )
                )
        return detections


class FacadeRootModuleApiRule(BaseRule):
    """Detects Facade module APIs exposing unified root namespaces (root.zig or main.zig)."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for f in model.files:
            pub_fns = [fn for fn in f.functions if fn.is_pub]
            pub_structs = [s for s in f.structs if s.is_pub]
            if (len(pub_fns) + len(pub_structs)) >= 6:
                module_name = f.file_path.split("/")[-1].replace(".zig", "")
                evidences = [
                    Evidence(
                        rule_code="STRUCTURAL_FACADE_MODULE",
                        description=f"Module '{module_name}' acts as a unified Facade API exposing {len(pub_fns)} public function(s) and {len(pub_structs)} public struct(s)",
                        weight=0.85,
                        location=pub_fns[0].location if pub_fns else (pub_structs[0].location if pub_structs else None),
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.FACADE_ROOT_MODULE_API,
                        pattern_category=PatternCategory.STRUCTURAL,
                        target_name=module_name,
                        target_kind="module",
                        confidence=Confidence(score=0.85, evidences=evidences),
                        primary_location=pub_fns[0].location if pub_fns else None,
                        evidences=evidences,
                    )
                )
        return detections


class FlyweightStaticInternPoolRule(BaseRule):
    """Detects Flyweight pattern sharing pre-allocated string intern tables or cached objects."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for s in model.all_structs:
            if "Pool" in s.name or "Intern" in s.name or "Flyweight" in s.name or "Cache" in s.name:
                evidences = [
                    Evidence(
                        rule_code="STRUCTURAL_FLYWEIGHT_POOL",
                        description=f"Struct '{s.name}' implements Flyweight memory pool sharing pre-allocated terms",
                        weight=0.88,
                        location=s.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.FLYWEIGHT_STATIC_INTERN_POOL,
                        pattern_category=PatternCategory.STRUCTURAL,
                        target_name=s.name,
                        target_kind="struct",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=s.location,
                        evidences=evidences,
                    )
                )
        return detections


class ProxyVTableGatewayRule(BaseRule):
    """Detects Proxy pattern acting as a surrogate for underlying VTable resources."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for s in model.all_structs:
            if "Proxy" in s.name or "Gateway" in s.name or "Client" in s.name:
                evidences = [
                    Evidence(
                        rule_code="STRUCTURAL_PROXY_GATEWAY",
                        description=f"Struct '{s.name}' acts as a Proxy Gateway controlling access to underlying hardware/network resources",
                        weight=0.88,
                        location=s.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.PROXY_VTABLE_GATEWAY,
                        pattern_category=PatternCategory.STRUCTURAL,
                        target_name=s.name,
                        target_kind="struct",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=s.location,
                        evidences=evidences,
                    )
                )
        return detections
