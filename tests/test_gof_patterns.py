"""Unit tests for all 23 GoF Creational, Structural, and Behavioral patterns in Zig."""

from __future__ import annotations

from pattern_detector.adapters.outbound.parsers.native_zig_parser import NativeZigParserAdapter
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
from pattern_detector.domain.rules.creational_rules import (
    AbstractFactoryVTableInterfaceRule,
    BuilderConfigurationFlowRule,
    FactoryInitAllocatorRule,
    PrototypeComptimeCloneRule,
    SingletonGlobalInstanceRule,
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
from pattern_detector.domain.value_objects import PatternType


# --- Creational (5/5) ---

def test_singleton_global_instance() -> None:
    code = """
pub const GlobalRegistry = struct {
    count: usize,
};
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("registry.zig", code)])

    rule = SingletonGlobalInstanceRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.SINGLETON_GLOBAL_INSTANCE


def test_factory_init_allocator() -> None:
    code = """
pub fn init(allocator: std.mem.Allocator, capacity: usize) !Self {
    return Self{ .items = try allocator.alloc(u8, capacity) };
}
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("factory.zig", code)])

    rule = FactoryInitAllocatorRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.FACTORY_INIT_ALLOCATOR


def test_abstract_factory_vtable_interface() -> None:
    code = """
pub const DriverFactory = struct {
    create_driver: *const fn(allocator: std.mem.Allocator) !*Driver,
};
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("factory_vtable.zig", code)])

    rule = AbstractFactoryVTableInterfaceRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.ABSTRACT_FACTORY_VTABLE_INTERFACE


def test_builder_configuration_flow() -> None:
    code = """
pub fn setTimeout(self: *Self, timeout: u64) *Self {
    self.timeout_ms = timeout;
    return self;
}
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("builder.zig", code)])

    rule = BuilderConfigurationFlowRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.BUILDER_CONFIGURATION_FLOW


def test_prototype_comptime_clone() -> None:
    code = """
pub fn clone(self: Self, allocator: std.mem.Allocator) !Self {
    return Self{ .data = try allocator.dupe(u8, self.data) };
}
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("proto.zig", code)])

    rule = PrototypeComptimeCloneRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.PROTOTYPE_COMPTIME_CLONE


# --- Structural (7/7) ---

def test_adapter_wrapper_type() -> None:
    code = """
pub const PosixFileAdapter = struct {
    handle: c_int,
};
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("adapter.zig", code)])

    rule = AdapterWrapperTypeRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.ADAPTER_WRAPPER_TYPE


def test_bridge_vtable_driver() -> None:
    code = """
pub const RenderBridge = struct {
    backend: *const GraphicsDriver,
};
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("bridge.zig", code)])

    rule = BridgeVTableDriverRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.BRIDGE_VTABLE_DRIVER


def test_composite_recursive_tagged_union() -> None:
    code = """
pub const Node = union(enum) {
    leaf: i32,
    branch: []Node,
};
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("tree.zig", code)])

    rule = CompositeRecursiveTaggedUnionRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.COMPOSITE_RECURSIVE_TAGGED_UNION


def test_decorator_allocator_wrapper() -> None:
    code = """
pub const LoggingAllocator = struct {
    child_allocator: std.mem.Allocator,
};
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("log_alloc.zig", code)])

    rule = DecoratorAllocatorWrapperRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.DECORATOR_ALLOCATOR_WRAPPER


def test_facade_root_module_api() -> None:
    code = """
pub const Config = struct {};
pub const State = struct {};

pub fn init() void {}
pub fn deinit() void {}
pub fn run() void {}
pub fn status() void {}
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("root.zig", code)])

    rule = FacadeRootModuleApiRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.FACADE_ROOT_MODULE_API


def test_flyweight_static_intern_pool() -> None:
    code = """
pub const StringInternPool = struct {
    capacity: usize,
};
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("pool.zig", code)])

    rule = FlyweightStaticInternPoolRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.FLYWEIGHT_STATIC_INTERN_POOL


def test_proxy_vtable_gateway() -> None:
    code = """
pub const SocketGateway = struct {
    socket: i32,
};
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("gateway.zig", code)])

    rule = ProxyVTableGatewayRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.PROXY_VTABLE_GATEWAY


# --- Behavioral (11/11) ---

def test_chain_of_responsibility_pipeline() -> None:
    code = """
pub const AuthMiddleware = struct {
    next_handler: *const fn(req: Request) Response,
};
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("middleware.zig", code)])

    rule = ChainOfResponsibilityPipelineRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.CHAIN_OF_RESPONSIBILITY_PIPELINE


def test_command_tagged_action_payload() -> None:
    code = """
pub const Command = union(enum) {
    write_file: []const u8,
    delete_file: []const u8,
};
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("cmd.zig", code)])

    rule = CommandTaggedActionPayloadRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.COMMAND_TAGGED_ACTION_PAYLOAD


def test_interpreter_ast_switch_eval() -> None:
    code = """
pub fn eval(node: Node) i64 {
    switch (node) {
        .number => |n| return n,
        .add => |pair| return eval(pair.left) + eval(pair.right),
    }
}
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("eval.zig", code)])

    rule = InterpreterAstSwitchEvalRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.INTERPRETER_AST_SWITCH_EVAL


def test_iterator_struct_next() -> None:
    code = """
pub fn next(self: *Self) ?u8 {
    if (self.index >= self.bytes.len) return null;
    const b = self.bytes[self.index];
    self.index += 1;
    return b;
}
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("iter.zig", code)])

    rule = IteratorStructNextRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.ITERATOR_STRUCT_NEXT


def test_mediator_event_bus() -> None:
    code = """
pub const EventBus = struct {
    subscribers_count: usize,
};
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("bus.zig", code)])

    rule = MediatorEventBusRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.MEDIATOR_EVENT_BUS


def test_memento_state_snapshot() -> None:
    code = """
pub const StateSnapshot = struct {
    step: u32,
    memory_used: usize,
};
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("snap.zig", code)])

    rule = MementoStateSnapshotRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.MEMENTO_STATE_SNAPSHOT


def test_observer_callback_subscription() -> None:
    code = """
pub const Broadcaster = struct {
    listeners: []const *const fn(event: Event) void,
};
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("obs.zig", code)])

    rule = ObserverCallbackSubscriptionRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.OBSERVER_CALLBACK_SUBSCRIPTION


def test_state_machine_tagged_union_fsm() -> None:
    code = """
pub const ConnectionState = union(enum) {
    disconnected,
    connecting: u32,
    connected: Socket,
};
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("fsm.zig", code)])

    rule = StateMachineTaggedUnionFsmRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.STATE_MACHINE_TAGGED_UNION_FSM


def test_strategy_function_pointer_injection() -> None:
    code = """
pub fn sort(items: []u32, sort_strategy: *const fn(a: u32, b: u32) bool) void {
    _ = items;
    _ = sort_strategy;
}
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("sort.zig", code)])

    rule = StrategyFunctionPointerInjectionRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.STRATEGY_FUNCTION_POINTER_INJECTION


def test_template_method_skeleton_hooks() -> None:
    code = """
pub fn process(self: *Self) void {
    self.step1_init();
    self.step2_execute();
    self.post_process_hook();
}
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("template.zig", code)])

    rule = TemplateMethodSkeletonHooksRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.TEMPLATE_METHOD_SKELETON_HOOKS


def test_visitor_switch_payload_walker() -> None:
    code = """
pub fn visit(node: Node) void {
    switch (node) {
        .leaf => |val| handle_leaf(val),
        .branch => |b| handle_branch(b),
    }
}
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("visitor.zig", code)])

    rule = VisitorSwitchPayloadWalkerRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.VISITOR_SWITCH_PAYLOAD_WALKER
