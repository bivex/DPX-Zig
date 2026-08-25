"""Rules registry and aggregation factory for Zig pattern detector."""

from __future__ import annotations

from pattern_detector.domain.rules.base import BaseRule
from pattern_detector.domain.rules.behavioral_rules import (
    ChainOfResponsibilityPipelineRule,
    CommandTaggedActionPayloadRule,
    InterpreterAstSwitchEvalRule,
    IteratorStructNextRule,
    MediatorEventBusRule,
    MementoStateSnapshotRule,
    ObserverCallbackSubscriptionRule,
    StateMachineTaggedUnionFsmRule,
    StrategyFunctionPointerInjectionRule,
    TemplateMethodSkeletonHooksRule,
    VisitorSwitchPayloadWalkerRule,
)
from pattern_detector.domain.rules.comptime_rules import (
    ComptimeGenericTypeFunctionRule,
    ComptimeStaticAssertionRule,
    ComptimeTypeInfoReflectionRule,
    InlineForWhileExpansionRule,
)
from pattern_detector.domain.rules.creational_rules import (
    AbstractFactoryVTableInterfaceRule,
    BuilderConfigurationFlowRule,
    FactoryInitAllocatorRule,
    PrototypeComptimeCloneRule,
    SingletonGlobalInstanceRule,
)
from pattern_detector.domain.rules.idiomatic_rules import (
    DeferErrdeferRaiiRule,
    ErrorUnionTryCatchRule,
    ExplicitAllocatorPassingRule,
    OpaqueTypeCHandleRule,
    PackedExternStructLayoutRule,
    TaggedUnionExhaustiveSwitchRule,
)
from pattern_detector.domain.rules.resilience_hazards_rules import (
    MissingDeferDeinitLeakRule,
    RawPointerAlignmentHazardRule,
    UnhandledErrorUnionCatchHazardRule,
    UnreachablePanicInProductionRule,
)
from pattern_detector.domain.rules.simd_hardware_rules import (
    CInteropTranslateCRule,
    InlineAssemblyIntrinsicRule,
    SimdVectorAccelerationRule,
)
from pattern_detector.domain.rules.solid_principles_rules import (
    FatVTableInterfaceIspRule,
    ManualTypeSwitchOcpRule,
    MonolithicStructSrpRule,
)
from pattern_detector.domain.rules.structural_rules import (
    AdapterWrapperTypeRule,
    BridgeVTableDriverRule,
    CompositeRecursiveTaggedUnionRule,
    DecoratorAllocatorWrapperRule,
    FacadeRootModuleApiRule,
    FlyweightStaticInternPoolRule,
    ProxyVTableGatewayRule,
)

DEFAULT_RULES: list[type[BaseRule]] = [
    # 1. Zig Idiomatic & Systems Architecture (6)
    ExplicitAllocatorPassingRule,
    DeferErrdeferRaiiRule,
    ErrorUnionTryCatchRule,
    TaggedUnionExhaustiveSwitchRule,
    PackedExternStructLayoutRule,
    OpaqueTypeCHandleRule,

    # 2. Comptime & Metaprogramming (4)
    ComptimeGenericTypeFunctionRule,
    ComptimeTypeInfoReflectionRule,
    ComptimeStaticAssertionRule,
    InlineForWhileExpansionRule,

    # 3. SIMD, Concurrency & Low-Level Hardware (3)
    SimdVectorAccelerationRule,
    InlineAssemblyIntrinsicRule,
    CInteropTranslateCRule,

    # 4. Creational Patterns (5/5)
    SingletonGlobalInstanceRule,
    FactoryInitAllocatorRule,
    AbstractFactoryVTableInterfaceRule,
    BuilderConfigurationFlowRule,
    PrototypeComptimeCloneRule,

    # 5. Structural Patterns (7/7)
    AdapterWrapperTypeRule,
    BridgeVTableDriverRule,
    CompositeRecursiveTaggedUnionRule,
    DecoratorAllocatorWrapperRule,
    FacadeRootModuleApiRule,
    FlyweightStaticInternPoolRule,
    ProxyVTableGatewayRule,

    # 6. Behavioral Patterns (11/11)
    ChainOfResponsibilityPipelineRule,
    CommandTaggedActionPayloadRule,
    InterpreterAstSwitchEvalRule,
    IteratorStructNextRule,
    MediatorEventBusRule,
    MementoStateSnapshotRule,
    ObserverCallbackSubscriptionRule,
    StateMachineTaggedUnionFsmRule,
    StrategyFunctionPointerInjectionRule,
    TemplateMethodSkeletonHooksRule,
    VisitorSwitchPayloadWalkerRule,

    # 7. Safety, Memory & Concurrency Hazards (4)
    UnhandledErrorUnionCatchHazardRule,
    MissingDeferDeinitLeakRule,
    UnreachablePanicInProductionRule,
    RawPointerAlignmentHazardRule,

    # 8. SOLID & Systems Clean Code (3)
    MonolithicStructSrpRule,
    FatVTableInterfaceIspRule,
    ManualTypeSwitchOcpRule,
]


def get_default_rules() -> list[BaseRule]:
    """Instantiate and return full suite of default Zig rules."""
    return [rule_cls() for rule_cls in DEFAULT_RULES]
