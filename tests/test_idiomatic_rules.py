"""Unit tests for Zig Idiomatic and Systems Architecture rules."""

from __future__ import annotations

from pattern_detector.adapters.outbound.parsers.native_zig_parser import NativeZigParserAdapter
from pattern_detector.domain.rules.idiomatic_rules import (
    DeferErrdeferRaiiRule,
    ErrorUnionTryCatchRule,
    ExplicitAllocatorPassingRule,
    OpaqueTypeCHandleRule,
    PackedExternStructLayoutRule,
    TaggedUnionExhaustiveSwitchRule,
)
from pattern_detector.domain.value_objects import PatternType


def test_explicit_allocator_passing() -> None:
    code = """
pub fn create_buffer(allocator: std.mem.Allocator, size: usize) ![]u8 {
    return allocator.alloc(u8, size);
}
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("buf.zig", code)])

    rule = ExplicitAllocatorPassingRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.EXPLICIT_ALLOCATOR_PASSING


def test_defer_errdefer_raii() -> None:
    code = """
pub fn process_file(allocator: std.mem.Allocator) !void {
    const buf = try allocator.alloc(u8, 1024);
    defer allocator.free(buf);
    errdefer log_error();
}
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("file.zig", code)])

    rule = DeferErrdeferRaiiRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.DEFER_ERRDEFER_RAII


def test_error_union_try_catch() -> None:
    code = """
pub fn parse_int(str: []const u8) !i32 {
    const val = try std.fmt.parseInt(i32, str, 10);
    return val;
}
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("parse.zig", code)])

    rule = ErrorUnionTryCatchRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.ERROR_UNION_TRY_CATCH


def test_tagged_union_exhaustive_switch() -> None:
    code = """
pub const Token = union(enum) {
    identifier: []const u8,
    number: i64,
    eof,
};
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("token.zig", code)])

    rule = TaggedUnionExhaustiveSwitchRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.TAGGED_UNION_EXHAUSTIVE_SWITCH
    assert detections[0].target_name == "Token"


def test_packed_extern_struct_layout() -> None:
    code = """
pub const Register = packed struct {
    enabled: bool,
    mode: u3,
    reserved: u4,
};
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("reg.zig", code)])

    rule = PackedExternStructLayoutRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.PACKED_EXTERN_STRUCT_LAYOUT


def test_opaque_type_c_handle() -> None:
    code = """
pub const WindowHandle = opaque {};
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("win.zig", code)])

    rule = OpaqueTypeCHandleRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.OPAQUE_TYPE_C_HANDLE
