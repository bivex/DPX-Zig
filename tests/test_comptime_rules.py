"""Unit tests for Zig Comptime Metaprogramming rules."""

from __future__ import annotations

from pattern_detector.adapters.outbound.parsers.native_zig_parser import NativeZigParserAdapter
from pattern_detector.domain.rules.comptime_rules import (
    ComptimeGenericTypeFunctionRule,
    ComptimeStaticAssertionRule,
    ComptimeTypeInfoReflectionRule,
    InlineForWhileExpansionRule,
)
from pattern_detector.domain.value_objects import PatternType


def test_comptime_generic_type_function() -> None:
    code = """
pub fn ArrayList(comptime T: type) type {
    return struct {
        items: []T,
    };
}
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("list.zig", code)])

    rule = ComptimeGenericTypeFunctionRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.COMPTIME_GENERIC_TYPE_FUNCTION


def test_comptime_typeinfo_reflection() -> None:
    code = """
pub fn print_fields(comptime T: type) void {
    const info = @typeInfo(T);
    _ = info;
}
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("info.zig", code)])

    rule = ComptimeTypeInfoReflectionRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.COMPTIME_TYPEINFO_REFLECTION


def test_comptime_static_assertion() -> None:
    code = """
pub fn assert_size(comptime T: type) void {
    if (@sizeOf(T) > 64) {
        @compileError("Type T exceeds size threshold");
    }
}
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("assert.zig", code)])

    rule = ComptimeStaticAssertionRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.COMPTIME_STATIC_ASSERTION


def test_inline_for_while_expansion() -> None:
    code = """
pub fn iterate_tuple(tuple: anytype) void {
    inline for (tuple) |item| {
        _ = item;
    }
}
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("tuple.zig", code)])

    rule = InlineForWhileExpansionRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.INLINE_FOR_WHILE_EXPANSION
