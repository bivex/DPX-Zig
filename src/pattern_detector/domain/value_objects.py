"""Value objects, Enums, and domain primitives for Zig static analysis."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class PatternCategory(str, Enum):
    """Broad architectural classification for Zig patterns and findings."""

    ZIG_IDIOMATIC = "zig_idiomatic"
    SIMD_HARDWARE_SYSTEMS = "simd_hardware_systems"
    COMPTIME_METAPROGRAMMING = "comptime_metaprogramming"
    CREATIONAL = "creational"
    STRUCTURAL = "structural"
    BEHAVIORAL = "behavioral"
    RESILIENCE = "resilience"
    PRINCIPLE = "principle"


class PatternType(str, Enum):
    """Exhaustive catalog of Zig patterns, hardware signals, and safety hazards."""

    # 1. Zig Idiomatic & Systems Architecture (6)
    EXPLICIT_ALLOCATOR_PASSING = "explicit_allocator_passing"
    DEFER_ERRDEFER_RAII = "defer_errdefer_raii"
    ERROR_UNION_TRY_CATCH = "error_union_try_catch"
    TAGGED_UNION_EXHAUSTIVE_SWITCH = "tagged_union_exhaustive_switch"
    PACKED_EXTERN_STRUCT_LAYOUT = "packed_extern_struct_layout"
    OPAQUE_TYPE_C_HANDLE = "opaque_type_c_handle"

    # 2. Comptime & Metaprogramming (4)
    COMPTIME_GENERIC_TYPE_FUNCTION = "comptime_generic_type_function"
    COMPTIME_TYPEINFO_REFLECTION = "comptime_typeinfo_reflection"
    COMPTIME_STATIC_ASSERTION = "comptime_static_assertion"
    INLINE_FOR_WHILE_EXPANSION = "inline_for_while_expansion"

    # 3. SIMD, Concurrency & Low-Level Hardware (3)
    SIMD_VECTOR_ACCELERATION = "simd_vector_acceleration"
    INLINE_ASSEMBLY_INTRINSIC = "inline_assembly_intrinsic"
    C_INTEROP_TRANSLATE_C = "c_interop_translate_c"

    # 4. Creational Patterns (5/5)
    SINGLETON_GLOBAL_INSTANCE = "singleton_global_instance"
    FACTORY_INIT_ALLOCATOR = "factory_init_allocator"
    ABSTRACT_FACTORY_VTABLE_INTERFACE = "abstract_factory_vtable_interface"
    BUILDER_CONFIGURATION_FLOW = "builder_configuration_flow"
    PROTOTYPE_COMPTIME_CLONE = "prototype_comptime_clone"

    # 5. Structural Patterns (7/7)
    ADAPTER_WRAPPER_TYPE = "adapter_wrapper_type"
    BRIDGE_VTABLE_DRIVER = "bridge_vtable_driver"
    COMPOSITE_RECURSIVE_TAGGED_UNION = "composite_recursive_tagged_union"
    DECORATOR_ALLOCATOR_WRAPPER = "decorator_allocator_wrapper"
    FACADE_ROOT_MODULE_API = "facade_root_module_api"
    FLYWEIGHT_STATIC_INTERN_POOL = "flyweight_static_intern_pool"
    PROXY_VTABLE_GATEWAY = "proxy_vtable_gateway"

    # 6. Behavioral Patterns (11/11)
    CHAIN_OF_RESPONSIBILITY_PIPELINE = "chain_of_responsibility_pipeline"
    COMMAND_TAGGED_ACTION_PAYLOAD = "command_tagged_action_payload"
    INTERPRETER_AST_SWITCH_EVAL = "interpreter_ast_switch_eval"
    ITERATOR_STRUCT_NEXT = "iterator_struct_next"
    MEDIATOR_EVENT_BUS = "mediator_event_bus"
    MEMENTO_STATE_SNAPSHOT = "memento_state_snapshot"
    OBSERVER_CALLBACK_SUBSCRIPTION = "observer_callback_subscription"
    STATE_MACHINE_TAGGED_UNION_FSM = "state_machine_tagged_union_fsm"
    STRATEGY_FUNCTION_POINTER_INJECTION = "strategy_function_pointer_injection"
    TEMPLATE_METHOD_SKELETON_HOOKS = "template_method_skeleton_hooks"
    VISITOR_SWITCH_PAYLOAD_WALKER = "visitor_switch_payload_walker"

    # 7. Safety, Memory & Concurrency Hazards (4)
    UNHANDLED_ERROR_UNION_CATCH_HAZARD = "unhandled_error_union_catch_hazard"
    MISSING_DEFER_DEINIT_LEAK = "missing_defer_deinit_leak"
    UNREACHABLE_PANIC_IN_PRODUCTION = "unreachable_panic_in_production"
    RAW_POINTER_ALIGNMENT_HAZARD = "raw_pointer_alignment_hazard"

    # 8. SOLID & Clean Code Quality (3)
    MONOLITHIC_STRUCT_SRP = "monolithic_struct_srp"
    FAT_VTABLE_INTERFACE_ISP = "fat_vtable_interface_isp"
    MANUAL_TYPE_SWITCH_OCP = "manual_type_switch_ocp"


class ConfidenceLevel(str, Enum):
    """Categorical confidence level ranking."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"


@dataclass(frozen=True)
class SourceLocation:
    """Precise source code location in a Zig file."""

    file_path: str
    line: int
    column: int = 1

    def __str__(self) -> str:
        return f"{self.file_path}:{self.line}:{self.column}"


@dataclass
class Evidence:
    """Individual heuristic or signal contributing to pattern detection."""

    rule_code: str
    description: str
    weight: float
    location: SourceLocation | None = None


@dataclass
class Confidence:
    """Aggregated detection confidence score and heuristic evidence trail."""

    score: float
    evidences: list[Evidence] = field(default_factory=list)

    @property
    def level(self) -> ConfidenceLevel:
        if self.score >= 0.85:
            return ConfidenceLevel.VERY_HIGH
        if self.score >= 0.70:
            return ConfidenceLevel.HIGH
        if self.score >= 0.50:
            return ConfidenceLevel.MEDIUM
        return ConfidenceLevel.LOW

    @property
    def percentage_str(self) -> str:
        return f"{int(round(self.score * 100))}%"
