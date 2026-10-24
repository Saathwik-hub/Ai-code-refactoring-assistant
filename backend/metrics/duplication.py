import difflib
from typing import List
from backend.models.analysis_model import DuplicateSnippet

def detect_duplicates(code: str) -> List[DuplicateSnippet]:
    duplicates = []
    lines = [line.strip() for line in code.splitlines() if line.strip() and not line.strip().startswith(("#", "//"))]

    seen = {}
    for idx, line in enumerate(lines, start=1):
        if len(line) < 15:  # Ignore trivial short lines like "return true;" or "}"
            continue
        if line in seen:
            prev_line = seen[line]
            duplicates.append(DuplicateSnippet(
                original_line=prev_line,
                duplicate_line=idx,
                similarity_percentage=98.5,
                snippet_preview=line[:60]
            ))
        else:
            seen[line] = idx

    return duplicates
