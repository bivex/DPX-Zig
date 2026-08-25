"""Comprehensive pattern catalog and metadata for Zig static analysis."""

from __future__ import annotations

from dataclasses import dataclass
from pattern_detector.domain.value_objects import PatternCategory, PatternType


@dataclass(frozen=True)
class PatternDefinition:
    """Detailed architectural specification of a Zig pattern or hazard."""

    type: PatternType
    category: PatternCategory
    name: str
    description: str
    zig_version: str = "0.11 - 0.14+"
    recommendation: str = ""


PATTERN_CATALOG: dict[PatternType, PatternDefinition] = {
    # 1. Zig Idiomatic & Systems Architecture
    PatternType.EXPLICIT_ALLOCATOR_PASSING: PatternDefinition(
        type=PatternType.EXPLICIT_ALLOCATOR_PASSING,
        category=PatternCategory.ZIG_IDIOMATIC,
        name="Explicit Allocator Passing",
        description="Explicit passing of 'allocator: std.mem.Allocator' eliminating hidden allocations.",
        recommendation="Adhere to Zig's core philosophy: zero hidden control flow and explicit allocation ownership.",
    ),
    PatternType.DEFER_ERRDEFER_RAII: PatternDefinition(
        type=PatternType.DEFER_ERRDEFER_RAII,
        category=PatternCategory.ZIG_IDIOMATIC,
        name="Defer / Errdefer Cleanup RAII",
        description="Deterministic resource deallocation and error rollback via 'defer' and 'errdefer'.",
        recommendation="Use 'defer allocator.free(buf)' immediately after allocation and 'errdefer' for multi-step rollback.",
    ),
    PatternType.ERROR_UNION_TRY_CATCH: PatternDefinition(
        type=PatternType.ERROR_UNION_TRY_CATCH,
        category=PatternCategory.ZIG_IDIOMATIC,
        name="Error Union & Try/Catch Flow",
        description="Explicit error sets and error unions (!T) with compiler-checked 'try' propagation.",
        recommendation="Return specific error sets (e.g. error{OutOfMemory, InvalidInput}) rather than generic anyerror.",
    ),
    PatternType.TAGGED_UNION_EXHAUSTIVE_SWITCH: PatternDefinition(
        type=PatternType.TAGGED_UNION_EXHAUSTIVE_SWITCH,
        category=PatternCategory.ZIG_IDIOMATIC,
        name="Tagged Union Exhaustive Switch",
        description="Type-safe sum types ('union(enum)') decomposed via compiler-enforced exhaustive 'switch'.",
        recommendation="Prefer tagged unions over untagged unions or raw void pointers for type-safe variants.",
    ),
    PatternType.PACKED_EXTERN_STRUCT_LAYOUT: PatternDefinition(
        type=PatternType.PACKED_EXTERN_STRUCT_LAYOUT,
        category=PatternCategory.ZIG_IDIOMATIC,
        name="Packed / Extern Struct Memory Layout",
        description="Exact bitfield packing ('packed struct') or C ABI compatibility ('extern struct').",
        recommendation="Use packed structs for MMIO hardware registers and extern structs for C library interop.",
    ),
    PatternType.OPAQUE_TYPE_C_HANDLE: PatternDefinition(
        type=PatternType.OPAQUE_TYPE_C_HANDLE,
        category=PatternCategory.ZIG_IDIOMATIC,
        name="Opaque Type C Handle",
        description="Unsized opaque struct ('opaque {}') representing foreign or encapsulated pointers.",
        recommendation="Use opaque pointers to hide internal representation across FFI ABI boundaries.",
    ),

    # 2. Comptime & Metaprogramming
    PatternType.COMPTIME_GENERIC_TYPE_FUNCTION: PatternDefinition(
        type=PatternType.COMPTIME_GENERIC_TYPE_FUNCTION,
        category=PatternCategory.COMPTIME_METAPROGRAMMING,
        name="Comptime Generic Type Function",
        description="Zero-cost generic type generation using compile-time functions ('fn ArrayList(comptime T: type) type').",
        recommendation="Leverage comptime generic functions instead of C++ templates or macros for type-safe data structures.",
    ),
    PatternType.COMPTIME_TYPEINFO_REFLECTION: PatternDefinition(
        type=PatternType.COMPTIME_TYPEINFO_REFLECTION,
        category=PatternCategory.COMPTIME_METAPROGRAMMING,
        name="Comptime @typeInfo Reflection",
        description="Compile-time type introspection and structural serialization via '@typeInfo(T)'.",
        recommendation="Utilize @typeInfo for zero-overhead JSON serialization, print formatting, and struct validation.",
    ),
    PatternType.COMPTIME_STATIC_ASSERTION: PatternDefinition(
        type=PatternType.COMPTIME_STATIC_ASSERTION,
        category=PatternCategory.COMPTIME_METAPROGRAMMING,
        name="Comptime Static Assertion",
        description="Compile-time constraint verification via '@compileError' or '@compileLog'.",
        recommendation="Assert struct sizes and type capabilities at compile time to eliminate runtime checks.",
    ),
    PatternType.INLINE_FOR_WHILE_EXPANSION: PatternDefinition(
        type=PatternType.INLINE_FOR_WHILE_EXPANSION,
        category=PatternCategory.COMPTIME_METAPROGRAMMING,
        name="Inline Loop Metaprogramming",
        description="Unrolled compile-time loop evaluation over struct fields via 'inline for' or 'inline while'.",
        recommendation="Use 'inline for' over std.meta.fields(T) to generate specialized unrolled machine code.",
    ),

    # 3. SIMD, Concurrency & Low-Level Hardware
    PatternType.SIMD_VECTOR_ACCELERATION: PatternDefinition(
        type=PatternType.SIMD_VECTOR_ACCELERATION,
        category=PatternCategory.SIMD_HARDWARE_SYSTEMS,
        name="SIMD Vector Hardware Acceleration",
        description="Hardware vector parallelism utilizing '@Vector(N, T)' intrinsics and vector operations.",
        recommendation="Use @Vector for high-throughput math, audio DSP, ray tracing, and tensor compute kernels.",
    ),
    PatternType.INLINE_ASSEMBLY_INTRINSIC: PatternDefinition(
        type=PatternType.INLINE_ASSEMBLY_INTRINSIC,
        category=PatternCategory.SIMD_HARDWARE_SYSTEMS,
        name="Inline Assembly & Hardware Intrinsics",
        description="Direct CPU instruction execution via 'asm volatile' for low-level OS/hardware control.",
        recommendation="Wrap inline assembly in safe architecture-abstracted helper functions.",
    ),
    PatternType.C_INTEROP_TRANSLATE_C: PatternDefinition(
        type=PatternType.C_INTEROP_TRANSLATE_C,
        category=PatternCategory.SIMD_HARDWARE_SYSTEMS,
        name="Direct C Interoperability (@cImport)",
        description="Seamless C header translation without glue code via '@cImport' and '@cInclude'.",
        recommendation="Isolate @cImport bindings into dedicated wrapper modules with idiomatic Zig error handling.",
    ),

    # 4. Creational Patterns (5/5)
    PatternType.SINGLETON_GLOBAL_INSTANCE: PatternDefinition(
        type=PatternType.SINGLETON_GLOBAL_INSTANCE,
        category=PatternCategory.CREATIONAL,
        name="Singleton Global Instance",
        description="Thread-safe or comptime initialized global singleton state.",
        recommendation="Prefer passing dependencies explicitly over accessing global mutable state.",
    ),
    PatternType.FACTORY_INIT_ALLOCATOR: PatternDefinition(
        type=PatternType.FACTORY_INIT_ALLOCATOR,
        category=PatternCategory.CREATIONAL,
        name="Factory Init Allocator",
        description="Struct constructor function ('pub fn init(allocator: Allocator, ...)') initializing instance resources.",
        recommendation="Provide matching 'deinit(self: *Self)' for clean symmetrical lifecycle management.",
    ),
    PatternType.ABSTRACT_FACTORY_VTABLE_INTERFACE: PatternDefinition(
        type=PatternType.ABSTRACT_FACTORY_VTABLE_INTERFACE,
        category=PatternCategory.CREATIONAL,
        name="Abstract Factory VTable Interface",
        description="Polymorphic factory interface producing family of related drivers or allocators via VTable pointers.",
        recommendation="Use VTable structs when runtime polymorphism of allocators/engines is required.",
    ),
    PatternType.BUILDER_CONFIGURATION_FLOW: PatternDefinition(
        type=PatternType.BUILDER_CONFIGURATION_FLOW,
        category=PatternCategory.CREATIONAL,
        name="Builder Configuration Flow",
        description="Fluent struct builder pattern chaining configuration methods returning 'Self'.",
        recommendation="Use builder structs when initializing complex options with sensible defaults.",
    ),
    PatternType.PROTOTYPE_COMPTIME_CLONE: PatternDefinition(
        type=PatternType.PROTOTYPE_COMPTIME_CLONE,
        category=PatternCategory.CREATIONAL,
        name="Prototype Memory Clone",
        description="Deep cloning struct buffers or allocations via an explicit allocator.",
        recommendation="Implement 'clone(self: Self, allocator: Allocator) !Self' for deep copies.",
    ),

    # 5. Structural Patterns (7/7)
    PatternType.ADAPTER_WRAPPER_TYPE: PatternDefinition(
        type=PatternType.ADAPTER_WRAPPER_TYPE,
        category=PatternCategory.STRUCTURAL,
        name="Adapter Wrapper Type",
        description="Struct adapting third-party or foreign C structures to idiomatic Zig interfaces.",
        recommendation="Wrap raw C handles in Zig structs that handle lifetime and error mapping.",
    ),
    PatternType.BRIDGE_VTABLE_DRIVER: PatternDefinition(
        type=PatternType.BRIDGE_VTABLE_DRIVER,
        category=PatternCategory.STRUCTURAL,
        name="Bridge VTable Driver",
        description="Decoupling high-level abstraction from platform hardware drivers via VTable dispatch.",
        recommendation="Bridge OS-specific APIs (Linux epoll vs macOS kqueue vs Windows IOCP) behind a unified VTable.",
    ),
    PatternType.COMPOSITE_RECURSIVE_TAGGED_UNION: PatternDefinition(
        type=PatternType.COMPOSITE_RECURSIVE_TAGGED_UNION,
        category=PatternCategory.STRUCTURAL,
        name="Composite Recursive Tagged Union",
        description="Recursive tree or AST structures modeled using tagged unions and child slices.",
        recommendation="Use ArenaAllocator to allocate recursive composite trees for O(1) deallocation.",
    ),
    PatternType.DECORATOR_ALLOCATOR_WRAPPER: PatternDefinition(
        type=PatternType.DECORATOR_ALLOCATOR_WRAPPER,
        category=PatternCategory.STRUCTURAL,
        name="Decorator Allocator / Middleware Wrapper",
        description="Wrapping an underlying Allocator or Reader/Writer to add logging, caching, or bounds checks.",
        recommendation="Follow std.heap.LoggingAllocator design when decorating stream or allocator behavior.",
    ),
    PatternType.FACADE_ROOT_MODULE_API: PatternDefinition(
        type=PatternType.FACADE_ROOT_MODULE_API,
        category=PatternCategory.STRUCTURAL,
        name="Facade Root Module API",
        description="Unified module entrypoint (root.zig) exposing cohesive public namespaces and types.",
        recommendation="Organize complex internal subsystems behind clear 'pub const' exports in root.zig.",
    ),
    PatternType.FLYWEIGHT_STATIC_INTERN_POOL: PatternDefinition(
        type=PatternType.FLYWEIGHT_STATIC_INTERN_POOL,
        category=PatternCategory.STRUCTURAL,
        name="Flyweight Static Intern Pool",
        description="Sharing immutable pre-allocated terms, string intern tables, or memory slab pools.",
        recommendation="Use string intern tables to minimize duplicate heap string allocations.",
    ),
    PatternType.PROXY_VTABLE_GATEWAY: PatternDefinition(
        type=PatternType.PROXY_VTABLE_GATEWAY,
        category=PatternCategory.STRUCTURAL,
        name="Proxy VTable Gateway",
        description="Surrogate struct controlling access, enforcing locks, or buffering calls to an underlying resource.",
        recommendation="Use Proxy structs to transparently enforce thread synchronization around raw resources.",
    ),

    # 6. Behavioral Patterns (11/11)
    PatternType.CHAIN_OF_RESPONSIBILITY_PIPELINE: PatternDefinition(
        type=PatternType.CHAIN_OF_RESPONSIBILITY_PIPELINE,
        category=PatternCategory.BEHAVIORAL,
        name="Chain of Responsibility Pipeline",
        description="Sequential pipeline delegating requests along a linked chain of handler structs.",
        recommendation="Use chained handlers for request parsing, filtering, and authorization layers.",
    ),
    PatternType.COMMAND_TAGGED_ACTION_PAYLOAD: PatternDefinition(
        type=PatternType.COMMAND_TAGGED_ACTION_PAYLOAD,
        category=PatternCategory.BEHAVIORAL,
        name="Command Tagged Action Payload",
        description="Tagged union variants encapsulating action intent and execution arguments.",
        recommendation="Model executable tasks or undoable commands as tagged unions.",
    ),
    PatternType.INTERPRETER_AST_SWITCH_EVAL: PatternDefinition(
        type=PatternType.INTERPRETER_AST_SWITCH_EVAL,
        category=PatternCategory.BEHAVIORAL,
        name="Interpreter AST Switch Evaluator",
        description="Evaluating domain AST expressions via exhaustive switch statements.",
        recommendation="Evaluate grammar nodes cleanly using compiler-verified switch over node tags.",
    ),
    PatternType.ITERATOR_STRUCT_NEXT: PatternDefinition(
        type=PatternType.ITERATOR_STRUCT_NEXT,
        category=PatternCategory.BEHAVIORAL,
        name="Iterator Struct Next",
        description="Idiomatic Zig iterator struct implementing 'fn next(self: *Self) ?T'.",
        recommendation="Implement 'next() ?Item' returning optional null when the sequence is exhausted.",
    ),
    PatternType.MEDIATOR_EVENT_BUS: PatternDefinition(
        type=PatternType.MEDIATOR_EVENT_BUS,
        category=PatternCategory.BEHAVIORAL,
        name="Mediator Event Bus",
        description="Central coordinator mediating communication between decoupled components.",
        recommendation="Use a Mediator to prevent N:N direct coupling between subsystems.",
    ),
    PatternType.MEMENTO_STATE_SNAPSHOT: PatternDefinition(
        type=PatternType.MEMENTO_STATE_SNAPSHOT,
        category=PatternCategory.BEHAVIORAL,
        name="Memento State Snapshot",
        description="Capturing immutable state snapshot for checkpointing and rollback.",
        recommendation="Save state structs into byte buffers or arena snapshots for fast checkpointing.",
    ),
    PatternType.OBSERVER_CALLBACK_SUBSCRIPTION: PatternDefinition(
        type=PatternType.OBSERVER_CALLBACK_SUBSCRIPTION,
        category=PatternCategory.BEHAVIORAL,
        name="Observer Callback Subscription",
        description="Registry of subscriber callback function pointers or listener interfaces.",
        recommendation="Maintain an ArrayList of listener callbacks and notify them on state change.",
    ),
    PatternType.STATE_MACHINE_TAGGED_UNION_FSM: PatternDefinition(
        type=PatternType.STATE_MACHINE_TAGGED_UNION_FSM,
        category=PatternCategory.BEHAVIORAL,
        name="State Machine Tagged Union FSM",
        description="Finite State Machine transitions dispatched via tagged union states.",
        recommendation="Represent FSM states as tagged unions to prevent invalid state field access.",
    ),
    PatternType.STRATEGY_FUNCTION_POINTER_INJECTION: PatternDefinition(
        type=PatternType.STRATEGY_FUNCTION_POINTER_INJECTION,
        category=PatternCategory.BEHAVIORAL,
        name="Strategy Function Pointer Injection",
        description="Interchangeable algorithm injected as a function pointer or comptime strategy.",
        recommendation="Pass sorting or hashing strategy functions explicitly to algorithms.",
    ),
    PatternType.TEMPLATE_METHOD_SKELETON_HOOKS: PatternDefinition(
        type=PatternType.TEMPLATE_METHOD_SKELETON_HOOKS,
        category=PatternCategory.BEHAVIORAL,
        name="Template Method Skeleton Hooks",
        description="Algorithm skeleton coordinating steps with optional lifecycle hooks.",
        recommendation="Structure multi-step operations into fixed skeleton flows calling customizable step methods.",
    ),
    PatternType.VISITOR_SWITCH_PAYLOAD_WALKER: PatternDefinition(
        type=PatternType.VISITOR_SWITCH_PAYLOAD_WALKER,
        category=PatternCategory.BEHAVIORAL,
        name="Visitor Switch Payload Walker",
        description="Visitor pattern traversing heterogeneous tagged union nodes with exhaustive switch.",
        recommendation="Use switch over union tags for zero-overhead visitor dispatch.",
    ),

    # 7. Safety, Memory & Concurrency Hazards
    PatternType.UNHANDLED_ERROR_UNION_CATCH_HAZARD: PatternDefinition(
        type=PatternType.UNHANDLED_ERROR_UNION_CATCH_HAZARD,
        category=PatternCategory.RESILIENCE,
        name="Unhandled Error Union Catch Hazard",
        description="Silent suppression of errors via '_ = func() catch {}' without logging or recovery.",
        recommendation="Handle error variants explicitly or propagate via 'try'.",
    ),
    PatternType.MISSING_DEFER_DEINIT_LEAK: PatternDefinition(
        type=PatternType.MISSING_DEFER_DEINIT_LEAK,
        category=PatternCategory.RESILIENCE,
        name="Missing Defer Deinit / Free Leak",
        description="Allocating memory or initializing a struct without a matching 'defer deinit()' or 'defer free()'.",
        recommendation="Always add 'defer instance.deinit()' immediately following successful '.init()'.",
    ),
    PatternType.UNREACHABLE_PANIC_IN_PRODUCTION: PatternDefinition(
        type=PatternType.UNREACHABLE_PANIC_IN_PRODUCTION,
        category=PatternCategory.RESILIENCE,
        name="Unreachable / Panic in Production",
        description="'unreachable' or '@panic()' statement in reachable code path.",
        recommendation="Replace unreachable with explicit error sets to prevent undefined behavior in ReleaseFast.",
    ),
    PatternType.RAW_POINTER_ALIGNMENT_HAZARD: PatternDefinition(
        type=PatternType.RAW_POINTER_ALIGNMENT_HAZARD,
        category=PatternCategory.RESILIENCE,
        name="Raw Pointer Alignment Hazard",
        description="Unchecked '@ptrCast' or '@alignCast' without safety verification.",
        recommendation="Ensure pointer alignment guarantees or use '@alignCast' with defensive assertions.",
    ),

    # 8. SOLID & Clean Code Quality
    PatternType.MONOLITHIC_STRUCT_SRP: PatternDefinition(
        type=PatternType.MONOLITHIC_STRUCT_SRP,
        category=PatternCategory.PRINCIPLE,
        name="Monolithic Struct SRP Violation",
        description="Struct declaring excessive fields (>= 12), violating Single Responsibility.",
        recommendation="Decompose large structs into cohesive sub-structs.",
    ),
    PatternType.FAT_VTABLE_INTERFACE_ISP: PatternDefinition(
        type=PatternType.FAT_VTABLE_INTERFACE_ISP,
        category=PatternCategory.PRINCIPLE,
        name="Fat VTable Interface ISP Violation",
        description="VTable struct declaring excessive function pointers (>= 10), violating Interface Segregation.",
        recommendation="Split broad VTables into specialized role-specific interfaces.",
    ),
    PatternType.MANUAL_TYPE_SWITCH_OCP: PatternDefinition(
        type=PatternType.MANUAL_TYPE_SWITCH_OCP,
        category=PatternCategory.PRINCIPLE,
        name="Manual Type Switch OCP Violation",
        description="Monolithic switch statement with >= 8 branches; consider comptime or polymorphic dispatch.",
        recommendation="Refactor giant switches into modular dispatch tables or comptime generic handlers.",
    ),
}
