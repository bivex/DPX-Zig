"""Abstract base class for Zig pattern detection rules."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection


class BaseRule(ABC):
    """Base interface for all Zig static analysis and architectural rules."""

    @abstractmethod
    def evaluate(self, model: CodeModel) -> list[Detection]:
        """Evaluate rule heuristics across the Zig codebase model."""
        raise NotImplementedError
