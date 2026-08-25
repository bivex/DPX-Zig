"""Unit tests for Zig SIMD, Inline Assembly, and C Interop rules."""

from __future__ import annotations

from pattern_detector.adapters.outbound.parsers.native_zig_parser import NativeZigParserAdapter
from pattern_detector.domain.rules.simd_hardware_rules import (
    CInteropTranslateCRule,
    InlineAssemblyIntrinsicRule,
    SimdVectorAccelerationRule,
)
from pattern_detector.domain.value_objects import PatternType


def test_simd_vector_acceleration() -> None:
    code = """
pub fn add_vectors(a: @Vector(4, f32), b: @Vector(4, f32)) @Vector(4, f32) {
    return a + b;
}
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("simd.zig", code)])

    rule = SimdVectorAccelerationRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.SIMD_VECTOR_ACCELERATION


def test_inline_assembly_intrinsic() -> None:
    code = """
pub fn disable_interrupts() void {
    asm volatile ("cli");
}
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("asm.zig", code)])

    rule = InlineAssemblyIntrinsicRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.INLINE_ASSEMBLY_INTRINSIC


def test_c_interop_translate_c() -> None:
    code = """
pub const c = @cImport({
    @cInclude("stdio.h");
});
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("c_binding.zig", code)])

    rule = CInteropTranslateCRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.C_INTEROP_TRANSLATE_C
