"""Unit tests for Zig Resilience, Memory Safety, and Low-Level Hazards."""

from __future__ import annotations

from pattern_detector.adapters.outbound.parsers.native_zig_parser import NativeZigParserAdapter
from pattern_detector.domain.rules.resilience_hazards_rules import (
    MissingDeferDeinitLeakRule,
    RawPointerAlignmentHazardRule,
    UnhandledErrorUnionCatchHazardRule,
    UnreachablePanicInProductionRule,
)
from pattern_detector.domain.value_objects import PatternType


def test_unhandled_error_union_catch_hazard() -> None:
    code = """
pub fn risky_operation() void {
    _ = perform_io() catch {};
}
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("catch.zig", code)])

    rule = UnhandledErrorUnionCatchHazardRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.UNHANDLED_ERROR_UNION_CATCH_HAZARD


def test_missing_defer_deinit_leak() -> None:
    code = """
pub fn leak_resource(allocator: std.mem.Allocator) void {
    const list = ArrayList.init(allocator);
    _ = list;
}
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("leak.zig", code)])

    rule = MissingDeferDeinitLeakRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.MISSING_DEFER_DEINIT_LEAK


def test_unreachable_panic_in_production() -> None:
    code = """
pub fn unsafe_fn() void {
    unreachable;
}
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("panic.zig", code)])

    rule = UnreachablePanicInProductionRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.UNREACHABLE_PANIC_IN_PRODUCTION


def test_raw_pointer_alignment_hazard() -> None:
    code = """
pub fn cast_pointer(ptr: [*]u8) *u32 {
    return @ptrCast(ptr);
}
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("ptr.zig", code)])

    rule = RawPointerAlignmentHazardRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.RAW_POINTER_ALIGNMENT_HAZARD
