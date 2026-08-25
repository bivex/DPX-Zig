"""Unit tests verifying zero false positives on clean, idiomatic Zig systems code."""

from __future__ import annotations

from pattern_detector.adapters.outbound.parsers.native_zig_parser import NativeZigParserAdapter
from pattern_detector.domain.rules import get_default_rules
from pattern_detector.domain.rules.resilience_hazards_rules import (
    MissingDeferDeinitLeakRule,
    UnhandledErrorUnionCatchHazardRule,
    UnreachablePanicInProductionRule,
)
from pattern_detector.domain.rules.solid_principles_rules import (
    ManualTypeSwitchOcpRule,
    MonolithicStructSrpRule,
)
from pattern_detector.domain.services.rule_engine import RuleEngineService
from pattern_detector.domain.value_objects import PatternCategory


def test_clean_allocation_with_defer_no_leak() -> None:
    code = """
pub fn safe_allocation(allocator: std.mem.Allocator) !void {
    var list = std.ArrayList(u8).init(allocator);
    defer list.deinit();
    try list.append(42);
}
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("clean_alloc.zig", code)])

    rule = MissingDeferDeinitLeakRule()
    detections = rule.evaluate(model)

    assert len(detections) == 0


def test_clean_error_handling_with_try() -> None:
    code = """
pub fn safe_parse(str: []const u8) !u32 {
    return try std.fmt.parseInt(u32, str, 10);
}
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("safe_parse.zig", code)])

    rule = UnhandledErrorUnionCatchHazardRule()
    detections = rule.evaluate(model)

    assert len(detections) == 0


def test_clean_cohesive_struct_no_srp() -> None:
    code = """
pub const Point = struct {
    x: f32,
    y: f32,
    z: f32,
};
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("point.zig", code)])

    rule = MonolithicStructSrpRule()
    detections = rule.evaluate(model)

    assert len(detections) == 0


def test_clean_domain_service_no_hazards() -> None:
    code = """
pub fn calculate_distance(p1: Point, p2: Point) f32 {
    const dx = p1.x - p2.x;
    const dy = p1.y - p2.y;
    return @sqrt(dx * dx + dy * dy);
}
"""
    parser = NativeZigParserAdapter()
    model = parser.parse_codebase([("math.zig", code)])

    engine = RuleEngineService(rules=get_default_rules())
    detections = engine.evaluate(model)

    hazards = [d for d in detections if d.pattern_category in (PatternCategory.RESILIENCE, PatternCategory.PRINCIPLE)]
    assert len(hazards) == 0
