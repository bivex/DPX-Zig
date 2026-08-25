"""Unit tests for Zig SOLID principles and systems code quality."""

from __future__ import annotations

from pattern_detector.adapters.outbound.parsers.native_zig_parser import NativeZigParserAdapter
from pattern_detector.domain.rules.solid_principles_rules import (
    FatVTableInterfaceIspRule,
    ManualTypeSwitchOcpRule,
    MonolithicStructSrpRule,
)
from pattern_detector.domain.value_objects import PatternType


def test_monolithic_struct_srp() -> None:
    fields = "\n".join(f"    f{i}: u32," for i in range(14))
    code = f"""
pub const MassiveStruct = struct {{
{fields}
}};
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("massive.zig", code)])

    rule = MonolithicStructSrpRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.MONOLITHIC_STRUCT_SRP


def test_fat_vtable_interface_isp() -> None:
    methods = "\n".join(f"    method_{i}: *const fn() void," for i in range(12))
    code = f"""
pub const FatVTable = struct {{
{methods}
}};
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("fat_vtable.zig", code)])

    rule = FatVTableInterfaceIspRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.FAT_VTABLE_INTERFACE_ISP


def test_manual_type_switch_ocp() -> None:
    prongs = "\n".join(f"        .case_{i} => handle_{i}()," for i in range(10))
    code = f"""
pub fn dispatch(cmd: Cmd) void {{
    switch (cmd) {{
{prongs}
    }}
}}
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("switch.zig", code)])

    rule = ManualTypeSwitchOcpRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.MANUAL_TYPE_SWITCH_OCP
