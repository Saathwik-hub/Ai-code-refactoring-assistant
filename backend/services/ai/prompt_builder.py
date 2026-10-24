from typing import Dict, Any, Optional

class PromptBuilder:
    @staticmethod
    def build_refactor_prompt(
        code: str,
        language: str,
        mode: str,
        analysis_report: Optional[Dict[str, Any]] = None
    ) -> str:
        prompt = f"""You are a Senior Software Architect and Master Code Refactoring Assistant.
Your task is to refactor the following {language.upper()} source code adhering to the '{mode}' refactoring mode.

Original Source Code:
```{language}
{code}
```
"""
        if analysis_report:
            issues = analysis_report.get("issues", [])
            issues_summary = "\n".join([f"- Line {i.get('line')}: [{i.get('severity')}] {i.get('message')}" for i in issues[:10]])
            prompt += f"""
Static Code Analysis Findings to Address:
{issues_summary}

Complexity & Metrics:
- Cyclomatic Complexity: {analysis_report.get('complexity', {}).get('cyclomatic_complexity')}
- Maintainability Score: {analysis_report.get('scores', {}).get('maintainability')}%
"""

        prompt += f"""
Refactoring Instructions:
1. Preserve exact runtime functionality and business logic.
2. Apply clean code principles for the '{mode}' mode (e.g. guard clauses, descriptive naming, method extraction, removing duplicate logic).
3. Return the response in strict JSON format with keys:
   - "refactored_code": "<complete refactored code snippet>",
   - "explanations": [
       {{
         "title": "<short descriptive title of change>",
         "original_snippet": "<original line or block>",
         "refactored_snippet": "<new line or block>",
         "rationale": "<why this change improves the code>",
         "principle_used": "<e.g., Guard Clause, DRY, Single Responsibility>",
         "trade_off": "<any trade-off if applicable or None>"
       }}
     ]
"""
        return prompt
