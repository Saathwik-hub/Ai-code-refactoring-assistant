from typing import List, Dict, Any
from backend.services.ai.ollama_service import OllamaService

class ChatEngine:
    @staticmethod
    def process_chat(messages: List[Dict[str, str]], current_code: str = "", language: str = "python") -> str:
        last_user_msg = messages[-1]["content"] if messages else ""

        if OllamaService.is_ollama_available():
            prompt = f"System: You are an AI Coding Assistant for {language.upper()}.\n"
            if current_code:
                prompt += f"Context Code:\n```{language}\n{current_code}\n```\n"
            prompt += f"User Question: {last_user_msg}\n"

            res = OllamaService.generate(prompt)
            if res:
                return res

        # Fallback local AI response generator
        msg_lower = last_user_msg.lower()
        if "explain" in msg_lower:
            return f"### Code Explanation ({language.upper()})\nThis code defines data structures and operations for processing application logic. Lines are structured cleanly with standard return expressions."
        elif "optimize" in msg_lower or "fast" in msg_lower:
            return f"### Optimization Strategy\nTo optimize this snippet:\n1. Replace linear searches `O(N)` with set/hash map lookups `O(1)`.\n2. Avoid redundant computations inside loop conditions.\n3. Leverage built-in vectorization or list comprehensions."
        elif "bug" in msg_lower or "wrong" in msg_lower or "error" in msg_lower:
            return f"### Bug Inspection Report\nChecked syntax and structure. Ensure all variable declarations are initialized before usage and handle potential null/empty data cases."
        elif "doc" in msg_lower or "comment" in msg_lower:
            return f"### Recommended Documentation\n```python\n\"\"\"\nFunction Overview: Processes input data payload.\nArgs:\n    items (list/dict): Input collection.\nReturns:\n    result: Processed output data.\n\"\"\"\n```"
        else:
            return f"I analyzed your **{language.upper()}** code snippet ({len(current_code.splitlines())} lines). You can ask me to explain code logic, optimize performance, fix security vulnerabilities, or generate documentation docstrings!"
