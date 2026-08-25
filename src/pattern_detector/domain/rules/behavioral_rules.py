"""GoF Behavioral design pattern detection rules for Zig (11/11)."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BaseRule
from pattern_detector.domain.value_objects import (
    Confidence,
    Evidence,
    PatternCategory,
    PatternType,
)


class ChainOfResponsibilityPipelineRule(BaseRule):
    """Detects Chain of Responsibility pipeline handlers."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for s in model.all_structs:
            has_next = any("next" in f.name.lower() or "handler" in f.name.lower() for f in s.fields)
            if has_next or "Middleware" in s.name or "Pipeline" in s.name:
                evidences = [
                    Evidence(
                        rule_code="BEHAVIORAL_CHAIN_OF_RESPONSIBILITY",
                        description=f"Struct '{s.name}' implements Chain of Responsibility delegating requests along a linked handler pipeline",
                        weight=0.88,
                        location=s.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.CHAIN_OF_RESPONSIBILITY_PIPELINE,
                        pattern_category=PatternCategory.BEHAVIORAL,
                        target_name=s.name,
                        target_kind="struct",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=s.location,
                        evidences=evidences,
                    )
                )
        return detections


class CommandTaggedActionPayloadRule(BaseRule):
    """Detects Command tagged union variants carrying execution payloads."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for u in model.all_unions:
            if "Command" in u.name or "Action" in u.name or "Msg" in u.name or "Event" in u.name:
                evidences = [
                    Evidence(
                        rule_code="BEHAVIORAL_COMMAND_PAYLOAD",
                        description=f"Tagged union '{u.name}' encapsulates executable instructions and arguments as Command variants",
                        weight=0.90,
                        location=u.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.COMMAND_TAGGED_ACTION_PAYLOAD,
                        pattern_category=PatternCategory.BEHAVIORAL,
                        target_name=u.name,
                        target_kind="union",
                        confidence=Confidence(score=0.90, evidences=evidences),
                        primary_location=u.location,
                        evidences=evidences,
                    )
                )
        return detections


class InterpreterAstSwitchEvalRule(BaseRule):
    """Detects Interpreter pattern evaluating domain AST expressions via switch."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if fn.name in ("eval", "evaluate", "interpret", "exec_ast", "execute") and fn.switches_count >= 1:
                evidences = [
                    Evidence(
                        rule_code="BEHAVIORAL_INTERPRETER_EVAL",
                        description=f"Function '{fn.name}' evaluates domain AST grammar nodes via switch statement",
                        weight=0.92,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.INTERPRETER_AST_SWITCH_EVAL,
                        pattern_category=PatternCategory.BEHAVIORAL,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.92, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class IteratorStructNextRule(BaseRule):
    """Detects Iterator pattern implementing 'fn next(self: *Self) ?T'."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if fn.name == "next" and fn.return_type.startswith("?"):
                evidences = [
                    Evidence(
                        rule_code="BEHAVIORAL_ITERATOR_NEXT",
                        description=f"Function '{fn.name}' implements idiomatic Zig Iterator protocol returning optional sequence elements ('?T')",
                        weight=0.95,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.ITERATOR_STRUCT_NEXT,
                        pattern_category=PatternCategory.BEHAVIORAL,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.95, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class MediatorEventBusRule(BaseRule):
    """Detects Mediator event coordinator routing messages between subsystems."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for s in model.all_structs:
            if "Mediator" in s.name or "EventBus" in s.name or "Dispatcher" in s.name or "Coordinator" in s.name:
                evidences = [
                    Evidence(
                        rule_code="BEHAVIORAL_MEDIATOR_BUS",
                        description=f"Struct '{s.name}' mediates communication between decoupled components as an Event Bus",
                        weight=0.88,
                        location=s.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.MEDIATOR_EVENT_BUS,
                        pattern_category=PatternCategory.BEHAVIORAL,
                        target_name=s.name,
                        target_kind="struct",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=s.location,
                        evidences=evidences,
                    )
                )
        return detections


class MementoStateSnapshotRule(BaseRule):
    """Detects Memento pattern capturing immutable state snapshots."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for s in model.all_structs:
            if "Snapshot" in s.name or "Memento" in s.name or "Checkpoint" in s.name:
                evidences = [
                    Evidence(
                        rule_code="BEHAVIORAL_MEMENTO_SNAPSHOT",
                        description=f"Struct '{s.name}' captures immutable state snapshot for Memento checkpointing and rollback",
                        weight=0.90,
                        location=s.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.MEMENTO_STATE_SNAPSHOT,
                        pattern_category=PatternCategory.BEHAVIORAL,
                        target_name=s.name,
                        target_kind="struct",
                        confidence=Confidence(score=0.90, evidences=evidences),
                        primary_location=s.location,
                        evidences=evidences,
                    )
                )
        return detections


class ObserverCallbackSubscriptionRule(BaseRule):
    """Detects Observer subscription holding a list of listener callbacks."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for s in model.all_structs:
            has_listeners = any(
                "listener" in f.name.lower() or "callback" in f.name.lower() or "subscribers" in f.name.lower()
                for f in s.fields
            )
            if has_listeners or "Observer" in s.name or "Broadcaster" in s.name:
                evidences = [
                    Evidence(
                        rule_code="BEHAVIORAL_OBSERVER_CALLBACK",
                        description=f"Struct '{s.name}' maintains subscriber callback registry for Observer event notifications",
                        weight=0.90,
                        location=s.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.OBSERVER_CALLBACK_SUBSCRIPTION,
                        pattern_category=PatternCategory.BEHAVIORAL,
                        target_name=s.name,
                        target_kind="struct",
                        confidence=Confidence(score=0.90, evidences=evidences),
                        primary_location=s.location,
                        evidences=evidences,
                    )
                )
        return detections


class StateMachineTaggedUnionFsmRule(BaseRule):
    """Detects Finite State Machine transitions in tagged union states."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for u in model.all_unions:
            if ("State" in u.name or "Status" in u.name or "Phase" in u.name) and u.is_tagged:
                evidences = [
                    Evidence(
                        rule_code="BEHAVIORAL_STATE_FSM",
                        description=f"Tagged union '{u.name}' models Finite State Machine (FSM) states and transitions",
                        weight=0.92,
                        location=u.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.STATE_MACHINE_TAGNING_UNION_FSM if hasattr(PatternType, "STATE_MACHINE_TAGNING_UNION_FSM") else PatternType.STATE_MACHINE_TAGGED_UNION_FSM,
                        pattern_category=PatternCategory.BEHAVIORAL,
                        target_name=u.name,
                        target_kind="union",
                        confidence=Confidence(score=0.92, evidences=evidences),
                        primary_location=u.location,
                        evidences=evidences,
                    )
                )
        return detections


class StrategyFunctionPointerInjectionRule(BaseRule):
    """Detects Strategy pattern injecting interchangeable algorithm function pointers."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            strat_params = [
                p for p in fn.parameters
                if "fn(" in p.type_name or "*const fn" in p.type_name or "strategy" in p.name.lower()
            ]
            if strat_params:
                evidences = [
                    Evidence(
                        rule_code="BEHAVIORAL_STRATEGY_INJECTION",
                        description=f"Function '{fn.name}' injects interchangeable Strategy algorithm via parameter '{strat_params[0].name}'",
                        weight=0.88,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.STRATEGY_FUNCTION_POINTER_INJECTION,
                        pattern_category=PatternCategory.BEHAVIORAL,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class TemplateMethodSkeletonHooksRule(BaseRule):
    """Detects Template Method pattern coordinating step execution with hooks."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            has_steps = any(kw in fn.body for kw in ("step1", "step2", "pre_process", "post_process", "before", "after", "hook"))
            if has_steps and ("process" in fn.name or "run" in fn.name or "execute" in fn.name):
                evidences = [
                    Evidence(
                        rule_code="BEHAVIORAL_TEMPLATE_METHOD",
                        description=f"Function '{fn.name}' coordinates a Template Method skeleton pipeline with configurable lifecycle hooks",
                        weight=0.85,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.TEMPLATE_METHOD_SKELETON_HOOKS,
                        pattern_category=PatternCategory.BEHAVIORAL,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.85, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class VisitorSwitchPayloadWalkerRule(BaseRule):
    """Detects Visitor pattern traversing tagged union payloads via switch."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if (fn.name.startswith("visit") or fn.name in ("accept", "walk_node")) and fn.switches_count >= 1:
                evidences = [
                    Evidence(
                        rule_code="BEHAVIORAL_VISITOR_WALKER",
                        description=f"Function '{fn.name}' implements Visitor pattern matching over heterogeneous node variants via switch",
                        weight=0.90,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.VISITOR_SWITCH_PAYLOAD_WALKER,
                        pattern_category=PatternCategory.BEHAVIORAL,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.90, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections
