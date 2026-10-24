from abc import ABC, abstractmethod
from typing import List, Dict, Any
from backend.models.analysis_model import StaticIssue, DuplicateSnippet

class BaseAnalyzer(ABC):
    @abstractmethod
    def analyze(self, code: str, filename: str) -> List[StaticIssue]:
        """Analyzes source code and returns a list of static issues."""
        pass
